<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Console Output and Reporting -->
<!-- Lines: 1545-1570 -->

## Console Output and Reporting

The `KpAnalysisUtils` class provides methods for displaying KPA results and reports directly to the console with formatted output and logging.

### User Report Display

The `print_report()` method displays comprehensive user account information including domain status and job history:

```python
KpAnalysisUtils.print_report(user_report)
```

This outputs structured information about domain statuses, data processing status, and key point analysis job history with detailed logging.

### Result Console Output

The `print_result()` method provides formatted console display of KPA results:

```python
KpAnalysisUtils.print_result(result_json, n_sentences_per_kp=5, title="Analysis Results")
```

This leverages the `KpaResult` class to display key points with their matching sentences in a readable console format.

**Sources:** [debater_python_api/api/clients/key_point_analysis/KpAnalysisUtils.py:18-37](), [debater_python_api/api/clients/key_point_analysis/KpAnalysisUtils.py:75-77]()

