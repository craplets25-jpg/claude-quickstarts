"""
TermWikifierService - Link terms to Wikipedia concepts.

Priority: P2 (implement later - may need Wikipedia API or knowledge base)
"""

from typing import List, Dict

from ..base import BaseService


class TermWikifierService(BaseService):
    """
    Annotate terms in sentences with Wikipedia links.

    Note: Different interface than other services.
    Input: List of sentences
    Output: List of dicts with term annotations
    """

    def run(self, sentences: List[str]) -> List[Dict]:
        """
        Wikify terms in sentences.

        Args:
            sentences: List of sentences to annotate

        Returns:
            List of dicts containing term annotations with Wikipedia links
        """
        raise NotImplementedError("TermWikifierService - implement later (needs Wikipedia API)")

    def _process_batch(self, sentence_topic_dicts):
        """Not used - TermWikifierService has different interface."""
        raise NotImplementedError("Use run() method instead")
