<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Input and Output Formats -->
<!-- Lines: 2654-2681 -->

## Input and Output Formats

### Input Format

Both clients accept input in the form of `sentence_topic_dicts`, which is a list of dictionaries with the following structure:

```python
sentence_topic_dicts = [
    {
        'sentence': 'Text to analyze for claims/evidence',
        'topic': 'Related topic or context'
    },
    # Additional sentence-topic pairs...
]
```

The system validates that:
- Neither `sentence` nor `topic` fields are empty strings
- Each dictionary contains both required fields

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:15-18]()

### Output Format

The clients return confidence scores from the respective services. The exact format depends on the service implementation, but typically includes numerical confidence values indicating the likelihood that the input text contains claims or evidence.

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:19-24]()

