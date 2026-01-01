<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: KpaResult Data Model -->
<!-- Lines: 1245-1307 -->

## KpaResult Data Model

The `KpaResult` class contains four primary data structures that represent different views of the analysis results:

| Component | Type | Purpose |
|-----------|------|---------|
| `result_json` | dict | Raw JSON response from the API |
| `result_df` | DataFrame | Detailed match-level results |
| `summary_df` | DataFrame | Key point summary statistics |
| `hierarchy_df` | DataFrame | Hierarchical relationship data |

**KpaResult Data Flow**
```mermaid
graph TD
    subgraph "Input Sources"
        JsonAPI["API JSON Response"]
        CsvFile["CSV File"]
    end
    
    subgraph "KpaResult Core"
        KpaResult["KpaResult Object"]
        ResultJson["result_json"]
        ResultDf["result_df"]
        SummaryDf["summary_df"]
        HierarchyDf["hierarchy_df"]
    end
    
    subgraph "Factory Methods"
        CreateFromJson["create_from_result_json()"]
        CreateFromCsv["create_from_result_csv()"]
    end
    
    subgraph "Processing Methods"
        JsonToDF["result_json_to_result_df()"]
        DfToSummary["result_df_to_summary_df()"]
        UpdateHierarchy["update_dataframes_with_hierarchical_results()"]
        DfToJson["result_df_to_result_json()"]
    end
    
    JsonAPI --> CreateFromJson
    CsvFile --> CreateFromCsv
    
    CreateFromJson --> KpaResult
    CreateFromCsv --> KpaResult
    
    KpaResult --> ResultJson
    KpaResult --> ResultDf
    KpaResult --> SummaryDf
    KpaResult --> HierarchyDf
    
    ResultJson --> JsonToDF
    JsonToDF --> ResultDf
    ResultDf --> DfToSummary
    DfToSummary --> SummaryDf
    ResultDf --> UpdateHierarchy
    SummaryDf --> UpdateHierarchy
    UpdateHierarchy --> HierarchyDf
    ResultDf --> DfToJson
    DfToJson --> ResultJson
```

Sources: [debater_python_api/api/clients/key_point_analysis/KpaResult.py:13-19]()

