<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Working with Results -->
<!-- Lines: 1404-1446 -->

## Working with Results

### Creating KpaResult Objects

The system provides two factory methods for creating `KpaResult` objects:

```python
# From API JSON response
result = KpaResult.create_from_result_json(json_response, name="analysis_1")

# From CSV file
result = KpaResult.create_from_result_csv("results.csv", name="analysis_1")
```

Sources: [debater_python_api/api/clients/key_point_analysis/KpaResult.py:185-193](), [debater_python_api/api/clients/key_point_analysis/KpaResult.py:195-201]()

### Data Access and Analysis

The `KpaResult` object provides methods for accessing and analyzing the processed data:

```python
# Get sentence counts
total_sentences = result.get_number_of_unique_sentences(include_unmatched=True)
matched_sentences = result.get_number_of_unique_sentences(include_unmatched=False)

# Get key point statistics
kp_stats = result.get_kp_to_n_matched_sentences(include_none=False)
```

Sources: [debater_python_api/api/clients/key_point_analysis/KpaResult.py:297-318]()

### Console Output

The `print_result` method provides formatted console output with hierarchical display:

```python
result.print_result(n_sentences_per_kp=5, title="Analysis Results")
```

This method handles hierarchical key point relationships and displays coverage statistics.

Sources: [debater_python_api/api/clients/key_point_analysis/KpaResult.py:218-292]()

