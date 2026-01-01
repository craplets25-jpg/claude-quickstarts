"""Evidence Detection Client Implementation

Derived from requirement cards ED-001 through ED-012.
This implementation satisfies behavioral requirements without copying legacy implementation details.
"""

from typing import List, Dict, Any


class AbstractClient:
    """Base client providing authentication and batch processing capabilities."""

    def __init__(self, apikey: str):
        """Initialize client with API key for authentication.

        Args:
            apikey: API key for service authentication
        """
        self.apikey = apikey

    def run_in_batch(self, list_name: str, list: List[Any], other_payload: Dict,
                     endpoint: str, timeout: int) -> List[float]:
        """Process a batch of items through the service.

        This is a mock implementation that returns dummy scores.
        In a real implementation, this would make HTTP requests to the service.

        Args:
            list_name: Name of the list parameter for the API
            list: List of items to process
            other_payload: Additional payload data
            endpoint: Service endpoint path
            timeout: Request timeout in seconds

        Returns:
            List of confidence scores (one per input item)
        """
        # Mock implementation - returns dummy scores
        # Real implementation would make HTTP POST request
        return [0.5] * len(list)


class ClaimEvidenceDetectionClient(AbstractClient):
    """Base client for claim and evidence detection with shared validation and transformation logic."""

    def __init__(self, apikey: str):
        """Initialize client with API key.

        Args:
            apikey: API key for service authentication
        """
        super().__init__(apikey)

    def run(self, sentence_topic_dicts: List[Dict[str, str]]) -> List[float]:
        """Process sentence-topic pairs and return confidence scores.

        This method implements the processing pipeline:
        1. Input Validation - checks for empty fields
        2. Data Transformation - converts dicts to pairs
        3. Batch Processing - sends to service
        4. Returns confidence scores in same order as input

        Args:
            sentence_topic_dicts: List of dictionaries with 'sentence' and 'topic' keys

        Returns:
            List of confidence scores (one per input pair)

        Raises:
            RuntimeError: If any sentence or topic field is empty
        """
        # Stage 1: Input Validation - check all pairs before processing
        for i, sentence_topic_dict in enumerate(sentence_topic_dicts):
            if len(sentence_topic_dict['sentence']) == 0 or len(sentence_topic_dict['topic']) == 0:
                raise RuntimeError(f'empty input argument in pair {i}')

        # Stage 2: Data Transformation - extract pairs
        sentence_topic_pairs = [
            [dict_item['sentence'], dict_item['topic']]
            for dict_item in sentence_topic_dicts
        ]

        # Stage 3: Batch Processing - send to service
        scores = self.run_in_batch(
            list_name='sentence_topic_pairs',
            list=sentence_topic_pairs,
            other_payload={},
            endpoint='/score/',
            timeout=100
        )

        # Stage 4: Return results (order preserved by batch processing)
        return scores


class EvidenceDetectionClient(ClaimEvidenceDetectionClient):
    """Client for detecting evidence in sentence-topic pairs.

    Inherits validation, transformation, and batch processing from parent class.
    Distinct from ClaimDetectionClient despite shared functionality.
    """
    pass


class ClaimDetectionClient(ClaimEvidenceDetectionClient):
    """Client for detecting claims in sentence-topic pairs.

    Inherits validation, transformation, and batch processing from parent class.
    Distinct from EvidenceDetectionClient despite shared functionality.
    """
    pass


class DebaterApi:
    """Factory for creating Debater API client instances."""

    def __init__(self, apikey: str):
        """Initialize factory with API key.

        Args:
            apikey: API key for service authentication
        """
        self.apikey = apikey

    def get_evidence_detection_client(self) -> EvidenceDetectionClient:
        """Create an Evidence Detection client instance.

        Returns:
            EvidenceDetectionClient instance with API key
        """
        return EvidenceDetectionClient(self.apikey)

    def get_claim_detection_client(self) -> ClaimDetectionClient:
        """Create a Claim Detection client instance.

        Returns:
            ClaimDetectionClient instance with API key
        """
        return ClaimDetectionClient(self.apikey)
