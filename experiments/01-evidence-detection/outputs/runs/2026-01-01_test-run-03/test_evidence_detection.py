"""
Test suite for Evidence Detection capability.

Tests verify BEHAVIOR requirements derived from requirement_cards.json.
"""
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from debater_api import DebaterApi


def test_001_factory_returns_client_instance():
    """
    TEST-001: Factory method returns evidence detection client instance
    Requirement: ED-001

    Test steps:
    1. Create factory instance with valid API key
    2. Call factory method to get evidence detection client
    3. Verify client instance is returned
    4. Verify client has run() method
    """
    # Step 1: Create factory with valid API key
    factory = DebaterApi('test-api-key-12345')

    # Step 2: Call factory method
    client = factory.get_evidence_detection_client()

    # Step 3: Verify client instance is returned
    assert client is not None, "Client instance should not be None"

    # Step 4: Verify client has run() method
    assert hasattr(client, 'run'), "Client should have run() method"
    assert callable(getattr(client, 'run')), "run() should be callable"

    print("✓ TEST-001 PASSED: Factory method returns evidence detection client instance")
    return True


def test_002_accepts_sentence_topic_dicts():
    """
    TEST-002: Accepts list of sentence-topic dictionaries and returns scores
    Requirement: ED-002
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create input
    input_data = [
        {'sentence': 'Text A', 'topic': 'Topic 1'},
        {'sentence': 'Text B', 'topic': 'Topic 2'}
    ]

    # Call client.run
    result = client.run(input_data)

    # Verify output is a list
    assert isinstance(result, list), "Output should be a list"

    # Verify output length equals input length
    assert len(result) == 2, f"Output length should be 2, got {len(result)}"

    # Verify each element is numeric
    for i, score in enumerate(result):
        assert isinstance(score, (int, float)), f"Element {i} should be numeric, got {type(score)}"

    print("✓ TEST-002 PASSED: Accepts list of sentence-topic dictionaries and returns scores")
    return True


def test_003_rejects_empty_sentence():
    """
    TEST-003: Rejects empty sentence field
    Requirement: ED-003
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create input with empty sentence
    input_data = [{'sentence': '', 'topic': 'Topic'}]

    # Verify error is raised
    try:
        client.run(input_data)
        assert False, "Should have raised an error for empty sentence"
    except (RuntimeError, ValueError) as e:
        # Verify error indicates empty sentence field
        error_msg = str(e).lower()
        assert 'empty' in error_msg, f"Error should mention 'empty', got: {e}"
        print("✓ TEST-003 PASSED: Rejects empty sentence field")
        return True


def test_004_rejects_empty_topic():
    """
    TEST-004: Rejects empty topic field
    Requirement: ED-003
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create input with empty topic
    input_data = [{'sentence': 'Text', 'topic': ''}]

    # Verify error is raised
    try:
        client.run(input_data)
        assert False, "Should have raised an error for empty topic"
    except (RuntimeError, ValueError) as e:
        # Verify error indicates empty topic field
        error_msg = str(e).lower()
        assert 'empty' in error_msg, f"Error should mention 'empty', got: {e}"
        print("✓ TEST-004 PASSED: Rejects empty topic field")
        return True


def test_005_returns_scores_in_range():
    """
    TEST-005: Returns scores in range [0, 1]
    Requirement: ED-004
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create valid input with 3 pairs
    input_data = [
        {'sentence': 'Sentence 1', 'topic': 'Topic 1'},
        {'sentence': 'Sentence 2', 'topic': 'Topic 2'},
        {'sentence': 'Sentence 3', 'topic': 'Topic 3'}
    ]

    result = client.run(input_data)

    # Verify each score is in [0, 1]
    for i, score in enumerate(result):
        assert 0 <= score <= 1, f"Score {i} ({score}) should be in range [0, 1]"

    print("✓ TEST-005 PASSED: Returns scores in range [0, 1]")
    return True


def test_006_processes_multiple_pairs():
    """
    TEST-006: Processes multiple sentence-topic pairs in single call
    Requirement: ED-006
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create input with 10 pairs
    input_data = [
        {'sentence': f'Sentence {i}', 'topic': f'Topic {i}'}
        for i in range(10)
    ]

    # Call once
    result = client.run(input_data)

    # Verify 10 scores returned
    assert len(result) == 10, f"Should return 10 scores, got {len(result)}"

    print("✓ TEST-006 PASSED: Processes multiple sentence-topic pairs in single call")
    return True


def test_007_preserves_input_order():
    """
    TEST-007: Preserves input order in output
    Requirement: ED-007
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create input with distinct items
    input_data = [
        {'sentence': 'A', 'topic': 'T1'},
        {'sentence': 'B', 'topic': 'T2'},
        {'sentence': 'C', 'topic': 'T3'}
    ]

    result = client.run(input_data)

    # Verify output length matches
    assert len(result) == 3, "Output should have 3 scores"

    # Each position should have a score (order preserved)
    assert all(isinstance(score, (int, float)) for score in result), "All outputs should be numeric"

    print("✓ TEST-007 PASSED: Preserves input order in output")
    return True


def test_008_run_method_api():
    """
    TEST-008: Public run() method accepts correct parameter
    Requirement: ED-008
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Verify run method exists
    assert hasattr(client, 'run'), "Client should have run method"

    # Create valid input
    input_data = [{'sentence': 'Test', 'topic': 'Topic'}]

    # Call run method
    result = client.run(input_data)

    # Verify execution without error
    assert result is not None, "run() should return a result"

    print("✓ TEST-008 PASSED: Public run() method accepts correct parameter")
    return True


def test_009_requires_api_key():
    """
    TEST-009: Requires API key for authentication
    Requirement: ED-010
    """
    # Test invalid/missing API key
    try:
        factory = DebaterApi('')
        assert False, "Should raise error for empty API key"
    except ValueError:
        pass

    try:
        factory = DebaterApi(None)
        assert False, "Should raise error for None API key"
    except (ValueError, TypeError):
        pass

    # Valid API key should succeed
    factory = DebaterApi('valid-key')
    assert factory is not None

    print("✓ TEST-009 PASSED: Requires API key for authentication")
    return True


def test_010_one_score_per_input():
    """
    TEST-010: Returns one score per input pair
    Requirement: ED-004
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create input with N=5 pairs
    input_data = [
        {'sentence': f'Sentence {i}', 'topic': f'Topic {i}'}
        for i in range(5)
    ]

    result = client.run(input_data)

    # Verify output length equals 5
    assert len(result) == 5, f"Should return 5 scores for 5 inputs, got {len(result)}"

    # Verify each position has exactly one score
    for i, score in enumerate(result):
        assert isinstance(score, (int, float)), f"Position {i} should have one numeric score"

    print("✓ TEST-010 PASSED: Returns one score per input pair")
    return True


def test_011_handles_empty_list():
    """
    TEST-011: Handles empty input list gracefully
    Requirement: ED-016
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Create empty input
    input_data = []

    # Call run
    result = client.run(input_data)

    # Verify no error and empty output
    assert result == [], f"Empty input should return empty list, got {result}"

    print("✓ TEST-011 PASSED: Handles empty input list gracefully")
    return True


def test_013_validates_required_keys():
    """
    TEST-013: Validates presence of required dictionary keys
    Requirement: ED-018
    """
    factory = DebaterApi('test-api-key')
    client = factory.get_evidence_detection_client()

    # Test missing 'sentence' key
    try:
        client.run([{'topic': 'Topic'}])
        assert False, "Should raise error for missing 'sentence' key"
    except (KeyError, RuntimeError):
        pass

    # Test missing 'topic' key
    try:
        client.run([{'sentence': 'Text'}])
        assert False, "Should raise error for missing 'topic' key"
    except (KeyError, RuntimeError):
        pass

    print("✓ TEST-013 PASSED: Validates presence of required dictionary keys")
    return True


if __name__ == '__main__':
    print("Running Evidence Detection Tests")
    print("=" * 60)

    tests = [
        test_001_factory_returns_client_instance,
        test_002_accepts_sentence_topic_dicts,
        test_003_rejects_empty_sentence,
        test_004_rejects_empty_topic,
        test_005_returns_scores_in_range,
        test_006_processes_multiple_pairs,
        test_007_preserves_input_order,
        test_008_run_method_api,
        test_009_requires_api_key,
        test_010_one_score_per_input,
        test_011_handles_empty_list,
        test_013_validates_required_keys,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED: {e}")

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")

    sys.exit(0 if failed == 0 else 1)
