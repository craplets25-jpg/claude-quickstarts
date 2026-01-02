"""
Evidence Detection Client for Debater API.
"""
from typing import List, Dict
import datetime
import logging
from .abstract_client import AbstractClient


class EvidenceDetectionClient(AbstractClient):
    """
    Client for evidence detection service.

    Detects evidence in sentence-topic pairs and returns confidence scores.
    """

    def __init__(self, apikey: str):
        """
        Initialize the evidence detection client.

        Args:
            apikey: API key for authentication
        """
        super().__init__(apikey)
        self.logger = logging.getLogger(__name__)

    def run(self, sentence_topic_dicts: List[Dict[str, str]]) -> List[float]:
        """
        Run evidence detection on sentence-topic pairs.

        Args:
            sentence_topic_dicts: List of dictionaries with 'sentence' and 'topic' keys

        Returns:
            List of confidence scores (0-1), one per input, in same order

        Raises:
            RuntimeError: If any sentence or topic is empty
            KeyError: If required keys are missing
        """
        # Start timing
        time_stamp_start = datetime.datetime.now().timestamp()

        # Validate all inputs before processing
        for i, dict_item in enumerate(sentence_topic_dicts):
            # Check for required keys
            if 'sentence' not in dict_item or 'topic' not in dict_item:
                raise KeyError(f"Missing required keys in input at index {i}")

            # Check for empty strings
            if len(dict_item['sentence']) == 0 or len(dict_item['topic']) == 0:
                raise RuntimeError(f"empty input argument in pair {dict_item}")

        # Transform dictionaries to pairs
        pairs = [[dict_item['sentence'], dict_item['topic']] for dict_item in sentence_topic_dicts]

        # Process in batches
        endpoint = "/score/"
        scores = self.run_in_batch(
            list_name='sentence_topic_pairs',
            list=pairs,
            other_payload={},
            endpoint=endpoint,
            timeout=100
        )

        # End timing and log
        time_stamp_end = datetime.datetime.now().timestamp()
        execution_time_ms = 1000 * (time_stamp_end - time_stamp_start)
        self.logger.info(f'evidence_detection_client.run = {execution_time_ms}ms.')

        return scores
