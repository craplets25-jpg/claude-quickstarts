<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Testing and Debugging -->
<!-- Lines: 3244-3290 -->

## Testing and Debugging

### Request Dumping

For debugging failed requests, use the `dump_on_fail` parameter:

```python
response = self.do_run(payload, endpoint='/test', dump_on_fail=True)
```

This creates pickle files with complete request information that can be replayed using `run_client_from_dump()`.

### Retry Configuration

The `do_run()` method supports configurable retries:

```python
response = self.do_run(payload, retries=3, timeout=120)
```

### Progress Monitoring

Control progress display for debugging:

```python
client.set_show_process(False)  # Disable progress bars
```

**Sources:** [debater_python_api/api/clients/abstract_client.py:58-88](), [debater_python_api/api/clients/abstract_client.py:26-27]()20:T339e,# SDK Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [debater_python_api/api/clients/abstract_client.py](debater_python_api/api/clients/abstract_client.py)
- [debater_python_api/examples/keypoints_example.py](debater_python_api/examples/keypoints_example.py)
- [debater_python_api/integration_tests/api/clients/ServicesIT.py](debater_python_api/integration_tests/api/clients/ServicesIT.py)

</details>



This document describes the internal architecture of the Debater Early Access Program Python SDK, focusing on the core design patterns, client factory system, and service communication layer. This covers the foundational components that enable consistent interaction with IBM's Project Debater API services.

For specific client usage patterns and examples, see [Key Point Analysis](#3) and [Other NLP Services](#4). For error handling specifics, see [Error Handling](#5.2).

