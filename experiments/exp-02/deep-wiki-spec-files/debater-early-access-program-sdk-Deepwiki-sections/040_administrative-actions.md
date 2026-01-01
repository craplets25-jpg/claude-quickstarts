<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Administrative Actions -->
<!-- Lines: 1961-1991 -->

## Administrative Actions

Administrative actions provide system control capabilities through the `/admin_action` endpoint.

### User Management Actions

| Function | Parameters | Description |
|----------|------------|-------------|
| `admin_action_delete_user()` | `user_id: str` | Permanently deletes a user and all associated data |
| `admin_action_delete_user_domain()` | `user_id: str`, `domain: str` | Deletes a specific domain for a user |
| `admin_action_set_user_limit()` | `user_id: str`, `user_limit: int` | Sets processing limits for a user |

**Sources:** [debater_python_api/api/clients/keypoints_admin_client.py:76-132]()

### Job Management Actions

| Function | Parameters | Description |
|----------|------------|-------------|
| `admin_action_cancel_job()` | `job_id: str` | Cancels a specific job |
| `admin_action_cancel_all_jobs()` | None | Cancels all running jobs system-wide |
| `admin_action_cancel_all_jobs_by_user()` | `user_id: str` | Cancels all jobs for a specific user |
| `admin_action_cancel_all_jobs_by_domain()` | `user_id: str`, `domain: str` | Cancels all jobs for a user's domain |

**Sources:** [debater_python_api/api/clients/keypoints_admin_client.py:99-125]()

### Domain Cleanup Actions

The `admin_action_delete_old_domains_by_date()` function provides automated cleanup of domains older than a specified date, using `datetime` objects for precise control.

**Sources:** [debater_python_api/api/clients/keypoints_admin_client.py:90-97]()

