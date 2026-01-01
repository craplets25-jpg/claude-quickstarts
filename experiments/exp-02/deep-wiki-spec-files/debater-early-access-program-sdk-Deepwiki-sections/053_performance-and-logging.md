<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Performance and Logging -->
<!-- Lines: 2491-2510 -->

## Performance and Logging

### Execution Timing

The client includes built-in performance monitoring:

- Records start and end timestamps for each `run` call
- Logs execution time in milliseconds
- Uses Python's `datetime.datetime.now().timestamp()` for precision

### Logging Integration

The client integrates with Python's logging framework:

- Logs execution times at INFO level
- Format: 'argument_quality_client.run = {time}ms.'
- Enables performance monitoring and debugging

**Sources:** [debater_python_api/api/clients/argument_quality_client.py:14, 20-21]()

