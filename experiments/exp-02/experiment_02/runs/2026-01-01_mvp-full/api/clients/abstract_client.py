"""
Abstract base client for Debater API services.
Provides batch processing and HTTP communication capabilities.
"""
from typing import List, Dict, Any, Optional
import logging


class AbstractClient:
    """Base class for all Debater API clients."""

    def __init__(self, apikey: str):
        """
        Initialize the client with API key.

        Args:
            apikey: API key for authentication
        """
        self.apikey = apikey
        self.batch_size = 500
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_in_batch(
        self,
        list_name: str,
        list: List[Any],
        other_payload: Dict[str, Any],
        endpoint: str,
        timeout: int
    ) -> List[Any]:
        """
        Process a list of items in batches.

        Args:
            list_name: Name identifier for the list being processed
            list: List of items to process
            other_payload: Additional payload data
            endpoint: Service endpoint
            timeout: Request timeout in seconds

        Returns:
            List of results aggregated from all batches
        """
        results = []

        # Process in batches
        for i in range(0, len(list), self.batch_size):
            batch = list[i:i + self.batch_size]

            # For now, create a mock response
            # This will be replaced with actual HTTP communication
            batch_results = self._process_batch(batch, list_name, other_payload, endpoint, timeout)
            results.extend(batch_results)

        return results

    def _process_batch(
        self,
        batch: List[Any],
        list_name: str,
        other_payload: Dict[str, Any],
        endpoint: str,
        timeout: int
    ) -> List[Any]:
        """
        Process a single batch.

        Args:
            batch: Batch of items to process
            list_name: Name identifier for the list
            other_payload: Additional payload data
            endpoint: Service endpoint
            timeout: Request timeout in seconds

        Returns:
            List of results for this batch
        """
        # Mock implementation that returns mock scores
        # Each item in batch should be a [sentence, topic] pair
        return [0.5 for _ in batch]

    def set_host(self, host: str) -> None:
        """Set the service host URL."""
        self.host = host

    def set_show_process(self, show: bool) -> None:
        """Configure process visibility."""
        self.show_process = show

    def do_run(self, payload: Dict[str, Any], endpoint: str, timeout: int) -> Dict[str, Any]:
        """
        Execute HTTP request to service.

        Args:
            payload: Request payload
            endpoint: Service endpoint
            timeout: Request timeout in seconds

        Returns:
            Service response
        """
        # Mock implementation
        return {"scores": [0.5] * len(payload.get("sentence_topic_pairs", []))}
