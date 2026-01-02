<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Admin Client Overview -->
<!-- Lines: 1823-1877 -->

## Admin Client Overview

The `KpAnalysisAdminClient` provides administrative control over the Key Point Analysis service through two main endpoint categories: reporting and actions. It requires special authentication credentials beyond the standard API key.

### Admin Client Architecture

```mermaid
graph TB
    subgraph "Client Hierarchy"
        KpAnalysisClient["KpAnalysisClient<br/>(Base Client)"]
        KpAnalysisAdminClient["KpAnalysisAdminClient<br/>(Admin Extension)"]
    end
    
    subgraph "Authentication"
        APIKey["apikey<br/>(Standard Auth)"]
        AdminPassword["admin_password<br/>(Admin Auth)"]
    end
    
    subgraph "Admin Endpoints"
        AdminReports["/admin_report<br/>(admin_reports_endpoint)"]
        AdminActions["/admin_action<br/>(admin_actions_endpoint)"]
    end
    
    subgraph "Report Types"
        DomainStatuses["domain_statuses"]
        JobStatuses["job_statuses_by_days<br/>job_statuses_by_dates<br/>not_finished_job_statuses"]
        CommentBatches["comment_batches_statuses"]
        CommentsStats["comments_stats"]
    end
    
    subgraph "Action Types"
        UserActions["delete_user<br/>delete_user_domain<br/>set_user_limit"]
        JobActions["cancel_job<br/>cancel_all_jobs<br/>cancel_all_jobs_by_user<br/>cancel_all_jobs_by_domain"]
        DomainActions["delete_old_domains"]
    end
    
    KpAnalysisClient --> KpAnalysisAdminClient
    APIKey --> KpAnalysisAdminClient
    AdminPassword --> KpAnalysisAdminClient
    
    KpAnalysisAdminClient --> AdminReports
    KpAnalysisAdminClient --> AdminActions
    
    AdminReports --> DomainStatuses
    AdminReports --> JobStatuses
    AdminReports --> CommentBatches
    AdminReports --> CommentsStats
    
    AdminActions --> UserActions
    AdminActions --> JobActions
    AdminActions --> DomainActions
```

**Sources:** [debater_python_api/api/clients/keypoints_admin_client.py:1-133]()

