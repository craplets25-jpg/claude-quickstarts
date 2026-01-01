<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Project Metadata -->
<!-- Lines: 4272-4332 -->

## Project Metadata

The SDK is configured as a Python package named `debater_python_api` with comprehensive metadata defined in the project configuration. The package follows modern Python packaging standards using the `pyproject.toml` configuration format.

**Project Configuration Structure**

```mermaid
graph TB
    subgraph "pyproject.toml"
        BuildSystem["[build-system]<br/>Build configuration"]
        ProjectMeta["[project]<br/>Package metadata"]
        OptionalDeps["[project.optional-dependencies]<br/>Development dependencies<br/>(commented)"]
        ProjectUrls["[project.urls]<br/>Project links<br/>(commented)"]
        ProjectScripts["[project.scripts]<br/>Console scripts<br/>(commented)"]
    end
    
    subgraph "Build System Components"
        Setuptools["setuptools>=61.0.0"]
        Wheel["wheel"]
        BuildBackend["setuptools.build_meta"]
    end
    
    subgraph "Project Identity"
        Name["debater_python_api"]
        Version["4.3.2"]
        Description["Project Debater Early Access Program API sdk for python"]
        ReadmeFile["README.md"]
        LicenseFile["LICENSE"]
    end
    
    subgraph "Author Information"
        AuthorName["Elad Venezian"]
        AuthorEmail["eladv@il.ibm.com"]
    end
    
    BuildSystem --> Setuptools
    BuildSystem --> Wheel
    BuildSystem --> BuildBackend
    
    ProjectMeta --> Name
    ProjectMeta --> Version
    ProjectMeta --> Description
    ProjectMeta --> ReadmeFile
    ProjectMeta --> LicenseFile
    ProjectMeta --> AuthorName
    ProjectMeta --> AuthorEmail
```

The core project metadata includes:

| Configuration | Value | Description |
|---------------|-------|-------------|
| Package Name | `debater_python_api` | Python package identifier |
| Version | `4.3.2` | Current release version |
| Description | Project Debater Early Access Program API sdk for python | Package summary |
| Author | Elad Venezian (eladv@il.ibm.com) | Package maintainer |
| License | File-based (LICENSE) | License reference |
| README | README.md | Package documentation |

Sources: [pyproject.toml:7-17]()

