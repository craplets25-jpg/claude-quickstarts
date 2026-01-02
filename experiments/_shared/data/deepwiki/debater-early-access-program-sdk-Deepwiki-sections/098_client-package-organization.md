<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Client Package Organization -->
<!-- Lines: 4610-4661 -->

## Client Package Organization

```mermaid
graph TB
    subgraph "debater_python_api.api.clients"
        AbstractClient["AbstractClient"]
        
        subgraph "Primary KPA Clients"
            KpAnalysisClient["KpAnalysisClient"]
            KpAnalysisAdminClient["KpAnalysisAdminClient"]
            KpAnalysisTaskFuture["KpAnalysisTaskFuture"]
        end
        
        subgraph "Text Analysis Clients"
            ArgumentQualityClient["ArgumentQualityClient"]
            ClaimDetectionClient["ClaimDetectionClient"]
            EvidenceDetectionClient["EvidenceDetectionClient"]
            ClusteringClient["ClusteringClient"]
            ClaimBoundariesClient["ClaimBoundariesClient"]
        end
        
        subgraph "Service Endpoints"
            KPAEndpoint["keypoint-matching-backend.debater.res.ibm.com"]
            ArgQualityEndpoint["arg-quality.debater.res.ibm.com"]
            ClaimDetectionEndpoint["claim-sentence.debater.res.ibm.com"]
            EvidenceEndpoint["motion-evidence.debater.res.ibm.com"]
            ClusteringEndpoint["clustering.debater.res.ibm.com"]
            BoundariesEndpoint["claim-boundaries.debater.res.ibm.com"]
        end
    end
    
    AbstractClient --> KpAnalysisClient
    AbstractClient --> KpAnalysisAdminClient
    AbstractClient --> ArgumentQualityClient
    AbstractClient --> ClaimDetectionClient
    AbstractClient --> EvidenceDetectionClient
    AbstractClient --> ClusteringClient
    AbstractClient --> ClaimBoundariesClient
    
    KpAnalysisClient --> KPAEndpoint
    KpAnalysisAdminClient --> KPAEndpoint
    ArgumentQualityClient --> ArgQualityEndpoint
    ClaimDetectionClient --> ClaimDetectionEndpoint
    EvidenceDetectionClient --> EvidenceEndpoint
    ClusteringClient --> ClusteringEndpoint
    ClaimBoundariesClient --> BoundariesEndpoint
```

**Client Inheritance and Service Mapping**: This diagram illustrates how all service clients inherit from `AbstractClient` and map to specific IBM Debater service endpoints.

*Sources: [debater_python_api/api/clients/__init__.py:1-1]()*

