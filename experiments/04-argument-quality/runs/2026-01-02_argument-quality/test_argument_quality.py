"""
Test suite for Argument Quality Client

This test suite validates all requirements from feature_list.json
"""

import pytest
from argument_quality_client import ArgumentQualityClient, DebaterApi


class TestArgumentQualityClient:
    """Test suite for ArgumentQualityClient"""

    def setup_method(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = ArgumentQualityClient(self.api_key)

    # TEST-001: Client initialization with API key
    def test_client_initialization_with_api_key(self):
        """Verify ArgumentQualityClient can be initialized with an API key"""
        # Create instance
        client = ArgumentQualityClient("test_api_key")

        # Verify instance is created successfully
        assert client is not None

        # Verify instance type
        assert isinstance(client, ArgumentQualityClient)

        # Verify API key is stored
        assert client.apikey == "test_api_key"

    def test_client_initialization_requires_api_key(self):
        """Verify that API key validation occurs during initialization"""
        # Empty string should raise error
        with pytest.raises(ValueError):
            ArgumentQualityClient("")

        # None should raise error
        with pytest.raises(ValueError):
            ArgumentQualityClient(None)

    # TEST-002: Input format validation
    def test_run_accepts_list_of_dictionaries(self):
        """Verify run method accepts list of dictionaries with sentence and topic keys"""
        # Create valid input
        valid_input = [{'sentence': 'Test sentence', 'topic': 'Test topic'}]

        # Call run method
        result = self.client.run(valid_input)

        # Verify method accepts input without raising error
        assert result is not None
        assert isinstance(result, list)

    def test_run_accepts_multiple_dictionaries(self):
        """Verify run method handles multiple dictionary inputs"""
        valid_input = [
            {'sentence': 'First sentence', 'topic': 'Topic one'},
            {'sentence': 'Second sentence', 'topic': 'Topic two'},
            {'sentence': 'Third sentence', 'topic': 'Topic three'}
        ]

        result = self.client.run(valid_input)
        assert result is not None
        assert isinstance(result, list)

    # TEST-003: Empty sentence validation
    def test_rejects_empty_sentences(self):
        """Verify system rejects empty sentences"""
        # Create input with empty sentence
        invalid_input = [{'sentence': '', 'topic': 'Test topic'}]

        # Call run method and expect error
        with pytest.raises(ValueError) as exc_info:
            self.client.run(invalid_input)

        # Verify error indicates validation failure
        assert 'sentence' in str(exc_info.value).lower()

    # TEST-004: Empty topic validation
    def test_rejects_empty_topics(self):
        """Verify system rejects empty topics"""
        # Create input with empty topic
        invalid_input = [{'sentence': 'Test sentence', 'topic': ''}]

        # Call run method and expect error
        with pytest.raises(ValueError) as exc_info:
            self.client.run(invalid_input)

        # Verify error indicates validation failure
        assert 'topic' in str(exc_info.value).lower()

    # TEST-005: Output format validation
    def test_output_is_list_of_numeric_scores(self):
        """Verify output is a list of numeric scores"""
        # Create valid input with 3 pairs
        input_data = [
            {'sentence': 'First argument about climate change', 'topic': 'climate change'},
            {'sentence': 'Second argument about renewable energy', 'topic': 'renewable energy'},
            {'sentence': 'Third argument about sustainability', 'topic': 'sustainability'}
        ]

        # Call run method
        result = self.client.run(input_data)

        # Verify return value is a list
        assert isinstance(result, list)

        # Verify list contains numeric values
        assert len(result) == 3
        for score in result:
            assert isinstance(score, (int, float))

        # Verify each value can be used in numeric comparisons
        assert all(score >= 0 for score in result)

    # TEST-006: Output length matches input length
    def test_output_length_matches_input_length(self):
        """Verify output length matches input length"""
        # Test with N=5
        input_data = [
            {'sentence': f'Sentence {i}', 'topic': f'Topic {i}'}
            for i in range(5)
        ]

        # Call run method
        result = self.client.run(input_data)

        # Verify output length equals input length
        assert len(result) == len(input_data)
        assert len(result) == 5

    def test_output_length_matches_input_length_various_sizes(self):
        """Test output length matches for various input sizes"""
        for n in [1, 3, 10, 20]:
            input_data = [
                {'sentence': f'Sentence {i}', 'topic': f'Topic {i}'}
                for i in range(n)
            ]
            result = self.client.run(input_data)
            assert len(result) == n

    # TEST-007: Output order corresponds to input order
    def test_output_order_corresponds_to_input_order(self):
        """Verify output order corresponds to input order"""
        # Create input with distinguishable pairs
        input_order_1 = [
            {'sentence': 'Climate change requires immediate action with comprehensive policies', 'topic': 'climate'},
            {'sentence': 'Simple short text', 'topic': 'topic'},
            {'sentence': 'Another detailed argument about environmental sustainability', 'topic': 'environment'}
        ]

        # Call run method and capture scores
        scores_1 = self.client.run(input_order_1)

        # Swap input order
        input_order_2 = [
            {'sentence': 'Simple short text', 'topic': 'topic'},
            {'sentence': 'Climate change requires immediate action with comprehensive policies', 'topic': 'climate'},
            {'sentence': 'Another detailed argument about environmental sustainability', 'topic': 'environment'}
        ]

        # Call run method again
        scores_2 = self.client.run(input_order_2)

        # Verify score positions moved with their corresponding pairs
        # scores_1[0] should equal scores_2[1] (first item moved to second position)
        # scores_1[1] should equal scores_2[0] (second item moved to first position)
        assert scores_1[0] == scores_2[1]
        assert scores_1[1] == scores_2[0]
        assert scores_1[2] == scores_2[2]

    # TEST-008: Single item batch processing
    def test_processes_single_item_correctly(self):
        """Verify system processes single item correctly"""
        # Create input with 1 pair
        input_data = [{'sentence': 'Test sentence', 'topic': 'Test topic'}]

        # Call run method
        result = self.client.run(input_data)

        # Verify returns list with 1 score
        assert isinstance(result, list)
        assert len(result) == 1

        # Verify processing completes successfully (score is numeric)
        assert isinstance(result[0], (int, float))

    # TEST-009: Multiple items batch processing
    def test_processes_multiple_items_correctly(self):
        """Verify system processes multiple items correctly"""
        # Create input with 10 pairs
        input_data = [
            {'sentence': f'Argument sentence number {i}', 'topic': f'Topic {i}'}
            for i in range(10)
        ]

        # Call run method
        result = self.client.run(input_data)

        # Verify returns list with 10 scores
        assert isinstance(result, list)
        assert len(result) == 10

        # Verify all items are processed (no missing scores)
        assert all(isinstance(score, (int, float)) for score in result)

    # TEST-010: Timeout parameter support
    def test_timeout_parameter_is_accepted(self):
        """Verify timeout parameter is accepted"""
        # Create valid input
        input_data = [{'sentence': 'Test sentence', 'topic': 'Test topic'}]

        # Call run method with timeout parameter
        result = self.client.run(input_data, timeout=30)

        # Verify method accepts timeout parameter without error
        assert result is not None

        # Verify processing completes
        assert isinstance(result, list)
        assert len(result) == 1

    # TEST-011: Factory pattern access
    def test_client_accessible_via_factory_pattern(self):
        """Verify client is accessible via factory pattern"""
        # Create factory instance with API key
        factory = DebaterApi("test_api_key")

        # Obtain ArgumentQualityClient through factory method
        client = factory.get_argument_quality_client()

        # Verify returned object is ArgumentQualityClient instance
        assert isinstance(client, ArgumentQualityClient)

        # Verify client is functional (can call run method)
        input_data = [{'sentence': 'Test sentence', 'topic': 'Test topic'}]
        result = client.run(input_data)
        assert isinstance(result, list)

    # TEST-012: Data transformation
    def test_dictionaries_transformed_correctly(self):
        """Verify dictionaries are transformed correctly for processing"""
        # Create input
        input_data = [
            {'sentence': 'S1', 'topic': 'T1'},
            {'sentence': 'S2', 'topic': 'T2'}
        ]

        # Call run method
        result = self.client.run(input_data)

        # Verify processing completes successfully
        assert result is not None

        # Verify output has 2 scores corresponding to 2 inputs
        assert len(result) == 2
        assert all(isinstance(score, (int, float)) for score in result)

    # TEST-013: Batch processing inheritance
    def test_client_inherits_batch_processing_capability(self):
        """Verify client inherits batch processing capability"""
        # Create instance
        client = ArgumentQualityClient("test_api_key")

        # Create input with multiple items (tests batch capability)
        input_data = [
            {'sentence': f'Sentence {i}', 'topic': f'Topic {i}'}
            for i in range(5)
        ]

        # Call run method
        result = client.run(input_data)

        # Verify batch processing works (all items processed)
        assert len(result) == 5
        assert all(isinstance(score, (int, float)) for score in result)

    # TEST-014: Service connectivity (mock implementation)
    def test_client_connects_to_scoring_service(self):
        """Verify client connects to scoring service"""
        # Create client with valid API key
        client = ArgumentQualityClient("valid_api_key")

        # Create valid input with recognizable sentence-topic pair
        input_data = [
            {'sentence': 'Autonomous vehicles reduce accidents', 'topic': 'autonomous vehicles'}
        ]

        # Call run method
        result = client.run(input_data)

        # Verify scores are returned (proves service connectivity)
        assert result is not None
        assert len(result) == 1

        # Verify scores are numeric quality values
        assert isinstance(result[0], (int, float))
        assert 0 <= result[0] <= 1.0

    # TEST-015: Single responsibility interface
    def test_client_provides_only_quality_scoring(self):
        """Verify client provides only quality scoring, not other services"""
        # Inspect ArgumentQualityClient public interface
        client = ArgumentQualityClient("test_api_key")

        # Verify run method exists for quality scoring
        assert hasattr(client, 'run')
        assert callable(client.run)

        # Verify no claim detection methods exist
        assert not hasattr(client, 'detect_claims')
        assert not hasattr(client, 'find_claims')

        # Verify no evidence detection methods exist
        assert not hasattr(client, 'detect_evidence')
        assert not hasattr(client, 'find_evidence')

        # The client should have minimal public interface
        public_methods = [m for m in dir(client) if not m.startswith('_') and callable(getattr(client, m))]
        assert 'run' in public_methods

    # TEST-016: Score differentiation
    def test_scores_differentiate_between_quality_levels(self):
        """Verify scores differentiate between quality levels"""
        # Create input with high-quality argument
        high_quality = {
            'sentence': 'Autonomous vehicles reduce traffic accidents by eliminating human error',
            'topic': 'autonomous vehicles'
        }

        # Create input with low-quality argument
        low_quality = {
            'sentence': 'cars cars cars',
            'topic': 'autonomous vehicles'
        }

        # Call run method with both inputs
        result = self.client.run([high_quality, low_quality])

        high_score = result[0]
        low_score = result[1]

        # Verify high-quality argument receives higher score
        assert high_score > low_score

        # Verify scores are sufficiently different to be meaningful
        assert high_score - low_score > 0.1  # At least 10% difference

    # TEST-017: Required keys enforcement
    def test_required_keys_enforced(self):
        """Verify required keys are enforced in input dictionaries"""
        # Create input missing 'sentence' key
        invalid_input = [{'topic': 'Test topic'}]

        # Attempt to call run method
        with pytest.raises(KeyError) as exc_info:
            self.client.run(invalid_input)

        # Verify error is raised for missing required key
        assert 'sentence' in str(exc_info.value).lower()

    def test_required_topic_key_enforced(self):
        """Verify topic key is required"""
        # Create input missing 'topic' key
        invalid_input = [{'sentence': 'Test sentence'}]

        # Attempt to call run method
        with pytest.raises(KeyError):
            self.client.run(invalid_input)

    # TEST-018: All pairs included in batch
    def test_batch_requests_contain_all_input_pairs(self):
        """Verify batch requests contain all input pairs"""
        # Create input with 5 distinct sentence-topic pairs
        input_data = [
            {'sentence': 'First unique sentence', 'topic': 'Topic A'},
            {'sentence': 'Second unique sentence', 'topic': 'Topic B'},
            {'sentence': 'Third unique sentence', 'topic': 'Topic C'},
            {'sentence': 'Fourth unique sentence', 'topic': 'Topic D'},
            {'sentence': 'Fifth unique sentence', 'topic': 'Topic E'}
        ]

        # Call run method
        result = self.client.run(input_data)

        # Verify all 5 pairs are processed (5 scores returned)
        assert len(result) == 5

        # Verify each score corresponds to its pair (order maintained)
        # All should be numeric
        assert all(isinstance(score, (int, float)) for score in result)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
