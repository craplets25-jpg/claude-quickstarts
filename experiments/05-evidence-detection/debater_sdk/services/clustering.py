"""
ClusteringService - Cluster similar sentences using LLM.

Priority: P2 (implement later - may need embeddings)
"""

from typing import List

from ..base import BaseService


class ClusteringService(BaseService):
    """
    Cluster sentences by semantic similarity.

    Note: Different interface than other services.
    Input: sentences list + num_clusters parameter
    Output: List of lists (clusters)
    """

    def run(self, sentences: List[str], num_of_clusters: int = 2) -> List[List[str]]:
        """
        Cluster sentences.

        Args:
            sentences: List of sentences to cluster
            num_of_clusters: Number of clusters to create

        Returns:
            List of clusters (each cluster is a list of sentences)
        """
        raise NotImplementedError("ClusteringService - implement later (may need embeddings)")

    def _process_batch(self, sentence_topic_dicts):
        """Not used - ClusteringService has different interface."""
        raise NotImplementedError("Use run() method instead")
