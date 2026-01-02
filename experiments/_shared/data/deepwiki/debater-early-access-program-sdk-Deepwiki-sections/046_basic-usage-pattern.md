<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Basic Usage Pattern -->
<!-- Lines: 2183-2212 -->

## Basic Usage Pattern

Most service clients follow a consistent usage pattern:

1. **Obtain client instance** through `DebaterApi` factory
2. **Prepare input data** in the required format
3. **Call the `run()` method** with appropriate parameters
4. **Process the returned results**

Example usage pattern:
```python
# Get client instance
debater_api = DebaterApi('YOUR_API_KEY')
client = debater_api.get_argument_quality_client()

# Prepare input data
sentence_topic_dicts = [
    {'sentence': 'Your sentence here', 'topic': 'Your topic here'}
]

# Run analysis
scores = client.run(sentence_topic_dicts)

# Process results
for score in scores:
    print(f"Score: {score}")  # Score between 0 and 1
```

Sources: [debater_python_api/integration_tests/api/clients/ServicesIT.py:28-44]()

