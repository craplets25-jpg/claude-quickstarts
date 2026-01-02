"""
Service implementations for NLP capabilities.

Each service implements the LOGIC for a specific capability using LLMs.
These are not API client wrappers - they are the service implementations themselves.
"""

from .argument_quality import ArgumentQualityService
from .evidence_detection import EvidenceDetectionService
from .claim_detection import ClaimDetectionService
from .pro_con import ProConService
from .clustering import ClusteringService
from .term_wikifier import TermWikifierService

__all__ = [
    "ArgumentQualityService",
    "EvidenceDetectionService",
    "ClaimDetectionService",
    "ProConService",
    "ClusteringService",
    "TermWikifierService",
]
