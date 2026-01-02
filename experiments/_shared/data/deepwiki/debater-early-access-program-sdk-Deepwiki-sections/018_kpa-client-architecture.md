<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: KPA Client Architecture -->
<!-- Lines: 812-864 -->

## KPA Client Architecture

```mermaid
graph TD
    subgraph "Client Layer"
        DebaterApi["DebaterApi Factory"]
        KpAnalysisClient["KpAnalysisClient"]
        AbstractClient["AbstractClient"]
    end
    
    subgraph "Core Operations"
        CreateDomain["create_domain()"]
        UploadComments["upload_comments()"]
        StartJob["start_kp_analysis_job()"]
        GetStatus["get_kp_extraction_job_status()"]
        SimpleRun["run()"]
    end
    
    subgraph "Task Management"
        KpAnalysisTaskFuture["KpAnalysisTaskFuture"]
        GetResult["get_result()"]
        Cancel["cancel()"]
    end
    
    subgraph "Service Endpoints"
        DomainsEndpoint["/domains"]
        CommentsEndpoint["/comments"]
        KpExtractionEndpoint["/kp_extraction"]
        DataEndpoint["/data"]
        ReportEndpoint["/report"]
    end
    
    DebaterApi --> KpAnalysisClient
    AbstractClient --> KpAnalysisClient
    
    KpAnalysisClient --> CreateDomain
    KpAnalysisClient --> UploadComments
    KpAnalysisClient --> StartJob
    KpAnalysisClient --> GetStatus
    KpAnalysisClient --> SimpleRun
    
    StartJob --> KpAnalysisTaskFuture
    KpAnalysisTaskFuture --> GetResult
    KpAnalysisTaskFuture --> Cancel
    
    CreateDomain --> DomainsEndpoint
    UploadComments --> CommentsEndpoint
    StartJob --> KpExtractionEndpoint
    GetStatus --> KpExtractionEndpoint
```

Sources: [debater_python_api/api/clients/keypoints_client.py:23-36](), [debater_python_api/api/clients/keypoints_client.py:345-359]()

