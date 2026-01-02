"""
Prompt Loading Utilities
========================

Functions for loading prompt templates from the prompts directory.
"""

import shutil
from pathlib import Path


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / f"{name}.md"
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


def copy_spec_to_project(project_dir: Path) -> None:
    """Copy canonical artifact references into the project directory."""
    # Copy the phase constraint file
    constraint_source = PROMPTS_DIR / "phase_constraint.txt"
    constraint_dest = project_dir / "phase_constraint.txt"
    if constraint_source.exists() and not constraint_dest.exists():
        shutil.copy(constraint_source, constraint_dest)
        print("Copied phase_constraint.txt to project directory")

    # Also copy the manifesto for reference
    # Manifesto is now in knowledge-base/ (moved from docs/ during restructure)
    manifesto_source = Path(__file__).parent.parent.parent / "knowledge-base" / "experiment-04-argument-quality" / "EXP_04_MANIFESTO.md"
    manifesto_dest = project_dir / "EXP_04_MANIFESTO.md"
    if manifesto_source.exists() and not manifesto_dest.exists():
        shutil.copy(manifesto_source, manifesto_dest)
        print("Copied EXP_04_MANIFESTO.md to project directory")
    elif not manifesto_source.exists():
        print(f"WARNING: EXP_04_MANIFESTO.md not found at {manifesto_source}")
