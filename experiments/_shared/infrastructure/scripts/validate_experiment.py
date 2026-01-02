#!/usr/bin/env python3
"""
Experiment Validation Script

Validates that an experiment is properly set up and all file references
in prompts actually exist. Prevents bugs like missing EXP_02_MANIFESTO.md.

Usage:
    python scripts/validate_experiment.py
    python scripts/validate_experiment.py --experiment-dir /path/to/experiment_03
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple


class ExperimentValidator:
    """Validates experiment setup and file references."""

    def __init__(self, experiment_dir: Path):
        self.experiment_dir = experiment_dir
        self.prompts_dir = experiment_dir / "prompts"
        self.docs_dir = experiment_dir / "docs"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def validate_all(self) -> bool:
        """Run all validations. Returns True if all passed."""
        print(f"=== Validating Experiment: {self.experiment_dir.name} ===\n")

        self.validate_directory_structure()
        self.validate_required_files()
        self.validate_file_references_in_prompts()
        self.validate_experiment_consistency()
        self.validate_symlinks()

        self.print_report()

        return len(self.errors) == 0

    def validate_directory_structure(self):
        """Check that required directories exist."""
        print("Checking directory structure...")

        required_dirs = [
            "prompts",
            "docs",
            "scripts",
            "runs",
        ]

        for dir_name in required_dirs:
            dir_path = self.experiment_dir / dir_name
            if dir_path.exists():
                self.info.append(f"✓ Directory exists: {dir_name}/")
            else:
                self.errors.append(f"Missing required directory: {dir_name}/")

    def validate_required_files(self):
        """Check that required files exist."""
        print("Checking required files...")

        # Required files in experiment root
        required_files = [
            "agent.py",
            "client.py",
            "experiment_logger.py",
            "progress.py",
            "prompts.py",
            "security.py",
            ".env",
            "requirements.txt",
        ]

        for file_name in required_files:
            file_path = self.experiment_dir / file_name
            if file_path.exists():
                self.info.append(f"✓ File exists: {file_name}")
            else:
                self.errors.append(f"Missing required file: {file_name}")

        # Check prompts
        required_prompts = [
            "spec_librarian_prompt.md",
            "spec_reviewer_prompt.md",
            "coding_prompt.md",
            "phase_constraint.txt",
        ]

        for prompt in required_prompts:
            prompt_path = self.prompts_dir / prompt
            if prompt_path.exists():
                self.info.append(f"✓ Prompt exists: prompts/{prompt}")
            else:
                self.errors.append(f"Missing required prompt: prompts/{prompt}")

    def validate_file_references_in_prompts(self):
        """Validate that all file references in prompts actually exist."""
        print("Checking file references in prompts...")

        if not self.prompts_dir.exists():
            self.errors.append(f"Prompts directory not found: {self.prompts_dir}")
            return

        for prompt_file in self.prompts_dir.glob('*.md'):
            self._validate_file_refs_in_file(prompt_file)

        # Also check phase_constraint.txt
        phase_constraint = self.prompts_dir / "phase_constraint.txt"
        if phase_constraint.exists():
            self._validate_file_refs_in_file(phase_constraint)

    def _validate_file_refs_in_file(self, file_path: Path):
        """Check file references in a single file."""
        content = file_path.read_text()
        relative_name = file_path.relative_to(self.experiment_dir)

        # Pattern to match file references
        # Matches: ../../../path/to/file.md or ./file.json or FILENAME.ext
        patterns = [
            r'(?:\.\.\/)+[^\s\)\]`]+\.[a-zA-Z]+',  # ../../../path/file.ext
            r'\.\/[^\s\)\]`]+\.[a-zA-Z]+',  # ./file.ext
            r'(?<![\/\w])[A-Z][A-Z_0-9]+\.(md|txt|json)',  # CAPS_FILE.ext
        ]

        for pattern in patterns:
            refs = re.findall(pattern, content)

            for ref in refs:
                # Handle tuple from regex groups
                if isinstance(ref, tuple):
                    ref = ref[0]

                # Resolve path
                ref_path = self._resolve_reference(ref, file_path)

                if ref_path and not ref_path.exists():
                    self.errors.append(
                        f"{relative_name}: Referenced file missing: {ref}"
                    )
                    self.errors.append(
                        f"  Expected at: {ref_path}"
                    )

    def _resolve_reference(self, ref: str, source_file: Path) -> Path | None:
        """Resolve a file reference to an absolute path."""
        try:
            if ref.startswith('../'):
                # Relative to source file's directory
                return (source_file.parent / ref).resolve()
            elif ref.startswith('./'):
                # Relative to source file's directory
                return (source_file.parent / ref[2:]).resolve()
            else:
                # Try in experiment root
                return (self.experiment_dir / ref).resolve()
        except (OSError, ValueError):
            return None

    def validate_experiment_consistency(self):
        """Check that experiment numbers and names are consistent."""
        print("Checking experiment number consistency...")

        # Extract experiment number from directory name
        dir_match = re.search(r'experiment_(\d+)', self.experiment_dir.name)
        if not dir_match:
            self.warnings.append("Could not extract experiment number from directory name")
            return

        exp_num = int(dir_match.group(1))

        # Check consistency in docs
        if self.docs_dir.exists():
            for doc_file in self.docs_dir.glob('*.md'):
                content = doc_file.read_text()

                # Look for experiment number references
                exp_refs = re.findall(r'(?:Experiment|EXPERIMENT|EXP)[_\s]+(\d+)', content)

                for ref_num in exp_refs:
                    if int(ref_num) != exp_num:
                        self.warnings.append(
                            f"{doc_file.name}: Found reference to Experiment {ref_num}, "
                            f"but directory is experiment_{exp_num:02d}"
                        )

    def validate_symlinks(self):
        """Check that symlinks to shared resources are valid."""
        print("Checking symlinks...")

        parent_dir = self.experiment_dir.parent

        expected_symlinks = [
            "deep-wiki-spec-files",
            "reference-files",
        ]

        for link_name in expected_symlinks:
            link_path = parent_dir / link_name

            if not link_path.exists():
                self.errors.append(f"Missing symlink: {link_name}")
            elif not link_path.is_symlink():
                self.warnings.append(f"{link_name} exists but is not a symlink")
            else:
                target = link_path.resolve()
                if target.exists():
                    self.info.append(f"✓ Symlink valid: {link_name} → {target.name}")
                else:
                    self.errors.append(
                        f"Symlink broken: {link_name} → {link_path.readlink()} (target missing)"
                    )

    def print_report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All validations passed!")
            print("\nExperiment is properly configured and ready to run.")
        elif not self.errors:
            print("\n✅ No critical errors found.")
            print("⚠  Please review warnings above.")
        else:
            print(f"\n❌ Found {len(self.errors)} error(s) that must be fixed.")
            print("Please address the errors before running the experiment.")

        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Validate experiment setup and file references'
    )
    parser.add_argument(
        '--experiment-dir',
        type=Path,
        help='Path to experiment directory (default: current directory)'
    )

    args = parser.parse_args()

    # Default to current directory
    experiment_dir = args.experiment_dir or Path.cwd()

    # If we're in scripts/, go up one level
    if experiment_dir.name == 'scripts':
        experiment_dir = experiment_dir.parent

    if not experiment_dir.exists():
        print(f"❌ Error: Directory not found: {experiment_dir}")
        return 1

    validator = ExperimentValidator(experiment_dir)
    success = validator.validate_all()

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
