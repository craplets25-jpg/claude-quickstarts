#!/usr/bin/env python3
"""
Feature Parity Checker

Compares experiment infrastructure against autonomous-coding baseline
to catch missing critical features like git initialization.

Usage:
    python scripts/check_feature_parity.py
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple


class FeatureParityChecker:
    """Check that experiment has feature parity with autonomous-coding."""

    def __init__(self):
        self.autonomous_coding_dir = Path("/workspaces/claude-quickstarts/autonomous-coding")
        self.experiment_dir = Path(__file__).parent.parent
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def check_all(self) -> bool:
        """Run all parity checks. Returns True if all critical features present."""
        print(f"=== Checking Feature Parity ===")
        print(f"Baseline: {self.autonomous_coding_dir}")
        print(f"Experiment: {self.experiment_dir.name}\n")

        self.check_git_initialization()
        self.check_git_usage_in_prompts()
        self.check_agent_commits()
        self.check_project_isolation()
        self.check_progress_tracking()

        self.print_report()
        return len(self.errors) == 0

    def check_git_initialization(self):
        """Check if experiment initializes git repos for each run."""
        print("Checking git initialization...")

        # Check if initializer prompt exists and mentions git init
        baseline_initializer = self.autonomous_coding_dir / "prompts/initializer_prompt.md"
        if baseline_initializer.exists():
            content = baseline_initializer.read_text()
            if "git repo" in content.lower() or "git init" in content.lower():
                self.info.append("✓ Baseline has git initialization in prompts")

                # Check if experiment has similar
                exp_prompts_dir = self.experiment_dir / "prompts"
                has_git_mention = False

                if exp_prompts_dir.exists():
                    for prompt_file in exp_prompts_dir.glob("*.md"):
                        content = prompt_file.read_text()
                        # Check for git commands (commit, log, status, etc.)
                        if any(cmd in content.lower() for cmd in ["git commit", "git log", "git status", "git add"]):
                            has_git_mention = True
                            break

                if has_git_mention:
                    self.info.append("✓ Prompts instruct agents to use git")
                else:
                    self.warnings.append(
                        "⚠ Experiment prompts don't explicitly mention git commands"
                    )

        # Check if agent.py initializes git
        baseline_agent = self.autonomous_coding_dir / "agent.py"
        exp_agent = self.experiment_dir / "agent.py"

        if baseline_agent.exists() and exp_agent.exists():
            baseline_content = baseline_agent.read_text()
            exp_content = exp_agent.read_text()

            # Check for git initialization - look for actual git commands
            exp_has_git_init = (
                "git init" in exp_content or
                "_initialize_git_repo" in exp_content or
                ("subprocess" in exp_content and "git" in exp_content)
            )

            if exp_has_git_init:
                self.info.append("✓ agent.py initializes git repositories")
            else:
                self.errors.append(
                    "❌ CRITICAL: agent.py doesn't initialize git for project directories"
                )

    def check_git_usage_in_prompts(self):
        """Check if prompts tell agents to use git commands."""
        print("Checking git usage in prompts...")

        baseline_prompts = self.autonomous_coding_dir / "prompts"
        exp_prompts = self.experiment_dir / "prompts"

        if baseline_prompts.exists():
            baseline_git_cmds = self._find_git_commands_in_prompts(baseline_prompts)
            exp_git_cmds = self._find_git_commands_in_prompts(exp_prompts)

            if baseline_git_cmds and not exp_git_cmds:
                self.errors.append(
                    f"❌ CRITICAL: Baseline prompts mention git commands {baseline_git_cmds}, "
                    f"but experiment prompts don't"
                )
            elif baseline_git_cmds:
                self.info.append(f"✓ Both use git commands: {', '.join(baseline_git_cmds)}")

    def _find_git_commands_in_prompts(self, prompts_dir: Path) -> List[str]:
        """Find git commands mentioned in prompt files."""
        git_commands = set()
        git_pattern = re.compile(r'git\s+(init|add|commit|log|status|diff|push)')

        for prompt_file in prompts_dir.glob("*.md"):
            content = prompt_file.read_text()
            for match in git_pattern.finditer(content):
                git_commands.add(f"git {match.group(1)}")

        return sorted(git_commands)

    def check_agent_commits(self):
        """Check if agents are told to commit their progress."""
        print("Checking agent commit behavior...")

        exp_prompts = self.experiment_dir / "prompts"

        if exp_prompts.exists():
            coding_prompt = exp_prompts / "coding_prompt.md"
            if coding_prompt.exists():
                content = coding_prompt.read_text()

                has_commit_instruction = "git commit" in content.lower() or "commit" in content.lower()

                if not has_commit_instruction:
                    self.warnings.append(
                        "⚠ Coding prompt doesn't explicitly tell agent to commit progress"
                    )
                else:
                    self.info.append("✓ Coding prompt mentions committing")

    def check_project_isolation(self):
        """Check if each run has isolated project directory."""
        print("Checking project isolation...")

        # Check if runs have .git directories
        runs_dir = self.experiment_dir / "runs"
        if runs_dir.exists():
            run_dirs = [d for d in runs_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

            if run_dirs:
                has_git = False
                for run_dir in run_dirs[:3]:  # Check first 3 runs
                    if (run_dir / ".git").exists():
                        has_git = True
                        break

                if not has_git:
                    self.errors.append(
                        "❌ CRITICAL: Run directories don't have .git/ - "
                        "not isolated repositories"
                    )
                else:
                    self.info.append("✓ Runs have isolated .git directories")

    def check_progress_tracking(self):
        """Check if progress tracking is properly set up."""
        print("Checking progress tracking...")

        baseline_progress = self.autonomous_coding_dir / "progress.py"
        exp_progress = self.experiment_dir / "progress.py"

        if baseline_progress.exists() and not exp_progress.exists():
            self.warnings.append("⚠ Baseline has progress.py but experiment doesn't")
        elif exp_progress.exists():
            self.info.append("✓ Progress tracking present")

    def print_report(self):
        """Print feature parity report."""
        print("\n" + "="*60)
        print("FEATURE PARITY REPORT")
        print("="*60)

        if self.errors:
            print(f"\n❌ CRITICAL ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.info:
            print(f"\n✓ INFO ({len(self.info)}):")
            for info in self.info:
                print(f"  {info}")

        if self.errors:
            print(f"\n❌ Feature parity check FAILED")
            print("These missing features could cause experiments to fail.")
            print("Fix critical errors before running experiments.")
        elif self.warnings:
            print(f"\n⚠  Feature parity check passed with warnings")
            print("Review warnings to ensure expected behavior.")
        else:
            print(f"\n✅ Feature parity check PASSED")
            print("Experiment has all critical features from baseline.")

        print("\n" + "="*60)


def main():
    checker = FeatureParityChecker()
    success = checker.check_all()
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
