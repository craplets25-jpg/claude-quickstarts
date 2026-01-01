<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Service Integration -->
<!-- Lines: 2511-2548 -->

## Service Integration

### Endpoint Configuration

The client connects to IBM's argument quality service:

- **Host**: `https://arg-quality.debater.res.ibm.com`
- **Endpoint**: `/score/`
- **Method**: Inherited batch processing via `AbstractClient`

### Service Inheritance

The client inherits core functionality from `AbstractClient`:

- HTTP communication handling
- Authentication management
- Batch processing capabilities
- Error handling and retry logic

**Sources:** [debater_python_api/api/clients/argument_quality_client.py:4, 6, 11, 19]()1d:T1f94,# Claim and Evidence Detection

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [debater_python_api/api/clients/claim_and_evidence_detection_client.py](debater_python_api/api/clients/claim_and_evidence_detection_client.py)

</details>



This document covers the Claim and Evidence Detection clients in the Debater SDK. These clients provide functionality for identifying claims and evidence within text by scoring sentence-topic pairs against specialized NLP models.

The system consists of two main clients: `ClaimDetectionClient` for identifying claims and `EvidenceDetectionClient` for detecting evidence. Both clients share a common base architecture and API pattern while targeting different IBM Debater services.

For information about the primary Key Point Analysis system, see [Key Point Analysis](#3). For other NLP service clients, see [Text Analysis Clients](#4.3).

