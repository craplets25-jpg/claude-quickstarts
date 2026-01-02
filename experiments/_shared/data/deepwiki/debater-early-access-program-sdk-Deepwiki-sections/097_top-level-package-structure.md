<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Top-Level Package Structure -->
<!-- Lines: 4544-4609 -->

## Top-Level Package Structure

```mermaid
graph TB
    subgraph "debater_python_api"
        RootInit["__init__.py"]
        
        subgraph "api"
            APIInit["api/__init__.py"]
            DebaterAPIModule["debater_api.py"]
            
            subgraph "clients"
                ClientsInit["clients/__init__.py"]
                AbstractClientModule["abstract_client.py"]
                
                subgraph "Key Point Analysis"
                    KPAClient["kp_analysis_client.py"]
                    KPAAdminClient["kp_analysis_admin_client.py"]
                    KPATaskFuture["kp_analysis_task_future.py"]
                end
                
                subgraph "Other NLP Clients"
                    ArgQualityClient["argument_quality_client.py"]
                    ClaimDetectionClient["claim_detection_client.py"]
                    EvidenceDetectionClient["evidence_detection_client.py"]
                    ClusteringClient["clustering_client.py"]
                    ClaimBoundariesClient["claim_boundaries_client.py"]
                end
            end
        end
        
        subgraph "utils"
            UtilsInit["utils/__init__.py"]
            KPAUtils["kp_analysis_utils.py"]
            DataUtils["data_utils.py"]
            DocxGenerator["docx_generator.py"]
            LoggingUtils["logging_utils.py"]
        end
        
        subgraph "models"
            ModelsInit["models/__init__.py"]
            KPAResult["kpa_result.py"]
            KPAExceptions["kpa_exceptions.py"]
        end
    end
    
    RootInit --> APIInit
    RootInit --> UtilsInit
    RootInit --> ModelsInit
    
    APIInit --> DebaterAPIModule
    APIInit --> ClientsInit
    
    ClientsInit --> AbstractClientModule
    ClientsInit --> KPAClient
    ClientsInit --> ArgQualityClient
    
    AbstractClientModule --> KPAClient
    AbstractClientModule --> ArgQualityClient
    AbstractClientModule --> ClaimDetectionClient
```

**Package Structure Overview**: This diagram shows the hierarchical organization of the main package modules, with clear separation between API clients, utilities, and data models.

*Sources: [debater_python_api/__init__.py:1-1](), [debater_python_api/api/__init__.py:1-1](), [debater_python_api/api/clients/__init__.py:1-1]()*

