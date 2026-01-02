<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Entry Points and Public API -->
<!-- Lines: 4676-4715 -->

## Entry Points and Public API

```mermaid
graph LR
    subgraph "Public API Entry Points"
        UserCode["User Application Code"]
        
        subgraph "Primary Entry Points"
            DebaterApiFactory["DebaterApi.get_client()"]
            DirectImports["Direct Client Imports"]
            UtilityFunctions["Utility Functions"]
        end
        
        subgraph "Client Access Patterns"
            FactoryPattern["Factory Pattern Access"]
            DirectPattern["Direct Import Pattern"]
            UtilityPattern["Utility Pattern Access"]
        end
    end
    
    UserCode --> DebaterApiFactory
    UserCode --> DirectImports
    UserCode --> UtilityFunctions
    
    DebaterApiFactory --> FactoryPattern
    DirectImports --> DirectPattern
    UtilityFunctions --> UtilityPattern
    
    FactoryPattern --> "KpAnalysisClient"
    FactoryPattern --> "ArgumentQualityClient"
    
    DirectPattern --> "from debater_python_api.api.clients import KpAnalysisClient"
    
    UtilityPattern --> "from debater_python_api.utils import KpAnalysisUtils"
```

**API Entry Points**: This diagram shows the different ways users can access SDK functionality through factory methods, direct imports, or utility functions.

*Sources: [debater_python_api/__init__.py:1-1](), [debater_python_api/api/__init__.py:1-1]()*

