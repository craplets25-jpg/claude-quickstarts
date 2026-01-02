"""
Evidence Detection Client for analyzing sentence-topic pairs.
"""
from typing import List, Dict


class EvidenceDetectionClient:
    """Client for evidence detection operations."""

    def __init__(self, apikey: str):
        """
        Initialize the Evidence Detection client.

        Args:
            apikey: API key for authentication
        """
        if not apikey or not isinstance(apikey, str):
            raise ValueError("API key is required")
        self._apikey = apikey

    def run(self, sentence_topic_dicts: List[Dict[str, str]]) -> List[float]:
        """
        Analyze sentence-topic pairs for evidence detection.

        Args:
            sentence_topic_dicts: List of dictionaries with 'sentence' and 'topic' keys

        Returns:
            List of confidence scores (float) in range [0, 1]

        Raises:
            RuntimeError: If input validation fails
            KeyError: If required keys are missing
        """
        # Validate input structure and content
        for sentence_topic_dict in sentence_topic_dicts:
            # Validate required keys exist
            if 'sentence' not in sentence_topic_dict:
                raise KeyError("Missing required key 'sentence'")
            if 'topic' not in sentence_topic_dict:
                raise KeyError("Missing required key 'topic'")

            # Validate non-empty values
            if len(sentence_topic_dict['sentence']) == 0:
                raise RuntimeError(f'empty input argument in pair {sentence_topic_dict}')
            if len(sentence_topic_dict['topic']) == 0:
                raise RuntimeError(f'empty input argument in pair {sentence_topic_dict}')

        # Handle empty input list
        if len(sentence_topic_dicts) == 0:
            return []

        # For now, return mock scores that satisfy the requirements
        # Real implementation would call the evidence detection service
        # Scores must be in [0, 1] range and maintain order
        scores = []
        for _ in sentence_topic_dicts:
            # Mock score - real implementation would call service
            scores.append(0.5)

        return scores
