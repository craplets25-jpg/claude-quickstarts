<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: API Reference -->
<!-- Lines: 2455-2490 -->

## API Reference

### Class: ArgumentQualityClient

#### Constructor

```python
ArgumentQualityClient(apikey)
```

**Parameters:**
- `apikey` (string): IBM API key for authentication

**Attributes:**
- `host`: Set to 'https://arg-quality.debater.res.ibm.com'

**Sources:** [debater_python_api/api/clients/argument_quality_client.py:8-11]()

#### Method: run

```python
run(sentence_topic_dicts, timeout=60)
```

**Parameters:**
- `sentence_topic_dicts` (list): List of dictionaries with 'sentence' and 'topic' keys
- `timeout` (int): Request timeout in seconds (default: 60)

**Returns:**
- List of quality scores corresponding to input pairs

**Raises:**
- `RuntimeError`: When input contains empty sentences or topics

**Sources:** [debater_python_api/api/clients/argument_quality_client.py:13-23]()

