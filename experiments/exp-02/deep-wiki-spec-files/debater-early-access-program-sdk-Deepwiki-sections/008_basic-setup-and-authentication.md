<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Basic Setup and Authentication -->
<!-- Lines: 323-360 -->

## Basic Setup and Authentication

### Creating the API Client

The primary entry point is the `DebaterApi` factory class, which provides access to all available service clients.

```python
from debater_python_api.api.debater_api import DebaterApi

# Initialize with your API key
debater_api = DebaterApi('YOUR_API_KEY_HERE')
```

### Authentication

All API calls require a valid API key. Replace `'YOUR_API_KEY_HERE'` with your actual API key from IBM's Debater Early Access Program.

**Client Architecture Overview**

```mermaid
graph TB
    APIKey["API Key"] --> DebaterApi["DebaterApi Factory"]
    DebaterApi --> KPAClient["get_keypoints_client()"]
    DebaterApi --> ArgQualityClient["get_argument_quality_client()"]
    DebaterApi --> ClaimClient["get_claim_detection_client()"]
    DebaterApi --> EvidenceClient["get_evidence_detection_client()"]
    DebaterApi --> ClusteringClient["get_clustering_client()"]
    DebaterApi --> OtherClients["Other Service Clients..."]
    
    KPAClient --> KPAService["keypoint-matching-backend.debater.res.ibm.com"]
    ArgQualityClient --> ArgService["arg-quality.debater.res.ibm.com"]
    ClaimClient --> ClaimService["claim-sentence.debater.res.ibm.com"]
    EvidenceClient --> EvidenceService["motion-evidence.debater.res.ibm.com"]
    ClusteringClient --> ClusterService["clustering.debater.res.ibm.com"]
```

Sources: [debater_python_api/examples/keypoints_example.py:4-5](), [debater_python_api/integration_tests/api/clients/ServicesIT.py:26]()

