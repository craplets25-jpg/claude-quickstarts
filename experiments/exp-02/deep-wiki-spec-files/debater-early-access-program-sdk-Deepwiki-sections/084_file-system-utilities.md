<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: File System Utilities -->
<!-- Lines: 3975-4014 -->

## File System Utilities

### Directory Operations

The `get_all_files_in_dir()` function retrieves all files from a directory:

```mermaid
graph LR
    Path["Directory Path"] --> listdir["os.listdir()"]
    listdir --> JoinPaths["os.path.join()"]
    JoinPaths --> FilterFiles["Filter isfile()"]
    FilterFiles --> FileList["List of File Paths"]
```

**Directory File Listing Process**

*Sources: [debater_python_api/api/clients/key_point_analysis/utils.py:53-56]()*

### File Writing Operations

The `write_df_to_file()` function handles DataFrame persistence:

```mermaid
graph TD
    DataFrame["pandas.DataFrame"] --> write_df_to_file["write_df_to_file()"]
    FilePath["Target File Path"] --> write_df_to_file
    
    write_df_to_file --> CheckDir{"Directory Exists?"}
    CheckDir -->|No| CreateDir["os.makedirs()"]
    CheckDir -->|Yes| WriteFile["df.to_csv()"]
    CreateDir --> WriteFile
    WriteFile --> LogInfo["logging.info()"]
```

**DataFrame File Writing Process**

The function ensures target directories exist before writing CSV files, creating them if necessary.

*Sources: [debater_python_api/api/clients/key_point_analysis/utils.py:58-64]()*

