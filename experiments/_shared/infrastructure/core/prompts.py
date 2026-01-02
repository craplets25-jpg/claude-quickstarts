"""
Prompt Loading Utilities
========================

Functions for loading prompt templates from the prompts directory.
Each experiment has its own prompts in config/prompts/.
"""

import shutil
from pathlib import Path
from typing import Optional


# Global prompts directory - must be set by experiment before use
_PROMPTS_DIR: Optional[Path] = None


def set_prompts_dir(prompts_dir: Path) -> None:
    """Set the prompts directory for this experiment."""
    global _PROMPTS_DIR
    _PROMPTS_DIR = Path(prompts_dir)


def get_prompts_dir() -> Path:
    """Get the current prompts directory."""
    if _PROMPTS_DIR is None:
        raise RuntimeError(
            "Prompts directory not set. Call set_prompts_dir() first."
        )
    return _PROMPTS_DIR


def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = get_prompts_dir() / f"{name}.md"
    return prompt_path.read_text()


def get_initializer_prompt() -> str:
    """Load the Spec Librarian prompt (replaces old initializer)."""
    return load_prompt("spec_librarian_prompt")


def get_coding_prompt() -> str:
    """Load the coding agent prompt."""
    return load_prompt("coding_prompt")


def get_reviewer_prompt() -> str:
    """Load the Spec Reviewer prompt (tech-agnostic filter)."""
    return load_prompt("spec_reviewer_prompt")


def copy_spec_to_project(project_dir: Path, config_dir: Path) -> None:
    """Copy canonical artifact references into the project directory.

    Args:
        project_dir: The run directory where files should be copied
        config_dir: The experiment's config directory containing source files
    """
    # Copy the phase constraint file
    constraint_source = config_dir / "phase_constraint.txt"
    constraint_dest = project_dir / "phase_constraint.txt"
    if constraint_source.exists() and not constraint_dest.exists():
        shutil.copy(constraint_source, constraint_dest)
        print("Copied phase_constraint.txt to project directory")

    # Also copy the manifesto for reference if it exists
    manifesto_source = config_dir.parent / "notes" / "EXP_02_MANIFESTO.md"
    manifesto_dest = project_dir / "EXP_02_MANIFESTO.md"
    if manifesto_source.exists() and not manifesto_dest.exists():
        shutil.copy(manifesto_source, manifesto_dest)
        print("Copied EXP_02_MANIFESTO.md to project directory")
