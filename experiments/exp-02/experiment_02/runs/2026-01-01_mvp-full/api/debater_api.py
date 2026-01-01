"""
Main factory class for Debater API clients.
"""
from .clients.evidence_detection_client import EvidenceDetectionClient


class DebaterApi:
    """
    Factory for creating Debater API client instances.
    """

    def __init__(self, apikey: str):
        """
        Initialize the Debater API factory.

        Args:
            apikey: API key for authentication
        """
        self.apikey = apikey

    def get_evidence_detection_client(self) -> EvidenceDetectionClient:
        """
        Create an EvidenceDetectionClient instance.

        Returns:
            EvidenceDetectionClient instance configured with API key
        """
        return EvidenceDetectionClient(self.apikey)
