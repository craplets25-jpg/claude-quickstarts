"""
DebaterSDK - Factory class for creating service instances.

This is the main entry point. It follows the Factory pattern to:
- Centralize configuration (API key, model)
- Lazy-initialize services (create on demand)
- Provide clean, consistent API

Architecture mirrors the reference pattern but implements service logic,
not API client wrappers.
"""

from typing import Optional


class DebaterSDK:
    """
    Factory for creating Debater service instances.

    Usage:
        sdk = DebaterSDK(api_key="...")
        service = sdk.get_argument_quality_service()
        results = service.run([{...}])

    Pattern: Create SDK once, get multiple services, all share configuration.
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize the SDK.

        Args:
            api_key: Anthropic API key
            model: Claude model to use for all services
        """
        self._api_key = api_key
        self._model = model

        # Lazy initialization - services created on first access
        self._argument_quality: Optional['ArgumentQualityService'] = None
        self._evidence_detection: Optional['EvidenceDetectionService'] = None
        self._claim_detection: Optional['ClaimDetectionService'] = None
        self._pro_con: Optional['ProConService'] = None
        self._clustering: Optional['ClusteringService'] = None
        self._term_wikifier: Optional['TermWikifierService'] = None

    def get_argument_quality_service(self):
        """
        Get ArgumentQualityService instance.

        Service scores argument quality on a 0.0-1.0 scale.

        Returns:
            ArgumentQualityService instance
        """
        if self._argument_quality is None:
            from .services.argument_quality import ArgumentQualityService
            self._argument_quality = ArgumentQualityService(self._api_key, self._model)
        return self._argument_quality

    def get_evidence_detection_service(self):
        """
        Get EvidenceDetectionService instance.

        Service detects evidence in sentence-topic pairs.

        Returns:
            EvidenceDetectionService instance
        """
        if self._evidence_detection is None:
            from .services.evidence_detection import EvidenceDetectionService
            self._evidence_detection = EvidenceDetectionService(self._api_key, self._model)
        return self._evidence_detection

    def get_claim_detection_service(self):
        """
        Get ClaimDetectionService instance.

        Service detects claims in sentence-topic pairs.

        Returns:
            ClaimDetectionService instance
        """
        if self._claim_detection is None:
            from .services.claim_detection import ClaimDetectionService
            self._claim_detection = ClaimDetectionService(self._api_key, self._model)
        return self._claim_detection

    def get_pro_con_service(self):
        """
        Get ProConService instance.

        Service scores pro/con stance on a -1.0 to +1.0 scale.

        Returns:
            ProConService instance
        """
        if self._pro_con is None:
            from .services.pro_con import ProConService
            self._pro_con = ProConService(self._api_key, self._model)
        return self._pro_con

    def get_clustering_service(self):
        """
        Get ClusteringService instance.

        Service clusters sentences by semantic similarity.

        Returns:
            ClusteringService instance
        """
        if self._clustering is None:
            from .services.clustering import ClusteringService
            self._clustering = ClusteringService(self._api_key, self._model)
        return self._clustering

    def get_term_wikifier_service(self):
        """
        Get TermWikifierService instance.

        Service annotates terms with Wikipedia links.

        Returns:
            TermWikifierService instance
        """
        if self._term_wikifier is None:
            from .services.term_wikifier import TermWikifierService
            self._term_wikifier = TermWikifierService(self._api_key, self._model)
        return self._term_wikifier
