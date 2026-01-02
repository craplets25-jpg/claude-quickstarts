"""
Shared Infrastructure Package
==============================

Code shared across all experiments to eliminate duplication and maintain
a single source of truth.

Structure:
- core/: Agent logic, client configuration, logging, security
- scripts/: Utility scripts (demo runner, validators, etc.)
- utils/: Helper utilities (document parser, etc.)

Usage:
    # From experiment wrapper script
    import sys
    from pathlib import Path

    # Add shared infrastructure to path
    shared_infra = Path(__file__).parent.parent / "_shared" / "infrastructure"
    sys.path.insert(0, str(shared_infra))

    # Import from shared core
    from core import run_autonomous_agent
"""

# Re-export core functionality at package level for convenience
from .core import (
    run_autonomous_agent,
    run_agent_session,
    create_client,
    count_passing_tests,
    ExperimentLogger,
)

__all__ = [
    "run_autonomous_agent",
    "run_agent_session",
    "create_client",
    "count_passing_tests",
    "ExperimentLogger",
]
