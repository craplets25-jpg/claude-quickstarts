"""
Debater SDK - Service Implementation

This package implements the NLP SERVICE LOGIC that powers argument analysis.

IMPORTANT: This is NOT an API client wrapper. This is the service implementation
itself, using LLMs (Claude) to provide the functionality that the reference
system provides through external HTTP endpoints.

Architecture:
    DebaterSDK (factory) → creates service instances
    BaseService (abstract) → common functionality
    *Service (concrete) → specific NLP capabilities

Usage:
    from debater_sdk import DebaterSDK

    sdk = DebaterSDK(api_key="your-anthropic-key")
    service = sdk.get_argument_quality_service()
    scores = service.run([{"sentence": "...", "topic": "..."}])
"""

__version__ = "1.0.0"

from .sdk import DebaterSDK
from .base import BaseService
from .exceptions import DebaterError, ValidationError, ProcessingError, LLMError

__all__ = [
    "DebaterSDK",
    "BaseService",
    "DebaterError",
    "ValidationError",
    "ProcessingError",
    "LLMError",
]
