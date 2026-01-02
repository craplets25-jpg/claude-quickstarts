"""
Shared Infrastructure - Core Module
====================================

Core agent functionality shared across all experiments.

Key Functions:
- run_autonomous_agent: Main entry point for running autonomous coding sessions
- run_agent_session: Single agent interaction session
- create_client: Create and configure Claude SDK client
- count_passing_tests: Track test progress
- ExperimentLogger: Comprehensive logging system

Usage from experiment wrapper:
    from shared.infrastructure.core import run_autonomous_agent

    await run_autonomous_agent(
        project_dir=Path("outputs/runs/my-run"),
        config_dir=Path(__file__).parent / "config",
        model="claude-sonnet-4-5",
        max_iterations=None
    )
"""

from .agent import run_autonomous_agent, run_agent_session
from .client import create_client
from .progress import count_passing_tests, print_session_header, print_progress_summary
from .security import bash_security_hook, validate_command
from .experiment_logger import ExperimentLogger, LogLevel
from .prompts import (
    set_prompts_dir,
    get_prompts_dir,
    load_prompt,
    get_initializer_prompt,
    get_coding_prompt,
    get_reviewer_prompt,
    copy_spec_to_project,
)

__all__ = [
    # Main entry points
    "run_autonomous_agent",
    "run_agent_session",

    # Client creation
    "create_client",

    # Progress tracking
    "count_passing_tests",
    "print_session_header",
    "print_progress_summary",

    # Security
    "bash_security_hook",
    "validate_command",

    # Logging
    "ExperimentLogger",
    "LogLevel",

    # Prompts
    "set_prompts_dir",
    "get_prompts_dir",
    "load_prompt",
    "get_initializer_prompt",
    "get_coding_prompt",
    "get_reviewer_prompt",
    "copy_spec_to_project",
]
