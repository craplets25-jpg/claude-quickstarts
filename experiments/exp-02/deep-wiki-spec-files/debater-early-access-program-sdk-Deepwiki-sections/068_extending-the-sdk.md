<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Extending the SDK -->
<!-- Lines: 3200-3243 -->

## Extending the SDK

### Creating New Service Clients

To add a new service client:

1. **Inherit from AbstractClient:**
   ```python
   class NewServiceClient(AbstractClient):
       def __init__(self, apikey):
           super().__init__(apikey)
           self.host = 'https://new-service.debater.res.ibm.com'
   ```

2. **Implement service-specific methods:**
   - Use `self.do_run()` for single requests
   - Use `self.run_in_batch()` for bulk operations
   - Handle service-specific response parsing

3. **Add to DebaterApi factory:**
   ```python
   def get_new_service_client(self):
       return NewServiceClient(self.apikey)
   ```

### Best Practices

1. **Error Handling:**
   - Use custom exceptions for domain-specific errors
   - Let `ConnectionError` bubble up for network issues
   - Implement proper retry logic for transient failures

2. **Batch Processing:**
   - Use `run_in_batch()` for processing large datasets
   - Configure appropriate batch sizes based on service limits
   - Handle empty strings with placeholder replacement

3. **Progress Tracking:**
   - Enable progress bars for long-running operations
   - Use descriptive class names for progress indicators
   - Allow users to disable progress tracking

**Sources:** [debater_python_api/api/clients/abstract_client.py:19-118]()

