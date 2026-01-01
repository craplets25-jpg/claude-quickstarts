<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Client Classes -->
<!-- Lines: 2610-2653 -->

## Client Classes

### ClaimEvidenceDetectionClient

The base class `ClaimEvidenceDetectionClient` provides shared functionality for both claim and evidence detection. It inherits from `AbstractClient` and implements the core `run` method.

| Method | Parameters | Description |
|--------|------------|-------------|
| `__init__` | `apikey` | Initializes the client with API key authentication |
| `run` | `sentence_topic_dicts` | Processes sentence-topic pairs and returns confidence scores |

The `run` method performs the following operations:

1. **Input Validation**: Checks that neither sentence nor topic fields are empty
2. **Data Transformation**: Converts dictionary format to list of pairs
3. **Batch Processing**: Uses inherited `run_in_batch` method
4. **Performance Logging**: Records execution time

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:9-24]()

### ClaimDetectionClient

The `ClaimDetectionClient` specializes in identifying claims within text. It inherits from `ClaimEvidenceDetectionClient` and configures the service endpoint for claim detection.

```python
# Configuration
host = 'https://claim-sentence.debater.res.ibm.com'
endpoint = '/score/'
```

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:26-29]()

### EvidenceDetectionClient

The `EvidenceDetectionClient` focuses on detecting evidence within text. It inherits from `AbstractClient` directly and configures the service endpoint for evidence detection.

```python
# Configuration  
host = 'https://motion-evidence.debater.res.ibm.com'
endpoint = '/score/'
```

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:32-35]()

