<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Error Handling and Monitoring -->
<!-- Lines: 1178-1240 -->

## Error Handling and Monitoring

The client provides several methods for monitoring system status and handling errors.

### Exception Types

| Exception | HTTP Status | Description |
|-----------|-------------|-------------|
| `KpaIllegalInputException` | 422 | Invalid request parameters |
| `KpaNoPrivilegesException` | 403 | Insufficient user privileges |
| `ConnectionError` | N/A | Network connectivity issues |

### Monitoring Methods

```python
# Check service health
status = kpa_client.run_self_check()
print(f"Service status: {status['status']}")  # UP or DOWN

# Get user report
report = kpa_client.get_full_report(days_ago=30)
print(f"Domains: {report['comments_status']}")
print(f"Jobs: {report['kp_analysis_status']}")

# Check comment limits
limits = kpa_client.get_comments_limit()
print(f"Comment limit: {limits['n_comments_limit']}")

# Get domain sentences
sentences = kpa_client.get_sentences_for_domain('my_domain')
```

### Job Management

```python
# Cancel specific job
kpa_client.cancel_kp_extraction_job('job_id')

# Cancel all jobs in domain
kpa_client.cancel_all_extraction_jobs_for_domain('my_domain')

# Cancel all jobs across all domains
kpa_client.cancel_all_extraction_jobs_all_domains()
```

Sources: [debater_python_api/api/clients/keypoints_client.py:326-342](), [debater_python_api/api/clients/keypoints_client.py:308-325](), [debater_python_api/api/clients/keypoints_client.py:265-288]()18:T285c,# Data Processing and Results

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [debater_python_api/api/clients/key_point_analysis/KpaResult.py](debater_python_api/api/clients/key_point_analysis/KpaResult.py)
- [debater_python_api/api/clients/key_point_analysis/utils.py](debater_python_api/api/clients/key_point_analysis/utils.py)

</details>



This page covers the data processing components and result handling capabilities of the Key Point Analysis system. It focuses on the `KpaResult` class and associated utilities that transform raw API responses into structured data formats suitable for analysis, export, and visualization.

For information about generating reports and visualizations from these results, see [Reporting and Visualization](#3.3). For details on the KPA client that produces these results, see [KPA Client Usage](#3.1).

