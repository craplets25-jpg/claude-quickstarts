"""
Factory for creating Debater SDK client instances.
"""


class DebaterApi:
    """Factory class for instantiating Debater SDK clients."""

    def __init__(self, apikey: str):
        """
        Initialize the Debater API factory.

        Args:
            apikey: API key for authentication

        Raises:
            ValueError: If API key is invalid or missing
        """
        if not apikey or not isinstance(apikey, str) or len(apikey.strip()) == 0:
            raise ValueError("API key is required and must be a non-empty string")
        self._apikey = apikey

    def get_evidence_detection_client(self):
        """
        Create and return an Evidence Detection client instance.

        Returns:
            EvidenceDetectionClient: Client for evidence detection operations
        """
        from evidence_detection_client import EvidenceDetectionClient
        return EvidenceDetectionClient(self._apikey)
