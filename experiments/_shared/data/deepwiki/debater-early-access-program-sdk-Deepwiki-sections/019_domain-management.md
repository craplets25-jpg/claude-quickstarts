<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Domain Management -->
<!-- Lines: 865-903 -->

## Domain Management

Domains are workspaces for organizing comments and KPA jobs. Each domain can be configured with specific processing parameters.

### Creating Domains

```python
# Create domain with default parameters
kpa_client.create_domain('my_domain')

# Create domain with custom parameters
domain_params = {
    'dont_split': True,          # Keep comments as-is without sentence splitting
    'do_stance_analysis': True,  # Calculate stance for sentences
    'do_kp_quality': True        # Calculate keypoint quality scores
}
kpa_client.create_domain('my_domain', domain_params)
```

### Domain Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dont_split` | bool | `False` | Skip comment cleaning and sentence splitting |
| `do_stance_analysis` | bool | `False` | Calculate stance (positive/negative/neutral/suggestion) |
| `do_kp_quality` | bool | `False` | Calculate keypoint quality scores |

### Domain Cleanup

```python
# Delete specific domain
kpa_client.delete_domain_cannot_be_undone('my_domain')

# Delete all domains
kpa_client.delete_all_domains_cannot_be_undone()
```

Sources: [debater_python_api/api/clients/keypoints_client.py:88-107](), [debater_python_api/api/clients/keypoints_client.py:290-306]()

