<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Usage -->
<!-- Lines: 2424-2454 -->

## Usage

### Basic Usage Pattern

The client follows a straightforward pattern for scoring sentence-topic pairs:

1. Initialize the client with an API key
2. Prepare sentence-topic pairs as dictionaries
3. Call the `run` method with the pairs
4. Process the returned quality scores

### Input Validation

The client performs validation on input data:

- Empty sentences raise `RuntimeError`
- Empty topics raise `RuntimeError`
- Each pair must contain both 'sentence' and 'topic' keys

**Sources:** [debater_python_api/api/clients/argument_quality_client.py:15-17]()

### Batch Processing

The client leverages the inherited `run_in_batch` method from `AbstractClient` to process multiple sentence-topic pairs efficiently. The data is formatted as:

- `list_name`: 'sentence_topic_pairs'
- `list`: Array of [sentence, topic] pairs
- `endpoint`: '/score/'

**Sources:** [debater_python_api/api/clients/argument_quality_client.py:18-19]()

