<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Utility Module Organization -->
<!-- Lines: 4015-4043 -->

## Utility Module Organization

The SDK organizes utilities across two main modules:

| Module | Purpose | Key Functions |
|---|---|---|
| `debater_python_api.utils.kp_analysis_utils` | Display and reporting utilities | `print_kps_summary`, `print_report`, `print_progress_bar` |
| `debater_python_api.api.clients.key_point_analysis.utils` | Data processing utilities | `read_dicts_from_csv`, `write_df_to_file`, `create_dict_to_list` |

Both modules use standard libraries including `logging`, `os`, `pathlib`, and `pandas` for their operations.

*Sources: [debater_python_api/utils/kp_analysis_utils.py:1-4](), [debater_python_api/api/clients/key_point_analysis/utils.py:1-7]()*23:T1ba0,# Reference

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [Release](Release)
- [pyproject.toml](pyproject.toml)

</details>



This document provides detailed reference information for the Debater Early Access Program SDK, including project configuration, dependencies, build settings, and release notes. This serves as the authoritative source for technical specifications and metadata about the SDK package.

For information about the SDK's internal architecture and development patterns, see [SDK Architecture](#5.1). For package organization and module structure, see [Package Structure](#6.2).

