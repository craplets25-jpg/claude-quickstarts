<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Job Submission and Execution -->
<!-- Lines: 981-1035 -->

## Job Submission and Execution

KPA jobs extract key points from comments and match sentences to those key points. Jobs run asynchronously and return a `KpAnalysisTaskFuture` for result retrieval.

### Job Parameters

The `run_params` dictionary controls job behavior:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keypoints` | List[str] | `[]` | Predefined key points for matching |
| `keypoints_by_job_id` | str | `None` | Use key points from previous job |
| `arg_min_len` | int | `4` | Minimum sentence length (tokens) |
| `arg_max_len` | int | `36` | Maximum sentence length (tokens) |
| `arg_relative_aq_threshold` | float | `1.0` | Argument quality percentile threshold |
| `mapping_policy` | str | `"NORMAL"` | Matching policy: "STRICT", "NORMAL", "LOOSE" |
| `sentence_to_multiple_kps` | bool | `False` | Allow sentence matching to multiple key points |
| `n_top_kps` | int | Auto | Number of key points to generate |
| `kp_relative_aq_threshold` | float | `0.65` | Key point quality percentile threshold |
| `invalid_kps_comment_ids` | List[str] | `[]` | Exclude comments from key point candidates |

### Starting Jobs

```python
# Start job with default parameters
future = kpa_client.start_kp_analysis_job('my_domain')

# Start job with custom parameters
run_params = {
    'arg_min_len': 5,
    'arg_max_len': 40,
    'mapping_policy': 'STRICT',
    'n_top_kps': 10
}

future = kpa_client.start_kp_analysis_job(
    domain='my_domain',
    run_params=run_params,
    description='Custom parameter analysis'
)

# Start job with predefined key points
run_params = {
    'keypoints': [
        'Cannabis affects memory and cognition',
        'Cannabis can be addictive',
        'Cannabis has medical benefits'
    ]
}

future = kpa_client.start_kp_analysis_job('my_domain', run_params=run_params)
```

Sources: [debater_python_api/api/clients/keypoints_client.py:168-211]()

