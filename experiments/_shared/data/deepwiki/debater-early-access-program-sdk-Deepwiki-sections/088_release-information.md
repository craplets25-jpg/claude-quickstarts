<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Release Information -->
<!-- Lines: 4158-4233 -->

## Release Information

### Current Version: 4.3.2

The current release introduces SSL certificate verification control for enhanced security configuration in enterprise environments.

#### Key Changes in 4.3.2

- **Certificate Verification Control**: Added `verify_certificate` parameter to `KpAnalysisClient` 
- **Enterprise Support**: Enables SDK usage in environments with custom certificate authorities or self-signed certificates
- **Backward Compatibility**: Parameter defaults to `True` maintaining existing security behavior

```mermaid
graph LR
    subgraph "Version 4.3.2 Features"
        KpAnalysisClient["KpAnalysisClient"]
        VerifyCert["verify_certificate parameter"]
        SSLConfig["SSL Configuration"]
    end
    
    subgraph "Use Cases"
        Enterprise["Enterprise Networks"]
        CustomCA["Custom Certificate Authorities"]
        SelfSigned["Self-Signed Certificates"]
    end
    
    KpAnalysisClient --> VerifyCert
    VerifyCert --> SSLConfig
    SSLConfig --> Enterprise
    SSLConfig --> CustomCA
    SSLConfig --> SelfSigned
```

**Certificate Verification Feature Architecture**

Sources: [pyproject.toml:9](), [Release:1]()

### Project Metadata

The project follows Python packaging best practices with comprehensive metadata:

```mermaid
graph TB
    subgraph "Project Metadata"
        Name["debater_python_api"]
        Version["4.3.2"]
        Description["Project Debater Early Access Program API sdk for python"]
        Author["Elad Venezian"]
        Email["eladv@il.ibm.com"]
        License["LICENSE file"]
        Readme["README.md"]
    end
    
    subgraph "Distribution Classifiers"
        PythonLang["Programming Language :: Python :: 3"]
        OSIndep["Operating System :: OS Independent"]
    end
    
    subgraph "Python Requirements"
        MinPython["Python >= 3.6"]
        BuildSystem["setuptools + wheel"]
    end
    
    Name --> Version
    Description --> Author
    Author --> Email
    License --> Readme
    
    PythonLang --> MinPython
    OSIndep --> BuildSystem
```

**Project Metadata Structure**

Sources: [pyproject.toml:7-17](), [pyproject.toml:29]()

