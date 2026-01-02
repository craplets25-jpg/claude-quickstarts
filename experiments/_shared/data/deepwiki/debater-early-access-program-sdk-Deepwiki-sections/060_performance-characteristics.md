<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Performance Characteristics -->
<!-- Lines: 2727-2752 -->

## Performance Characteristics

The clients include performance monitoring through timestamp logging:

- **Execution Time**: Measured from start to completion of the `run` method
- **Timeout Configuration**: 100-second timeout for service requests
- **Batch Processing**: Inherits efficient batch processing from `AbstractClient`

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:14](), [debater_python_api/api/clients/claim_and_evidence_detection_client.py:19-22]()1e:T2025,# Text Analysis Clients

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [debater_python_api/api/clients/claim_boundaries_client.py](debater_python_api/api/clients/claim_boundaries_client.py)
- [debater_python_api/api/clients/clustering_client.py](debater_python_api/api/clients/clustering_client.py)

</details>



This page documents the additional text analysis clients available in the Debater Python API SDK, specifically focusing on specialized NLP services for clustering and claim boundary detection. These clients provide complementary functionality to the core argument analysis services.

For argument quality scoring, see [Argument Quality Client](#4.1). For claim and evidence detection services, see [Claim and Evidence Detection](#4.2). For the primary Key Point Analysis functionality, see [Key Point Analysis](#3).

