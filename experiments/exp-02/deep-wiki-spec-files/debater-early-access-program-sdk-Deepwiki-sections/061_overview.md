<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Overview -->
<!-- Lines: 2753-2793 -->

## Overview

The text analysis clients provide specialized natural language processing capabilities that extend beyond the core debating services. These clients follow the same architectural patterns as other SDK clients, inheriting from `AbstractClient` and providing standardized interfaces for their respective services.

### Text Analysis Client Architecture

```mermaid
graph TB
    subgraph "AbstractClient Base"
        AbstractClient["AbstractClient<br/>- Authentication<br/>- HTTP Communication<br/>- Batch Processing"]
    end
    
    subgraph "Text Analysis Clients"
        ClaimBoundariesClient["ClaimBoundariesClient<br/>- Claim span detection<br/>- Boundary identification"]
        ClusteringClient["ClusteringClient<br/>- Sentence clustering<br/>- Configurable algorithms"]
    end
    
    subgraph "External Services"
        ClaimBoundariesService["claim-boundaries.debater.res.ibm.com<br/>/score/"]
        ClusteringService["clustering.debater.res.ibm.com<br/>/api/public/clustering"]
    end
    
    subgraph "Configuration Options"
        TextPreprocessing["text_preprocessing<br/>- stemming<br/>- lemmatization<br/>- wikifier"]
        EmbeddingMethod["embedding_method<br/>- tf<br/>- ifidf<br/>- concepts<br/>- glove<br/>- bert_ft_concat"]
        ClusteringMethod["clustering_method<br/>- kmeans<br/>- skmeans_euclidean<br/>- sib"]
    end
    
    AbstractClient --> ClaimBoundariesClient
    AbstractClient --> ClusteringClient
    
    ClaimBoundariesClient --> ClaimBoundariesService
    ClusteringClient --> ClusteringService
    
    ClusteringClient --> TextPreprocessing
    ClusteringClient --> EmbeddingMethod
    ClusteringClient --> ClusteringMethod
```

**Sources:** [debater_python_api/api/clients/claim_boundaries_client.py:1-22](), [debater_python_api/api/clients/clustering_client.py:1-113]()

