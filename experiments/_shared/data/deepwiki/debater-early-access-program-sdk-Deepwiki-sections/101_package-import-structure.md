<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Package Import Structure -->
<!-- Lines: 4716-4729 -->

## Package Import Structure

The package uses a structured import pattern where:

- **Root package** (`debater_python_api/__init__.py`) serves as the main entry point
- **API package** (`debater_python_api/api/__init__.py`) exposes the `DebaterApi` factory
- **Clients package** (`debater_python_api/api/clients/__init__.py`) contains all service client implementations
- **Utils package** contains utility functions and helper classes
- **Models package** contains data models and custom exceptions

Each `__init__.py` file controls the public API surface by explicitly importing and exposing relevant classes and functions. This design allows for clean separation of concerns while maintaining a simple import structure for end users.

*Sources: [debater_python_api/__init__.py:1-1](), [debater_python_api/api/__init__.py:1-1](), [debater_python_api/api/clients/__init__.py:1-1]()*

