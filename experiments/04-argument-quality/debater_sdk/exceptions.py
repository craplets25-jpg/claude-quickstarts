"""
Custom exceptions for the Debater SDK.

These exceptions represent failure modes in the SERVICE LOGIC,
not HTTP/network errors from external APIs.
"""


class DebaterError(Exception):
    """Base exception for all Debater SDK errors."""
    pass


class ValidationError(DebaterError):
    """Input validation failed (empty strings, wrong types, etc.)."""
    pass


class ProcessingError(DebaterError):
    """Service processing failed (LLM errors, logic errors, etc.)."""
    pass


class LLMError(DebaterError):
    """LLM API call failed (authentication, rate limits, etc.)."""
    pass
