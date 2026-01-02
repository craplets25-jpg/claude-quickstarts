"""
ProConService - Score pro/con stance using LLM.

Priority: P1 (implement after ArgumentQuality)
"""

from typing import List, Dict

from ..base import BaseService


class ProConService(BaseService):
    """
    Score pro/con stance (-1.0 to +1.0).

    Input: [{"sentence": str, "topic": str}]
    Output: [float] (-1.0 to +1.0, negative=con, positive=pro)
    """

    def _process_batch(
        self,
        sentence_topic_dicts: List[Dict[str, str]]
    ) -> List[float]:
        """TODO: Implement pro/con scoring logic."""
        raise NotImplementedError("ProConService - implement after ArgumentQuality")
