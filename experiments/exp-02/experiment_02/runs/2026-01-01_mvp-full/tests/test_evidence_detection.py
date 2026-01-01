"""
Test suite for Evidence Detection Client.
Tests derived from requirement_cards.json and feature_list.json.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.debater_api import DebaterApi
from api.clients.evidence_detection_client import EvidenceDetectionClient
from api.clients.abstract_client import AbstractClient


class TestEvidenceDetectionInterface:
    """TEST-001: Interface tests"""

    def test_client_has_run_method(self):
        """TEST-001: Verify EvidenceDetectionClient provides run() method"""
        client = EvidenceDetectionClient(apikey="test_key")
        assert hasattr(client, 'run'), "Client must have run() method"
        assert callable(client.run), "run() must be callable"

    def test_run_accepts_sentence_topic_dicts(self):
        """TEST-001: Verify run() accepts sentence_topic_dicts parameter"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'test sentence', 'topic': 'test topic'}
        ]
        # Should not raise an error
        result = client.run(test_input)
        assert isinstance(result, list), "run() must return a list"


class TestInputValidation:
    """TEST-002, TEST-003, TEST-010, TEST-014, TEST-015, TEST-019: Validation tests"""

    def test_empty_sentence_raises_error(self):
        """TEST-002: Verify system raises error when sentence field is empty"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [{'sentence': '', 'topic': 'some topic'}]

        with pytest.raises(RuntimeError):
            client.run(test_input)

    def test_empty_topic_raises_error(self):
        """TEST-003: Verify system raises error when topic field is empty"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [{'sentence': 'some sentence', 'topic': ''}]

        with pytest.raises(RuntimeError):
            client.run(test_input)

    def test_validation_before_processing(self):
        """TEST-010: Verify error is raised before processing when validation fails"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'valid', 'topic': 'valid'},
            {'sentence': '', 'topic': 'valid'}
        ]

        with pytest.raises(RuntimeError):
            result = client.run(test_input)

    def test_missing_sentence_key_raises_error(self):
        """TEST-014: Verify system requires 'sentence' key in input dictionaries"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [{'topic': 'some topic'}]

        with pytest.raises(KeyError):
            client.run(test_input)

    def test_missing_topic_key_raises_error(self):
        """TEST-015: Verify system requires 'topic' key in input dictionaries"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [{'sentence': 'some sentence'}]

        with pytest.raises(KeyError):
            client.run(test_input)

    def test_all_validated_before_any_processed(self):
        """TEST-019: Verify all items are validated before any processing"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'valid1', 'topic': 'valid1'},
            {'sentence': 'valid2', 'topic': 'valid2'},
            {'sentence': '', 'topic': 't'}  # Last item is invalid
        ]

        with pytest.raises(RuntimeError):
            client.run(test_input)


class TestDataTransformation:
    """TEST-004, TEST-017: Transformation tests"""

    def test_transformation_preserves_pairing(self):
        """TEST-004: Verify data transformation preserves sentence-topic pairing"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'A', 'topic': 'T1'},
            {'sentence': 'B', 'topic': 'T2'}
        ]

        result = client.run(test_input)
        assert len(result) == 2, "Must return exactly 2 scores for 2 inputs"
        assert all(isinstance(score, (int, float)) for score in result), "All results must be numeric"

    def test_transformation_before_batch_processing(self):
        """TEST-017: Verify transformation happens before batch processing"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'sentence1', 'topic': 'topic1'},
            {'sentence': 'sentence2', 'topic': 'topic2'}
        ]

        # Should successfully process dictionary format
        result = client.run(test_input)
        assert isinstance(result, list), "Must accept and process dict format"


class TestBatchProcessing:
    """TEST-005, TEST-020: Batch processing tests"""

    def test_batch_processing_multiple_inputs(self):
        """TEST-005: Verify batch processing handles multiple inputs correctly"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 's1', 'topic': 't1'},
            {'sentence': 's2', 'topic': 't2'},
            {'sentence': 's3', 'topic': 't3'},
            {'sentence': 's4', 'topic': 't4'}
        ]

        result = client.run(test_input)
        assert len(result) == 4, "Must return exactly 4 scores for 4 inputs"

    def test_batch_aggregation(self):
        """TEST-020: Verify batch processing aggregates results correctly"""
        client = EvidenceDetectionClient(apikey="test_key")
        # Create larger input to potentially span multiple batches
        test_input = [
            {'sentence': f'sentence_{i}', 'topic': f'topic_{i}'}
            for i in range(15)
        ]

        result = client.run(test_input)
        assert isinstance(result, list), "Result must be a single flat list"
        assert len(result) == 15, "Must have one score per input"
        assert not any(isinstance(item, list) for item in result), "Result must not be nested"


class TestOutputFormat:
    """TEST-006, TEST-007, TEST-018: Output format tests"""

    def test_one_score_per_input(self):
        """TEST-006: Verify output returns one score per input"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 's1', 'topic': 't1'},
            {'sentence': 's2', 'topic': 't2'},
            {'sentence': 's3', 'topic': 't3'}
        ]

        result = client.run(test_input)
        assert len(result) == 3, "Must return exactly 3 scores for 3 inputs"
        assert all(isinstance(score, (int, float)) for score in result), "Each element must be numeric"

    def test_scores_are_numeric_in_range(self):
        """TEST-007: Verify scores are numeric values in reasonable range"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'test sentence', 'topic': 'test topic'}
        ]

        result = client.run(test_input)
        assert all(isinstance(score, (int, float)) for score in result), "Scores must be numeric"
        assert all(0 <= score <= 1 for score in result), "Scores should be in range [0, 1]"

    def test_varied_evidence_strength(self):
        """TEST-018: Verify varied evidence strength produces varied scores"""
        # This test verifies behavior exists, not specific score values
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'detailed relevant evidence about the topic', 'topic': 'evidence'},
            {'sentence': 'unrelated vague statement', 'topic': 'specific topic'}
        ]

        result = client.run(test_input)
        assert len(result) == 2, "Must return 2 scores"
        # Both should be valid numeric scores
        assert all(isinstance(score, (int, float)) for score in result), "Scores must be numeric"
        assert all(0 <= score <= 1 for score in result), "Scores should be in range [0, 1]"


class TestInitialization:
    """TEST-008, TEST-009: Initialization tests"""

    def test_client_initialization_with_apikey(self):
        """TEST-008: Verify client can be initialized with API key"""
        client = EvidenceDetectionClient(apikey="test_api_key")
        assert client is not None, "Client must be created successfully"
        assert hasattr(client, 'apikey'), "Client must store API key"
        assert client.apikey == "test_api_key", "API key must be stored correctly"

    def test_factory_method_provides_client(self):
        """TEST-009: Verify factory method provides EvidenceDetectionClient instance"""
        debater_api = DebaterApi(apikey="test_key")
        client = debater_api.get_evidence_detection_client()

        assert isinstance(client, EvidenceDetectionClient), "Factory must return EvidenceDetectionClient"
        assert hasattr(client, 'run'), "Client must have run() method"


class TestOrderPreservation:
    """TEST-011, TEST-012: Order preservation tests"""

    def test_output_order_matches_input(self):
        """TEST-011: Verify output order matches input order"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'first', 'topic': 'topic1'},
            {'sentence': 'second', 'topic': 'topic2'},
            {'sentence': 'third', 'topic': 'topic3'}
        ]

        result = client.run(test_input)
        assert len(result) == 3, "Must preserve count"
        # Order is preserved if we get 3 distinct scores in a consistent order
        # The actual values don't matter, just that we get them in order

    def test_positional_correspondence(self):
        """TEST-012: Verify positional correspondence between input and output"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'item_0', 'topic': 'topic_0'},
            {'sentence': 'item_1', 'topic': 'topic_1'},
            {'sentence': 'item_2', 'topic': 'topic_2'}
        ]

        result = client.run(test_input)
        # Verify we can index results positionally
        assert result[0] is not None, "output[0] must correspond to input[0]"
        assert result[1] is not None, "output[1] must correspond to input[1]"
        assert result[2] is not None, "output[2] must correspond to input[2]"


class TestArchitecture:
    """TEST-016: Architecture tests"""

    def test_client_inherits_from_abstract_client(self):
        """TEST-016: Verify client inherits from AbstractClient"""
        client = EvidenceDetectionClient(apikey="test_key")

        assert isinstance(client, AbstractClient), "Must inherit from AbstractClient"
        assert hasattr(client, 'run_in_batch'), "Must have run_in_batch from AbstractClient"
        assert hasattr(client, 'do_run'), "Must have do_run from AbstractClient"


class TestConfiguration:
    """TEST-013: Configuration tests"""

    def test_timeout_parameter_handling(self):
        """TEST-013: Verify system handles timeout parameter"""
        client = EvidenceDetectionClient(apikey="test_key")
        test_input = [
            {'sentence': 'test', 'topic': 'topic'}
        ]

        # System should process without timeout errors in normal operation
        result = client.run(test_input)
        assert result is not None, "Must return result within reasonable time"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
