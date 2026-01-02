"""
BaseService - Abstract base class for all NLP services.

This class provides the common infrastructure for implementing service logic.
Each subclass implements a specific NLP capability using LLMs.

ARCHITECTURE NOTE:
The reference system has:
    Client (HTTP wrapper) → External Service (black box) → Results

Our system has:
    Service (this class) → LLM (Claude) → Results

We're implementing what's INSIDE the external service, not the HTTP client.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
import time

from anthropic import Anthropic

from .exceptions import ValidationError, ProcessingError, LLMError


class BaseService(ABC):
    """
    Abstract base class for all Debater services.

    Provides:
    - LLM client management (Anthropic/Claude)
    - Input validation (empty strings, required fields)
    - Timing and logging
    - Helper method for LLM calls

    Subclasses implement:
    - _process_batch() - Core service logic for the specific capability
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize the service.

        Args:
            api_key: Anthropic API key (supports standard or Foundry keys)
            model: Claude model to use for processing
        """
        # Detect Foundry API keys and set appropriate base URL
        if api_key and not api_key.startswith('sk-ant-'):
            # Foundry API key
            self.client = Anthropic(
                api_key=api_key,
                base_url="https://api.forge.anthropic.com"
            )
        else:
            # Standard Anthropic API key
            self.client = Anthropic(api_key=api_key)

        self.model = model
        self.logger = logging.getLogger(f"debater_sdk.{self.__class__.__name__}")

    def run(
        self,
        sentence_topic_dicts: List[Dict[str, str]],
        timeout: int = 60
    ) -> List[float]:
        """
        Process sentence-topic pairs and return scores.

        This is the PUBLIC API. It handles validation, timing, and logging.
        Actual processing is delegated to _process_batch() (implemented by subclasses).

        Args:
            sentence_topic_dicts: List of dicts with 'sentence' and 'topic' keys
            timeout: Processing timeout in seconds (for future use)

        Returns:
            List of float scores corresponding to input pairs

        Raises:
            ValidationError: If input validation fails
            ProcessingError: If processing fails
        """
        # Validate inputs
        self._validate_inputs(sentence_topic_dicts)

        # Process with timing
        start_time = time.time()
        try:
            results = self._process_batch(sentence_topic_dicts)
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise ProcessingError(f"Failed to process batch: {e}") from e

        # Log timing
        elapsed_ms = (time.time() - start_time) * 1000
        self.logger.info(f"{self.__class__.__name__}.run = {elapsed_ms:.0f}ms.")

        return results

    def _validate_inputs(self, sentence_topic_dicts: List[Dict[str, str]]) -> None:
        """
        Validate input format and content.

        From reference behavior: Must raise RuntimeError for empty sentence/topic.

        Args:
            sentence_topic_dicts: Input to validate

        Raises:
            RuntimeError: If sentence or topic is empty (matches reference behavior)
        """
        if not isinstance(sentence_topic_dicts, list):
            raise RuntimeError("Input must be a list")

        for pair in sentence_topic_dicts:
            if not isinstance(pair, dict):
                raise RuntimeError(f"Each item must be a dict, got {type(pair)}")

            sentence = pair.get('sentence', '')
            topic = pair.get('topic', '')

            # Match reference error behavior
            if len(sentence) == 0:
                raise RuntimeError(f'empty input argument in pair {pair}')
            if len(topic) == 0:
                raise RuntimeError(f'empty input argument in pair {pair}')

    @abstractmethod
    def _process_batch(
        self,
        sentence_topic_dicts: List[Dict[str, str]]
    ) -> List[float]:
        """
        Process a batch of sentence-topic pairs.

        This is where the SERVICE LOGIC lives. Subclasses implement this
        using LLM calls to replicate the functionality of the external service.

        Args:
            sentence_topic_dicts: Validated list of sentence-topic pairs

        Returns:
            List of float scores (one per input pair)
        """
        pass

    def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.0
    ) -> str:
        """
        Helper method for making LLM calls.

        Provides:
        - Consistent API across services
        - Error handling and logging
        - Future: retry logic, caching, etc.

        Args:
            system_prompt: System prompt (defines task/role)
            user_prompt: User prompt (specific input)
            max_tokens: Max tokens in response
            temperature: Sampling temperature (0 = deterministic)

        Returns:
            Text response from LLM

        Raises:
            LLMError: If LLM call fails
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return response.content[0].text

        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            raise LLMError(f"LLM API call failed: {e}") from e
