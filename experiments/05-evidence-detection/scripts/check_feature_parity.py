#!/usr/bin/env python3
"""
Feature Parity Checker (FLAT STRUCTURE)

Validates that an experiment has all critical features.
Supports both flat and nested experiment structures.

Usage:
    cd experiments/05-your-experiment
    python scripts/check_feature_parity.py
"""

import re
from pathlib import Path
from typing import List


class FeatureParityChecker:
    """Check that experiment has all critical features."""

    def __init__(self):
        # Find experiment root (where this script is run from)
        self.experiment_dir = Path.cwd()

        # If we're in scripts/, go up one level
        if self.experiment_dir.name == "scripts":
            self.experiment_dir = self.experiment_dir.parent

        # Find the actual experiment root (where agent.py lives)
        self.exp_root = self._find_experiment_root()

        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def _find_experiment_root(self) -> Path:
        """Find experiment root (where agent.py lives)."""
        # Check flat structure
        if (self.experiment_dir / "agent.py").exists():
            return self.experiment_dir

        # Check nested structure
        for exp_dir in self.experiment_dir.glob("experiment_*"):
            if (exp_dir / "agent.py").exists():
                return exp_dir

        # Default to cwd
        return self.experiment_dir

    def check_all(self) -> bool:
        """Run all parity checks. Returns True if all critical features present."""
        print(f"=== Feature Parity Check ===")
        print(f"Experiment: {self.experiment_dir.name}")
        print(f"Root: {self.exp_root.relative_to(self.experiment_dir.parent)}\n")

        self.check_git_initialization()
        self.check_git_in_prompts()
        self.check_progress_tracking()
        self.check_runner_script()
        self.check_rich_feature_list()
        self.check_symlinks()
        self.check_runs_isolation()

        self.print_report()
        return len(self.errors) == 0

    def check_git_initialization(self):
        """Check if experiment initializes git repos for each run."""
        print("Checking git initialization...")

        agent_py = self.exp_root / "agent.py"
        if not agent_py.exists():
            self.errors.append("❌ CRITICAL: agent.py not found")
            return

        content = agent_py.read_text()
        has_git_init = (
            "_initialize_git_repo" in content or
            ("subprocess" in content and "git init" in content)
        )

        if has_git_init:
            self.info.append("✓ agent.py has git initialization")
        else:
            self.errors.append(
                "❌ CRITICAL: agent.py doesn't initialize git for runs\n"
                "   Each run should have isolated .git/ directory"
            )

    def check_git_in_prompts(self):
        """Check if prompts instruct agents to use git."""
        print("Checking git in prompts...")

        coding_prompt = self.exp_root / "prompts" / "coding_prompt.md"
        if not coding_prompt.exists():
            self.warnings.append("⚠  coding_prompt.md not found")
            return

        content = coding_prompt.read_text()
        git_commands = ["git commit", "git add", "git status", "git log"]
        has_git = any(cmd in content for cmd in git_commands)

        if has_git:
            self.info.append("✓ coding_prompt.md includes git instructions")
        else:
            self.errors.append(
                "❌ CRITICAL: coding_prompt.md doesn't mention git commands\n"
                "   Agent won't commit progress incrementally"
            )

    def check_progress_tracking(self):
        """Check if progress tracking is set up."""
        print("Checking progress tracking...")

        progress_py = self.exp_root / "progress.py"
        if progress_py.exists():
            self.info.append("✓ progress.py present")
        else:
            self.warnings.append("⚠  progress.py not found")

    def check_runner_script(self):
        """Check if runner script exists."""
        print("Checking runner script...")

        runner = self.exp_root / "scripts" / "autonomous_agent_demo.py"
        if runner.exists():
            self.info.append("✓ autonomous_agent_demo.py present")
        else:
            self.errors.append("❌ CRITICAL: scripts/autonomous_agent_demo.py not found")

    def check_rich_feature_list(self):
        """Check if spec_librarian creates rich feature_list.json."""
        print("Checking rich feature_list support...")

        spec_librarian = self.exp_root / "prompts" / "spec_librarian_prompt.md"
        if not spec_librarian.exists():
            self.warnings.append("⚠  spec_librarian_prompt.md not found")
            return

        content = spec_librarian.read_text()

        # Check for rich feature_list fields
        rich_fields = ["sources", "invariants", "non_guarantees", "legacy_notes"]
        has_rich = all(field in content for field in rich_fields)

        if has_rich:
            self.info.append("✓ spec_librarian creates rich feature_list.json")
        else:
            self.warnings.append(
                "⚠  spec_librarian may not create rich feature_list.json\n"
                "   Missing fields: sources, invariants, non_guarantees, legacy_notes"
            )

    def check_symlinks(self):
        """Check if symlinks to shared resources exist."""
        print("Checking symlinks...")

        # Check deep-wiki-spec-files
        deepwiki = self.exp_root / "deep-wiki-spec-files"
        if deepwiki.exists() or deepwiki.is_symlink():
            if deepwiki.is_symlink():
                self.info.append(f"✓ deep-wiki-spec-files → {deepwiki.resolve().name}")
            else:
                self.info.append("✓ deep-wiki-spec-files exists")
        else:
            self.warnings.append("⚠  deep-wiki-spec-files symlink missing")

        # Check reference-files
        ref = self.exp_root / "reference-files"
        if ref.exists() or ref.is_symlink():
            self.info.append("✓ reference-files exists")
        else:
            self.warnings.append("⚠  reference-files symlink missing")

        # Check custom_skills/deepwiki-navigator
        skill = self.exp_root / "custom_skills" / "deepwiki-navigator"
        if skill.exists() or skill.is_symlink():
            self.info.append("✓ custom_skills/deepwiki-navigator exists")
        else:
            self.warnings.append("⚠  custom_skills/deepwiki-navigator missing")

    def check_runs_isolation(self):
        """Check if existing runs have isolated git repos."""
        print("Checking run isolation...")

        runs_dir = self.exp_root / "runs"
        if not runs_dir.exists():
            self.info.append("✓ runs/ directory exists (empty)")
            return

        run_dirs = [d for d in runs_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

        if not run_dirs:
            self.info.append("✓ runs/ directory ready (no runs yet)")
            return

        # Check first few runs for .git
        checked = 0
        has_git = 0
        for run_dir in run_dirs[:3]:
            checked += 1
            if (run_dir / ".git").exists():
                has_git += 1

        if checked > 0:
            if has_git == checked:
                self.info.append(f"✓ Existing runs have isolated .git/ ({has_git}/{checked})")
            elif has_git > 0:
                self.warnings.append(f"⚠  Some runs missing .git/ ({has_git}/{checked} have it)")
            else:
                # Only warning - old runs may predate git init
                # Critical is if agent.py doesn't have git init (checked earlier)
                self.warnings.append(
                    f"⚠  Existing runs don't have .git/ ({checked} checked)\n"
                    "   These runs predate git initialization - new runs will have it"
                )

    def print_report(self):
        """Print feature parity report."""
        print("\n" + "="*60)
        print("FEATURE PARITY REPORT")
        print("="*60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.info:
            print(f"\n✓ PASSED ({len(self.info)}):")
            for info in self.info:
                print(f"  {info}")

        print("\n" + "="*60)
        if self.errors:
            print("❌ Feature parity check FAILED")
            print("Fix critical errors before running experiments.")
        elif self.warnings:
            print("⚠  Feature parity check PASSED with warnings")
            print("Review warnings to ensure expected behavior.")
        else:
            print("✅ Feature parity check PASSED")
            print("All critical features present!")
        print("="*60)


def main():
    checker = FeatureParityChecker()
    success = checker.check_all()
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
