<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Hierarchical Representations -->
<!-- Lines: 1680-1721 -->

## Hierarchical Representations

The system provides multiple ways to represent key point hierarchies as text and structured data.

### Textual Bullet Format

The `hierarchical_graph_data_to_textual_bullets()` method creates indented bullet point representations:

```python
bullets = KpAnalysisUtils.hierarchical_graph_data_to_textual_bullets(
    graph_data=hierarchical_data,
    out_file="hierarchy_bullets.txt"
)
```

This generates hierarchical text with indentation levels representing parent-child relationships and match counts for each key point.

### Comprehensive Report Generation

The `generate_graphs_and_textual_summary()` method creates all visualization formats:

```python
KpAnalysisUtils.generate_graphs_and_textual_summary(
    result_file="results.csv",
    min_n_similar_matches_in_graph=5,
    n_top_matches_in_graph=20,
    filter_min_relations_for_text=0.4,
    n_top_matches_in_docx=50,
    include_match_score_in_docx=False,
    min_n_matches_in_docx=5,
    save_only_docx=False
)
```

This generates four output files:
- `*_graph_data.json`: Full graph data for visualization tools
- `*_hierarchical_graph_data.json`: Simplified hierarchical graph
- `*_hierarchical_bullets.txt`: Text bullet representation
- `*_hierarchical.docx`: Formatted DOCX report

**Sources:** [debater_python_api/api/clients/key_point_analysis/KpAnalysisUtils.py:267-310](), [debater_python_api/api/clients/key_point_analysis/KpAnalysisUtils.py:313-377]()

