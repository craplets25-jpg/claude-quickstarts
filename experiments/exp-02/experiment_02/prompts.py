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


def copy_spec_to_project(project_dir: Path) -> None:
    """Copy canonical artifact references into the project directory."""
    # Copy the phase spec file
    spec_source = PROMPTS_DIR / "phase_spec.txt"
    spec_dest = project_dir / "phase_spec.txt"
    if spec_source.exists() and not spec_dest.exists():
        shutil.copy(spec_source, spec_dest)
        print("Copied phase_spec.txt to project directory")

    # Also copy the manifesto for reference
    manifesto_source = Path(__file__).parent / "EXP_02_MANIFESTO.md"
    manifesto_dest = project_dir / "EXP_02_MANIFESTO.md"
    if manifesto_source.exists() and not manifesto_dest.exists():
        shutil.copy(manifesto_source, manifesto_dest)
        print("Copied EXP_02_MANIFESTO.md to project directory")
