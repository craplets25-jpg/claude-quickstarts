#!/usr/bin/env python3
"""
Automated Experiment Setup Script (FLAT STRUCTURE)

Creates a new experiment by copying an existing one with FLAT structure.
No more experiment_XX subdirectories - everything at experiment root level.

Usage:
    python setup_new_experiment.py --source 04-argument-quality --target 05-new-cap --capability "New Capability" --num 5
"""

import argparse
import shutil
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional


def get_experiment_root(exp_path: Path) -> Path:
    """
    Get the experiment root directory (where agent.py lives).

    Supports both:
    - FLAT structure: exp_path/agent.py (NEW)
    - NESTED structure: exp_path/experiment_XX/agent.py (OLD)
    """
    # Check flat structure first
    if (exp_path / "agent.py").exists():
        return exp_path

    # Check nested structure (backward compatibility)
    experiment_dirs = list(exp_path.glob("experiment_*"))
    if experiment_dirs:
        experiment_dirs.sort()
        nested_dir = experiment_dirs[-1]
        if (nested_dir / "agent.py").exists():
            return nested_dir

    raise FileNotFoundError(
        f"Cannot find agent.py in {exp_path} or {exp_path}/experiment_*/"
    )


def validate_source_has_critical_features(source_path: Path) -> bool:
    """
    Validate that source experiment has critical features.
    Returns True if source has all critical features.
    """
    print("🔍 Validating source experiment has critical features...")

    errors = []
    warnings = []

    try:
        source_root = get_experiment_root(source_path)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return False

    # Check 1: Git initialization in agent.py
    agent_py = source_root / "agent.py"
    content = agent_py.read_text()
    has_git_init = (
        "_initialize_git_repo" in content or
        ("subprocess" in content and "git init" in content)
    )

    if not has_git_init:
        errors.append(
            "❌ CRITICAL: agent.py doesn't initialize git repositories\n"
            "   New experiment won't have isolated git per run!"
        )
    else:
        print("  ✓ Has git initialization")

    # Check 2: Git commands in coding prompt
    coding_prompt = source_root / "prompts" / "coding_prompt.md"
    if coding_prompt.exists():
        content = coding_prompt.read_text()
        has_git_cmds = "git commit" in content or "git add" in content

        if not has_git_cmds:
            warnings.append(
                "⚠  coding_prompt.md doesn't mention git commands"
            )
        else:
            print("  ✓ Has git instructions in prompts")

    # Check 3: Progress tracking
    if not (source_root / "progress.py").exists():
        warnings.append("⚠  progress.py not found")
    else:
        print("  ✓ Has progress tracking")

    # Check 4: Spec librarian with rich feature_list
    spec_librarian = source_root / "prompts" / "spec_librarian_prompt.md"
    if spec_librarian.exists():
        content = spec_librarian.read_text()
        has_rich_features = "invariants" in content and "sources" in content
        if has_rich_features:
            print("  ✓ Has rich feature_list.json support")
        else:
            warnings.append("⚠  spec_librarian may not create rich feature_list.json")

    # Check 5: Scripts directory
    if not (source_root / "scripts" / "autonomous_agent_demo.py").exists():
        errors.append("❌ CRITICAL: scripts/autonomous_agent_demo.py not found")
    else:
        print("  ✓ Has runner script")

    if errors:
        print("\n" + "="*60)
        print("❌ SOURCE VALIDATION FAILED")
        print("="*60)
        for error in errors:
            print(f"  {error}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  {warning}")
        print("\n⚠️  DO NOT COPY FROM THIS SOURCE!")
        print(f"   Source: {source_path.name}")
        print("\nRecommendation:")
        print("  Copy from 04-argument-quality (source of truth)")
        print("="*60)
        return False

    if warnings:
        print("\n⚠  Warnings (non-critical):")
        for warning in warnings:
            print(f"  {warning}")

    print("  ✅ Source validation passed\n")
    return True


def run_feature_parity_check(target_path: Path) -> bool:
    """Run feature parity check on newly created experiment."""
    print("\n🔍 Running feature parity check...")

    check_script = Path(__file__).parent / "check_feature_parity.py"
    if not check_script.exists():
        print("  ⚠  check_feature_parity.py not found, skipping")
        return True

    # Copy to target
    target_scripts = target_path / "scripts"
    target_scripts.mkdir(exist_ok=True)
    shutil.copy(check_script, target_scripts / "check_feature_parity.py")

    # Also copy validate_experiment.py if exists
    validate_script = Path(__file__).parent / "validate_experiment.py"
    if validate_script.exists():
        shutil.copy(validate_script, target_scripts / "validate_experiment.py")

    try:
        result = subprocess.run(
            [sys.executable, str(target_scripts / "check_feature_parity.py")],
            cwd=target_path,
            capture_output=True,
            text=True,
            timeout=15
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode != 0:
            print("\n" + "="*60)
            print("❌ FEATURE PARITY CHECK FAILED")
            print("="*60)
            return False

        return True

    except subprocess.TimeoutExpired:
        print("  ⚠  Feature parity check timed out")
        return False
    except Exception as e:
        print(f"  ⚠  Could not run feature parity check: {e}")
        return False


def setup_experiment(
    source_exp: str,
    target_exp: str,
    capability: str,
    exp_num: int,
    base_dir: Path = None
) -> None:
    """
    Set up a new experiment with FLAT structure.
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.parent.parent.parent

    source_path = base_dir / source_exp
    target_path = base_dir / target_exp

    print("="*60)
    print(f"  EXPERIMENT SETUP (FLAT STRUCTURE)")
    print("="*60)
    print(f"\nSource: {source_exp}")
    print(f"Target: {target_exp}")
    print(f"Capability: {capability}")
    print(f"Number: {exp_num}")
    print()

    # Step 1: Validate source exists
    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source_path}")

    # Step 2: Validate source has critical features
    if not validate_source_has_critical_features(source_path):
        raise ValueError(
            f"Source '{source_exp}' missing critical features!\n"
            f"Use 04-argument-quality as source."
        )

    # Step 3: Check target doesn't exist
    if target_path.exists():
        raise FileExistsError(f"Target already exists: {target_path}")

    # Step 4: Get source root (handles flat or nested)
    source_root = get_experiment_root(source_path)
    print(f"✓ Source root: {source_root.relative_to(base_dir)}")

    # Step 5: Create target with FLAT structure
    print(f"✓ Creating {target_path.name}/ (flat structure)")
    target_path.mkdir(parents=True)

    # Step 6: Copy source to target (flat)
    print(f"✓ Copying experiment files...")

    # Files/dirs to copy (includes debater_sdk - cumulative work)
    items_to_copy = [
        "agent.py", "client.py", "progress.py", "prompts.py",
        "experiment_logger.py", "security.py", "requirements.txt",
        ".gitignore", ".env",
        "prompts", "scripts", "custom_skills",
        "debater_sdk"  # Scaffold is CUMULATIVE - each experiment adds to it
    ]

    for item in items_to_copy:
        src = source_root / item
        dst = target_path / item
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"    Copied: {item}")

    # Step 7: Create runs/ directory
    runs_dir = target_path / "runs"
    runs_dir.mkdir(exist_ok=True)
    print("✓ Created runs/")

    # Step 8: Create symlinks to shared resources
    print("✓ Creating symlinks to _shared/...")

    # Symlink to deepwiki
    deepwiki_link = target_path / "deep-wiki-spec-files"
    deepwiki_link.symlink_to("../_shared/data/deepwiki")
    print("    deep-wiki-spec-files → ../_shared/data/deepwiki")

    # Symlink to reference files
    ref_link = target_path / "reference-files"
    ref_link.symlink_to("../_shared/data/reference-examples")
    print("    reference-files → ../_shared/data/reference-examples")

    # Create custom_skills directory and symlink
    custom_skills = target_path / "custom_skills"
    if not custom_skills.exists():
        custom_skills.mkdir()

    skill_link = custom_skills / "deepwiki-navigator"
    if not skill_link.exists():
        skill_link.symlink_to("../../_shared/skills/deepwiki-navigator")
        print("    custom_skills/deepwiki-navigator → ../../_shared/skills/deepwiki-navigator")

    # Step 9: Clean up docs/ if present (belongs in knowledge-base)
    docs_dir = target_path / "docs"
    if docs_dir.exists():
        shutil.rmtree(docs_dir)
        print("✓ Removed docs/ (use knowledge-base/ instead)")

    # Step 10: Update file references
    print("✓ Updating references...")
    replacements = generate_replacements(source_exp, target_exp, exp_num)
    update_all_files(target_path, replacements)

    # Step 11: Update phase_constraint.txt
    print(f"✓ Updating phase_constraint.txt for '{capability}'...")
    update_phase_constraint(target_path, capability)

    # Step 12: Rename manifesto file if present
    rename_manifesto(target_path, exp_num)

    # Step 13: Run feature parity check
    parity_passed = run_feature_parity_check(target_path)

    # Step 14: Summary
    print("\n" + "="*60)
    if parity_passed:
        print(f"✅ Experiment {exp_num} setup complete!")
    else:
        print(f"⚠️  Experiment {exp_num} setup complete with warnings")
    print("="*60)

    print(f"""
Location: {target_path}
Structure: FLAT (no experiment_XX subdirectory)

Next steps:
  1. Create knowledge-base docs:
     mkdir -p {base_dir.parent}/knowledge-base/experiment-{exp_num:02d}-{capability.lower().replace(' ', '-')}/reports

  2. Navigate to experiment:
     cd {target_path}

  3. Run experiment:
     python scripts/autonomous_agent_demo.py \\
       --project-dir runs/$(date +%Y-%m-%d)_{capability.lower().replace(' ', '-')} \\
       --model sonnet \\
       --max-iterations 20

💡 Documentation goes in knowledge-base/, not here!
""")


def generate_replacements(source_exp: str, target_exp: str, exp_num: int) -> List[Tuple[str, str]]:
    """Generate string replacements for updating references."""
    # Try to extract source number
    source_match = re.search(r'(\d+)', source_exp)
    source_num = int(source_match.group(1)) if source_match else 4

    return [
        # Experiment names
        (f"Experiment {source_num:02d}", f"Experiment {exp_num:02d}"),
        (f"Experiment {source_num}", f"Experiment {exp_num}"),
        (f"EXPERIMENT {source_num:02d}", f"EXPERIMENT {exp_num:02d}"),
        (f"EXPERIMENT {source_num}", f"EXPERIMENT {exp_num}"),

        # File prefixes
        (f"EXP_{source_num:02d}", f"EXP_{exp_num:02d}"),
        (f"EXP_{source_num}", f"EXP_{exp_num}"),

        # Directory patterns (for any remaining nested refs)
        (f"experiment_{source_num:02d}", f"experiment_{exp_num:02d}"),
        (f"experiment_{source_num}", f"experiment_{exp_num}"),
    ]


def update_all_files(target_path: Path, replacements: List[Tuple[str, str]]) -> None:
    """Update text files with replacements."""
    text_extensions = {'.md', '.txt', '.py', '.json', '.sh'}

    for file_path in target_path.rglob('*'):
        if not file_path.is_file():
            continue
        if file_path.suffix not in text_extensions:
            continue
        if '__pycache__' in file_path.parts or '.git' in file_path.parts:
            continue

        try:
            content = file_path.read_text()
            updated = content

            for old, new in replacements:
                updated = updated.replace(old, new)

            if updated != content:
                file_path.write_text(updated)
                print(f"    Updated: {file_path.name}")

        except (UnicodeDecodeError, PermissionError):
            pass


def update_phase_constraint(target_path: Path, capability: str) -> None:
    """Update phase_constraint.txt with new capability."""
    constraint_file = target_path / "prompts" / "phase_constraint.txt"

    if not constraint_file.exists():
        print(f"    ⚠  phase_constraint.txt not found")
        return

    content = constraint_file.read_text()

    # Replace capability references
    content = re.sub(
        r'You must implement:\n- [^\n]+',
        f'You must implement:\n- {capability}',
        content
    )

    content = re.sub(
        r'You must choose EXACTLY ONE capability from:\n- [^\n]+',
        f'You must implement:\n- {capability}',
        content
    )

    constraint_file.write_text(content)


def rename_manifesto(target_path: Path, exp_num: int) -> None:
    """Rename manifesto file to match new experiment number."""
    prompts_dir = target_path / "prompts"

    for old_manifesto in prompts_dir.glob("EXP_*_MANIFESTO.md"):
        new_name = f"EXP_{exp_num:02d}_MANIFESTO.md"
        new_path = prompts_dir / new_name
        if old_manifesto.name != new_name:
            old_manifesto.rename(new_path)
            print(f"    Renamed: {old_manifesto.name} → {new_name}")


def main():
    parser = argparse.ArgumentParser(
        description='Set up new experiment with FLAT structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create experiment 05 from source of truth (exp-04)
  python setup_new_experiment.py \\
    --source 04-argument-quality \\
    --target 05-evidence-detection \\
    --capability "Evidence Detection" \\
    --num 5

  # The script will:
  # - Validate source has all critical features
  # - Create FLAT structure (no experiment_XX nesting)
  # - Copy all necessary files
  # - Create symlinks to _shared/
  # - Update references
  # - Run feature parity check
"""
    )

    parser.add_argument(
        '--source', required=True,
        help='Source experiment (e.g., 04-argument-quality)'
    )
    parser.add_argument(
        '--target', required=True,
        help='Target experiment (e.g., 05-evidence-detection)'
    )
    parser.add_argument(
        '--capability', required=True,
        help='Capability name (e.g., "Evidence Detection")'
    )
    parser.add_argument(
        '--num', type=int, required=True,
        help='Experiment number (e.g., 5)'
    )
    parser.add_argument(
        '--base-dir', type=Path,
        help='Base experiments directory (optional)'
    )

    args = parser.parse_args()

    try:
        setup_experiment(
            source_exp=args.source,
            target_exp=args.target,
            capability=args.capability,
            exp_num=args.num,
            base_dir=args.base_dir
        )
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
