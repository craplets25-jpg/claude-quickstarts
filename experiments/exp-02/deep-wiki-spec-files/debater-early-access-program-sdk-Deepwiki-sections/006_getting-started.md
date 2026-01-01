<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Getting Started -->
<!-- Lines: 247-276 -->

## Getting Started

To begin using the SDK, developers should:

1. Install the package and configure authentication
2. Initialize the `DebaterApi` factory to access service clients
3. Use specialized clients for specific NLP tasks
4. Process results using the provided utilities and data models

For detailed setup instructions, see [Getting Started](#2). For comprehensive usage examples, see the service-specific documentation sections: [Key Point Analysis](#3) and [Other NLP Services](#4).

Sources: [README.md:1-3](), [pyproject.toml:7-10]()15:T25a9,# Getting Started

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [debater_python_api/examples/keypoints_example.py](debater_python_api/examples/keypoints_example.py)
- [debater_python_api/integration_tests/api/clients/ServicesIT.py](debater_python_api/integration_tests/api/clients/ServicesIT.py)
- [pyproject.toml](pyproject.toml)

</details>



This document provides installation instructions, basic configuration, and simple usage examples to help you quickly start using the Debater Early Access Program SDK. The SDK is a Python client library for IBM's Project Debater API services, enabling access to various natural language processing capabilities including Key Point Analysis, Argument Quality scoring, Claim Detection, and more.

For comprehensive documentation of the Key Point Analysis system (the primary feature), see [Key Point Analysis](#3). For details about other NLP services available in the SDK, see [Other NLP Services](#4).

