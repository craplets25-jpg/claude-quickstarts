<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Service Endpoint Mapping -->
<!-- Lines: 2134-2182 -->

## Service Endpoint Mapping

The following diagram shows the mapping between client classes and their corresponding service endpoints:

```mermaid
graph LR
    subgraph "Client Classes"
        ArgumentQualityClient["ArgumentQualityClient"]
        ClaimDetectionClient["ClaimDetectionClient"]
        EvidenceDetectionClient["EvidenceDetectionClient"]
        ClaimBoundariesClient["ClaimBoundariesClient"]
        ClusteringClient["ClusteringClient"]
        ProConClient["ProConClient"]
        NarrativeGenerationClient["NarrativeGenerationClient"]
        TermRelaterClient["TermRelaterClient"]
        TermWikifierClient["TermWikifierClient"]
        ThemeExtractionClient["ThemeExtractionClient"]
        IndexSearcherClient["IndexSearcherClient"]
    end
    
    subgraph "Service Endpoints"
        ArgQualityEndpoint["arg-quality.debater.res.ibm.com<br/>/score/"]
        ClaimDetectionEndpoint["claim-sentence.debater.res.ibm.com"]
        EvidenceDetectionEndpoint["motion-evidence.debater.res.ibm.com"]
        ClaimBoundariesEndpoint["claim-boundaries.debater.res.ibm.com"]
        ClusteringEndpoint["clustering.debater.res.ibm.com"]
        ProConEndpoint["pro-con service endpoint"]
        NarrativeEndpoint["narrative generation endpoint"]
        TermRelaterEndpoint["term relater endpoint"]
        TermWikifierEndpoint["term wikifier endpoint"]
        ThemeExtractionEndpoint["theme extraction endpoint"]
        IndexSearcherEndpoint["index searcher endpoint"]
    end
    
    ArgumentQualityClient --> ArgQualityEndpoint
    ClaimDetectionClient --> ClaimDetectionEndpoint
    EvidenceDetectionClient --> EvidenceDetectionEndpoint
    ClaimBoundariesClient --> ClaimBoundariesEndpoint
    ClusteringClient --> ClusteringEndpoint
    ProConClient --> ProConEndpoint
    NarrativeGenerationClient --> NarrativeEndpoint
    TermRelaterClient --> TermRelaterEndpoint
    TermWikifierClient --> TermWikifierEndpoint
    ThemeExtractionClient --> ThemeExtractionEndpoint
    IndexSearcherClient --> IndexSearcherEndpoint
```

Sources: [debater_python_api/api/clients/argument_quality_client.py:6-11](), [debater_python_api/integration_tests/api/clients/ServicesIT.py:28-238]()

