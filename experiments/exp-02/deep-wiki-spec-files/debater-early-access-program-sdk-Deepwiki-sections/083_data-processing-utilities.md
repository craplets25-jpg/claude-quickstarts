<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Data Processing Utilities -->
<!-- Lines: 3913-3974 -->

## Data Processing Utilities

### CSV and DataFrame Operations

The data processing utilities handle conversion between different data formats:

```mermaid
graph TB
    subgraph "Input Sources"
        CSVFile["CSV Files"]
        DataFrame["pandas.DataFrame"]
    end
    
    subgraph "Core Functions"
        read_tups_from_csv["read_tups_from_csv()"]
        read_tups_from_df["read_tups_from_df()"]
        read_dicts_from_csv["read_dicts_from_csv()"]
        read_dicts_from_df["read_dicts_from_df()"]
    end
    
    subgraph "Transformation Layer"
        tups_to_dicts["tups_to_dicts()"]
        create_dict_to_list["create_dict_to_list()"]
    end
    
    subgraph "Output Formats"
        Tuples["List of Tuples"]
        Dicts["List of Dictionaries"]
        DictLists["Dictionary of Lists"]
    end
    
    CSVFile --> read_tups_from_csv
    DataFrame --> read_tups_from_df
    CSVFile --> read_dicts_from_csv
    DataFrame --> read_dicts_from_df
    
    read_tups_from_csv --> Tuples
    read_tups_from_df --> Tuples
    read_dicts_from_csv --> Dicts
    read_dicts_from_df --> Dicts
    
    Tuples --> tups_to_dicts
    tups_to_dicts --> Dicts
    Dicts --> create_dict_to_list
    create_dict_to_list --> DictLists
```

**Data Format Conversion Pipeline**

*Sources: [debater_python_api/api/clients/key_point_analysis/utils.py:9-41]()*

### Data Transformation Functions

| Function | Purpose | Input | Output |
|---|---|---|---|
| `create_dict_to_list()` | Convert tuples to grouped lists | `List[(key, value)]` | `Dict[key, List[value]]` |
| `read_tups_from_df()` | Extract tuples from DataFrame | `pandas.DataFrame` | `(tuples, columns)` |
| `tups_to_dicts()` | Convert tuples to dictionaries | `(tuples, columns)` | `List[Dict]` |
| `trunc_float()` | Truncate float precision | `(float, decimals)` | `float` |

*Sources: [debater_python_api/api/clients/key_point_analysis/utils.py:9-51]()*

