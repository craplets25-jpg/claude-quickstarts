<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Architecture Overview -->
<!-- Lines: 2549-2609 -->

## Architecture Overview

The Claim and Evidence Detection system follows the standard client architecture pattern used throughout the SDK. Both detection clients inherit from a shared base class that provides common functionality for processing sentence-topic pairs.

### Client Class Hierarchy

```mermaid
graph TB
    AbstractClient["AbstractClient<br/>- Authentication<br/>- HTTP Communication<br/>- Batch Processing"]
    
    ClaimEvidenceDetectionClient["ClaimEvidenceDetectionClient<br/>- run()<br/>- Input validation<br/>- Batch processing"]
    
    ClaimDetectionClient["ClaimDetectionClient<br/>- host: claim-sentence.debater.res.ibm.com<br/>- Claim scoring"]
    
    EvidenceDetectionClient["EvidenceDetectionClient<br/>- host: motion-evidence.debater.res.ibm.com<br/>- Evidence scoring"]
    
    AbstractClient --> ClaimEvidenceDetectionClient
    ClaimEvidenceDetectionClient --> ClaimDetectionClient
    ClaimEvidenceDetectionClient --> EvidenceDetectionClient
```

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:1-37]()

### Service Integration

The clients communicate with IBM Debater services through REST APIs, processing sentence-topic pairs and returning confidence scores.

```mermaid
graph LR
    subgraph "Client Layer"
        ClaimClient["ClaimDetectionClient"]
        EvidenceClient["EvidenceDetectionClient"]
    end
    
    subgraph "Input Processing"
        SentenceTopicPairs["sentence_topic_dicts<br/>[{sentence, topic}, ...]"]
        ValidationLayer["Input Validation<br/>- Empty string check<br/>- Pair format validation"]
    end
    
    subgraph "External Services"
        ClaimService["claim-sentence.debater.res.ibm.com<br/>/score/"]
        EvidenceService["motion-evidence.debater.res.ibm.com<br/>/score/"]
    end
    
    subgraph "Output"
        ScoreResults["Confidence Scores<br/>- Claim probability<br/>- Evidence probability"]
    end
    
    SentenceTopicPairs --> ValidationLayer
    ValidationLayer --> ClaimClient
    ValidationLayer --> EvidenceClient
    
    ClaimClient --> ClaimService
    EvidenceClient --> EvidenceService
    
    ClaimService --> ScoreResults
    EvidenceService --> ScoreResults
```

**Sources:** [debater_python_api/api/clients/claim_and_evidence_detection_client.py:13-24](), [debater_python_api/api/clients/claim_and_evidence_detection_client.py:26-36]()

