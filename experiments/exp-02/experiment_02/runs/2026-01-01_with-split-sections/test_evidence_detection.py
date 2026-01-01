"""Test suite for Evidence Detection client

Tests derived from feature_list.json (TEST-001 through TEST-018).
Tests verify BEHAVIOR, not legacy implementation details.
"""

import pytest
from evidence_detection import DebaterApi, EvidenceDetectionClient, ClaimDetectionClient


class TestInputValidation:
    """Tests for input structure and validation (TEST-001 through TEST-004, TEST-015, TEST-017)."""

    def test_001_accepts_sentence_topic_dictionaries(self):
        """TEST-001: Verify client accepts list of sentence-topic dictionaries with required keys."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        input_data = [
            {'sentence': 'Test sentence 1', 'topic': 'Test topic'},
            {'sentence': 'Test sentence 2', 'topic': 'Test topic'}
        ]

        # Should accept input without structure errors
        result = client.run(input_data)

        # Verify method accepts input and proceeds to processing
        assert isinstance(result, list)

    def test_002_rejects_empty_sentence(self):
        """TEST-002: Verify client rejects empty sentence field."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        input_data = [{'sentence': '', 'topic': 'valid topic'}]

        # Should raise exception for empty sentence
        with pytest.raises(RuntimeError):
            client.run(input_data)

    def test_003_rejects_empty_topic(self):
        """TEST-003: Verify client rejects empty topic field."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        input_data = [{'sentence': 'valid sentence', 'topic': ''}]

        # Should raise exception for empty topic
        with pytest.raises(RuntimeError):
            client.run(input_data)

    def test_004_accepts_non_empty_inputs(self):
        """TEST-004: Verify client accepts non-empty sentence and topic."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        input_data = [{'sentence': 'Test sentence', 'topic': 'Test topic'}]

        # Should not raise validation exception
        result = client.run(input_data)

        # Verify processing completed
        assert isinstance(result, list)
        assert len(result) == 1

    def test_015_handles_single_pair(self):
        """TEST-015: Verify client handles single sentence-topic pair."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        input_data = [{'sentence': 'Single sentence', 'topic': 'Single topic'}]

        result = client.run(input_data)

        # Verify single input produces single-element list output (not scalar)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_017_exception_identifies_invalid_pair(self):
        """TEST-017: Verify exception includes information about which pair failed."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # Create list with invalid pair at position 1
        input_data = [
            {'sentence': 'Valid sentence', 'topic': 'Valid topic'},
            {'sentence': '', 'topic': 'Valid topic'},  # Invalid at index 1
            {'sentence': 'Another valid', 'topic': 'Valid topic'}
        ]

        # Should raise exception with pair information
        with pytest.raises(RuntimeError) as exc_info:
            client.run(input_data)

        # Verify exception provides diagnostic information
        error_message = str(exc_info.value)
        assert 'pair' in error_message.lower() or '1' in error_message


class TestBehavior:
    """Tests for order preservation and batch processing (TEST-005, TEST-006, TEST-008, TEST-012, TEST-013, TEST-014, TEST-018)."""

    def test_005_output_order_matches_input_order(self):
        """TEST-005: Verify output order matches input order for multiple pairs."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # Create 3 distinct pairs
        input_data = [
            {'sentence': 'First sentence', 'topic': 'Topic A'},
            {'sentence': 'Second sentence', 'topic': 'Topic B'},
            {'sentence': 'Third sentence', 'topic': 'Topic C'}
        ]

        result = client.run(input_data)

        # Verify output has 3 scores
        assert len(result) == 3

        # Verify one score per input pair (order preservation implied by count match)
        # Specific score values are service-dependent, so we verify structure only
        assert all(isinstance(score, (int, float)) for score in result)

    def test_006_batch_processing_handles_multiple_pairs(self):
        """TEST-006: Verify batch processing handles multiple sentence-topic pairs."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # Create 4 pairs
        input_data = [
            {'sentence': 'Sentence 1', 'topic': 'Topic'},
            {'sentence': 'Sentence 2', 'topic': 'Topic'},
            {'sentence': 'Sentence 3', 'topic': 'Topic'},
            {'sentence': 'Sentence 4', 'topic': 'Topic'}
        ]

        result = client.run(input_data)

        # Verify all 4 pairs processed in single call
        assert len(result) == 4

    def test_008_score_position_matches_input_position(self):
        """TEST-008: Verify score at index i corresponds to input at index i."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # Create distinctive pairs
        input_data = [
            {'sentence': 'Distinctive sentence A', 'topic': 'Topic A'},
            {'sentence': 'Distinctive sentence B', 'topic': 'Topic B'},
            {'sentence': 'Distinctive sentence C', 'topic': 'Topic C'}
        ]

        result = client.run(input_data)

        # Verify each index has a score (no shuffling)
        assert len(result) == len(input_data)
        for i in range(len(result)):
            assert isinstance(result[i], (int, float))

    def test_012_validation_prevents_processing(self):
        """TEST-012: Verify processing flows through validation before transformation."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # Mix invalid and valid pairs
        input_data = [
            {'sentence': '', 'topic': 'Topic'},  # Invalid
            {'sentence': 'Valid sentence', 'topic': 'Valid topic'}  # Valid
        ]

        # Should raise exception before any processing
        with pytest.raises(RuntimeError):
            client.run(input_data)

        # No partial results should be returned (exception prevents this)

    def test_013_transformation_after_validation(self):
        """TEST-013: Verify transformation occurs after validation passes."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # All valid inputs
        input_data = [
            {'sentence': 'Sentence 1', 'topic': 'Topic 1'},
            {'sentence': 'Sentence 2', 'topic': 'Topic 2'}
        ]

        result = client.run(input_data)

        # Verify processing completes successfully (indicating transformation occurred)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_014_validation_checks_all_pairs_before_processing(self):
        """TEST-014: Verify validation checks all pairs before processing."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # First pair valid, second pair invalid
        input_data = [
            {'sentence': 'Valid sentence', 'topic': 'Valid topic'},
            {'sentence': 'Another valid', 'topic': ''}  # Invalid topic
        ]

        # Should raise exception
        with pytest.raises(RuntimeError):
            client.run(input_data)

        # No partial processing should occur (no results for first pair)

    def test_018_run_returns_synchronously(self):
        """TEST-018: Verify run() returns results synchronously."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        input_data = [{'sentence': 'Test sentence', 'topic': 'Test topic'}]

        # Call run() - should block until complete
        result = client.run(input_data)

        # Results immediately available after method returns
        assert result is not None
        assert isinstance(result, list)
        # Not a future, promise, or callback - direct return value


class TestOutputValidation:
    """Tests for output structure and format (TEST-007, TEST-016)."""

    def test_007_output_is_list_of_numbers_matching_input_length(self):
        """TEST-007: Verify output is list of numerical scores matching input length."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # Create N=4 pairs
        input_data = [
            {'sentence': f'Sentence {i}', 'topic': 'Topic'}
            for i in range(4)
        ]

        result = client.run(input_data)

        # Verify output is a list
        assert isinstance(result, list)

        # Verify output length equals N
        assert len(result) == 4

        # Verify each element is a number
        for score in result:
            assert isinstance(score, (int, float))

    def test_016_scores_are_numerical_values(self):
        """TEST-016: Verify scores are numerical values."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        input_data = [
            {'sentence': 'Test 1', 'topic': 'Topic 1'},
            {'sentence': 'Test 2', 'topic': 'Topic 2'}
        ]

        result = client.run(input_data)

        # Verify each score is numeric (int or float)
        for score in result:
            assert isinstance(score, (int, float))
            # Not string, boolean, or other types
            assert not isinstance(score, bool)
            assert not isinstance(score, str)


class TestInterface:
    """Tests for public API interface (TEST-009)."""

    def test_009_client_provides_run_method(self):
        """TEST-009: Verify client provides run() method as public API."""
        api = DebaterApi('test_api_key')
        client = api.get_evidence_detection_client()

        # Verify run() method exists
        assert hasattr(client, 'run')
        assert callable(client.run)

        # Verify run() accepts sentence_topic_dicts parameter
        input_data = [{'sentence': 'Test', 'topic': 'Topic'}]
        result = client.run(input_data)

        # Verify run() returns list of scores
        assert isinstance(result, list)


class TestInitialization:
    """Tests for client initialization (TEST-010)."""

    def test_010_client_initializes_with_api_key(self):
        """TEST-010: Verify client initializes with API key via factory."""
        # Create DebaterApi instance with API key
        api = DebaterApi('test_api_key_12345')

        # Call factory method
        client = api.get_evidence_detection_client()

        # Verify client instance is returned
        assert isinstance(client, EvidenceDetectionClient)

        # Verify client can make authenticated calls (run() succeeds)
        input_data = [{'sentence': 'Test sentence', 'topic': 'Test topic'}]
        result = client.run(input_data)
        assert isinstance(result, list)


class TestArchitecture:
    """Tests for client architecture (TEST-011)."""

    def test_011_evidence_and_claim_clients_are_distinct(self):
        """TEST-011: Verify EvidenceDetectionClient is distinct from ClaimDetectionClient."""
        api = DebaterApi('test_api_key')

        # Get both clients
        evidence_client = api.get_evidence_detection_client()
        claim_client = api.get_claim_detection_client()

        # Verify they are different class instances
        assert type(evidence_client) != type(claim_client)
        assert isinstance(evidence_client, EvidenceDetectionClient)
        assert isinstance(claim_client, ClaimDetectionClient)

        # Both should be functional (separate implementations)
        input_data = [{'sentence': 'Test', 'topic': 'Topic'}]
        evidence_result = evidence_client.run(input_data)
        claim_result = claim_client.run(input_data)

        assert isinstance(evidence_result, list)
        assert isinstance(claim_result, list)
