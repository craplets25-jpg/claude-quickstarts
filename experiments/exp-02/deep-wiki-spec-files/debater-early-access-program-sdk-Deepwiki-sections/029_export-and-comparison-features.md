<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Export and Comparison Features -->
<!-- Lines: 1447-1480 -->

## Export and Comparison Features

### File Export

The system supports exporting results to CSV files in multiple formats:

```python
# Export all DataFrames
result.write_to_file("analysis_results.csv", also_hierarchy=True)
```

This creates three files:
- `analysis_results.csv` - Detailed match results
- `analysis_results_kps_summary.csv` - Key point summary
- `analysis_results_kps_hierarchy.csv` - Hierarchical relationships

Sources: [debater_python_api/api/clients/key_point_analysis/KpaResult.py:203-216]()

### Result Comparison

The `compare_with_other` method enables comparison between different analysis results:

```python
comparison_df = result1.compare_with_other(result2)
```

The comparison DataFrame includes:
- Key points present in both results
- Sentence counts and percentages for each result
- Change metrics between results
- Key points unique to each result

Sources: [debater_python_api/api/clients/key_point_analysis/KpaResult.py:320-356]()

