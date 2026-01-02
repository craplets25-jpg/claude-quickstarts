"""
Argument Quality Client

This module provides the ArgumentQualityClient class for scoring argument quality.
"""

from typing import List, Dict, Union


class ArgumentQualityClient:
    """
    Client for scoring argument quality.

    This client evaluates the quality of arguments (sentence-topic pairs)
    and returns numeric quality scores.
    """

    def __init__(self, apikey: str):
        """
        Initialize the ArgumentQualityClient.

        Args:
            apikey: API key for authentication

        Raises:
            ValueError: If API key is invalid or missing
        """
        if not apikey or not isinstance(apikey, str) or not apikey.strip():
            raise ValueError("API key must be a non-empty string")

        self.apikey = apikey

    def run(self, sentence_topic_dicts: List[Dict[str, str]], timeout: int = 60) -> List[float]:
        """
        Score the quality of sentence-topic pairs.

        Args:
            sentence_topic_dicts: List of dictionaries, each containing 'sentence' and 'topic' keys
            timeout: Optional timeout in seconds (default: 60)

        Returns:
            List of numeric quality scores, one for each input pair

        Raises:
            ValueError: If input validation fails
            KeyError: If required keys are missing
        """
        # Validate input is a list
        if not isinstance(sentence_topic_dicts, list):
            raise ValueError("Input must be a list of dictionaries")

        # Validate each dictionary
        for i, item in enumerate(sentence_topic_dicts):
            if not isinstance(item, dict):
                raise ValueError(f"Item at index {i} must be a dictionary")

            # Check for required keys
            if 'sentence' not in item:
                raise KeyError(f"Missing required key 'sentence' in dictionary at index {i}")
            if 'topic' not in item:
                raise KeyError(f"Missing required key 'topic' in dictionary at index {i}")

            # Validate non-empty strings
            sentence = item['sentence']
            topic = item['topic']

            if not isinstance(sentence, str) or len(sentence) == 0:
                raise ValueError(f"Empty sentence in input pair at index {i}")

            if not isinstance(topic, str) or len(topic) == 0:
                raise ValueError(f"Empty topic in input pair at index {i}")

        # Transform dictionaries to pairs for processing
        pairs = [[item['sentence'], item['topic']] for item in sentence_topic_dicts]

        # Process batch and return scores
        scores = self._score_pairs(pairs, timeout)

        return scores

    def _score_pairs(self, pairs: List[List[str]], timeout: int) -> List[float]:
        """
        Internal method to score sentence-topic pairs.

        This is a mock implementation that returns placeholder scores.
        In a real implementation, this would connect to a scoring service.

        Args:
            pairs: List of [sentence, topic] pairs
            timeout: Timeout in seconds

        Returns:
            List of quality scores (0.0 to 1.0)
        """
        # Mock implementation: return placeholder scores
        # Real implementation would make HTTP requests to scoring service
        scores = []
        for sentence, topic in pairs:
            # Simple heuristic for demonstration:
            # Score based on sentence length and relevance keywords
            score = self._calculate_mock_score(sentence, topic)
            scores.append(score)

        return scores

    def _calculate_mock_score(self, sentence: str, topic: str) -> float:
        """
        Calculate a mock quality score for testing purposes.

        This implements a simple heuristic to differentiate between
        high and low quality arguments for testing.

        Args:
            sentence: The argument sentence
            topic: The topic

        Returns:
            Quality score between 0.0 and 1.0
        """
        # Very simple heuristic for differentiation:
        # - Longer sentences with more words score higher
        # - Sentences with topic keywords score higher
        # - Very short or repetitive sentences score lower

        sentence_lower = sentence.lower()
        topic_lower = topic.lower()

        words = sentence_lower.split()
        word_count = len(words)
        unique_words = len(set(words))

        # Check for repetitive content
        if word_count > 0 and unique_words / word_count < 0.5:
            # Repetitive (e.g., "cars cars cars")
            return 0.25

        # Check for topic relevance
        topic_words = set(topic_lower.split())
        sentence_words = set(words)
        relevance = len(topic_words & sentence_words) > 0

        # Base score on word count
        if word_count < 5:
            base_score = 0.3
        elif word_count < 10:
            base_score = 0.5
        else:
            base_score = 0.7

        # Boost for relevance
        if relevance:
            base_score += 0.1

        # Cap at 1.0
        return min(1.0, base_score)


class DebaterApi:
    """
    Factory class for creating Debater API clients.

    This provides the factory pattern for accessing ArgumentQualityClient.
    """

    def __init__(self, apikey: str):
        """
        Initialize the DebaterApi factory.

        Args:
            apikey: API key for authentication
        """
        self.apikey = apikey

    def get_argument_quality_client(self) -> ArgumentQualityClient:
        """
        Get an ArgumentQualityClient instance.

        Returns:
            ArgumentQualityClient configured with the API key
        """
        return ArgumentQualityClient(self.apikey)
