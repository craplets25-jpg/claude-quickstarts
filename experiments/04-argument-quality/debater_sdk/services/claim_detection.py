"""
ClaimDetectionService - Detect claims in text using LLM.

Priority: P1 (implement after ArgumentQuality)
"""

from typing import List, Dict

from ..base import BaseService


class ClaimDetectionService(BaseService):
    """
    Detect claims in sentence-topic pairs (0.0-1.0 score).

    Input: [{"sentence": str, "topic": str}]
    Output: [float] (0.0-1.0, one score per input)
    """

    def _process_batch(
        self,
        sentence_topic_dicts: List[Dict[str, str]]
    ) -> List[float]:
        """TODO: Implement claim detection logic."""
        raise NotImplementedError("ClaimDetectionService - implement after ArgumentQuality")
