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
    # Detect experiment number from current directory
    experiment_dir = Path(__file__).parent
    exp_num = experiment_dir.name.split('-')[0]  # Extract '04' from '04-argument-quality'

    manifesto_filename = f"EXP_{exp_num}_MANIFESTO.md"
    kb_experiment_dir = f"experiment-{experiment_dir.name}"

    manifesto_source = Path(__file__).parent.parent.parent / "knowledge-base" / kb_experiment_dir / manifesto_filename
    manifesto_dest = project_dir / manifesto_filename

    if manifesto_source.exists() and not manifesto_dest.exists():
        shutil.copy(manifesto_source, manifesto_dest)
        print(f"Copied {manifesto_filename} to project directory")
    elif not manifesto_source.exists():
        print(f"WARNING: {manifesto_filename} not found at {manifesto_source}")
