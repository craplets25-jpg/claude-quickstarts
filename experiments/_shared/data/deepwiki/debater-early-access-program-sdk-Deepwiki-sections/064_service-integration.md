<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Service Integration -->
<!-- Lines: 2898-2954 -->

## Service Integration

Both clients integrate with their respective IBM Debater services using the standard `AbstractClient` pattern:

```mermaid
graph TB
    subgraph "Client Layer"
        ClaimBoundariesClient["ClaimBoundariesClient"]
        ClusteringClient["ClusteringClient"]
    end
    
    subgraph "Service Layer"
        ClaimBoundariesEndpoint["claim-boundaries.debater.res.ibm.com/score/"]
        ClusteringEndpoint["clustering.debater.res.ibm.com/api/public/clustering"]
    end
    
    subgraph "Common Functionality"
        Authentication["API Key Authentication"]
        BatchProcessing["Batch Processing"]
        ErrorHandling["Error Handling"]
        Logging["Performance Logging"]
    end
    
    ClaimBoundariesClient --> ClaimBoundariesEndpoint
    ClusteringClient --> ClusteringEndpoint
    
    ClaimBoundariesClient --> Authentication
    ClaimBoundariesClient --> BatchProcessing
    ClaimBoundariesClient --> ErrorHandling
    ClaimBoundariesClient --> Logging
    
    ClusteringClient --> Authentication
    ClusteringClient --> BatchProcessing
    ClusteringClient --> ErrorHandling
    ClusteringClient --> Logging
```

Both clients inherit common functionality from `AbstractClient` including authentication, batch processing capabilities, and standardized error handling patterns.

**Sources:** [debater_python_api/api/clients/claim_boundaries_client.py:5-13](), [debater_python_api/api/clients/clustering_client.py:5-12]()1f:T2e82,# Development Guide

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [debater_python_api/api/clients/abstract_client.py](debater_python_api/api/clients/abstract_client.py)
- [debater_python_api/api/clients/key_point_analysis/KpaExceptions.py](debater_python_api/api/clients/key_point_analysis/KpaExceptions.py)

</details>



This document provides technical information for developers working with or extending the Debater Early Access Program SDK. It covers the internal architecture, error handling patterns, development utilities, and best practices for extending the SDK functionality.

The Development Guide focuses on implementation details and code organization. For basic usage and API documentation, see [Getting Started](#2) and [Key Point Analysis](#3). For detailed API reference, see [Reference](#6).

