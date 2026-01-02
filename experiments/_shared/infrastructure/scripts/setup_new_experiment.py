#!/usr/bin/env python3
"""
Automated Experiment Setup Script

Creates a new experiment by copying an existing one and updating all references
to avoid naming bugs like the EXP_02_MANIFESTO.md issue.

Usage:
    python scripts/setup_new_experiment.py --source exp-02 --target exp-04 --capability "Claim Detection" --num 4
"""

import argparse
import shutil
import re
from pathlib import Path
from typing import List, Tuple


def setup_experiment(
    source_exp: str,
    target_exp: str,
    capability: str,
    exp_num: int,
    base_dir: Path = None
) -> None:
    """
    Set up a new experiment by copying and updating an existing one.

    Args:
        source_exp: Source experiment directory name (e.g., 'exp-02')
        target_exp: Target experiment directory name (e.g., 'exp-04')
        capability: Name of capability to implement (e.g., 'Claim Detection')
        exp_num: Experiment number (e.g., 4)
        base_dir: Base experiments directory (defaults to parent of parent)
    """
    if base_dir is None:
        # Default: /workspaces/claude-quickstarts/experiments/
        base_dir = Path(__file__).parent.parent.parent.parent

    source_path = base_dir / source_exp
    target_path = base_dir / target_exp

    print(f"=== Setting up {target_exp} from {source_exp} ===")
    print(f"Capability: {capability}")
    print(f"Experiment Number: {exp_num}")
    print()

    # Step 1: Validate source exists
    if not source_path.exists():
        raise FileNotFoundError(f"Source experiment not found: {source_path}")

    # Step 2: Check target doesn't exist
    if target_path.exists():
        raise FileExistsError(f"Target experiment already exists: {target_path}")

    # Step 3: Create target root directory
    print(f"✓ Creating {target_path}")
    target_path.mkdir(parents=True)

    # Step 4: Create symlinks for shared resources
    print("✓ Creating symlinks to shared resources...")
    (target_path / "deep-wiki-spec-files").symlink_to("../exp-02/deep-wiki-spec-files")
    (target_path / "reference-files").symlink_to("../exp-02/reference-files")

    # Step 5: Copy experiment working directory
    source_work_dir = get_latest_experiment_dir(source_path)
    target_work_name = f"experiment_{exp_num:02d}"
    target_work_dir = target_path / target_work_name

    print(f"✓ Copying {source_work_dir.name} → {target_work_name}")
    shutil.copytree(source_work_dir, target_work_dir)

    # Step 6: Clean up non-essential files
    print("✓ Cleaning up runs/, reports/, generations/...")
    for cleanup_dir in ["runs", "reports", "generations"]:
        cleanup_path = target_work_dir / cleanup_dir
        if cleanup_path.exists():
            shutil.rmtree(cleanup_path)
            cleanup_path.mkdir()
            (cleanup_path / "archive").mkdir()

    # Step 7: Update all file references
    print("✓ Updating file references...")
    replacements = generate_replacements(source_exp, target_exp, exp_num)
    update_all_files(target_work_dir, replacements)

    # Step 8: Update phase_constraint.txt for new capability
    print(f"✓ Updating phase_constraint.txt for '{capability}'...")
    update_phase_constraint(target_work_dir, capability)

    # Step 9: Validate all file references
    print("✓ Validating file references...")
    validation_errors = validate_file_references(target_work_dir)

    if validation_errors:
        print(f"\n⚠ WARNING: Found {len(validation_errors)} validation errors:")
        for error in validation_errors:
            print(f"  - {error}")
        print("\nPlease fix these before running the experiment.")
    else:
        print("✓ All file references validated successfully")

    # Step 10: Generate setup summary
    print("\n" + "="*60)
    print(f"✅ Experiment {exp_num} setup complete!")
    print("="*60)
    print(f"\nLocation: {target_work_dir}")
    print(f"Capability: {capability}")
    print("\nNext steps:")
    print(f"  1. cd {target_work_dir.relative_to(Path.cwd())}")
    print(f"  2. Review and customize prompts if needed")
    print(f"  3. Run: python scripts/autonomous_agent_demo.py --project-dir runs/YYYY-MM-DD_run-name --model sonnet --max-iterations 20")


def get_latest_experiment_dir(exp_path: Path) -> Path:
    """Find the latest experiment_XX directory in the experiment path."""
    experiment_dirs = list(exp_path.glob("experiment_*"))
    if not experiment_dirs:
        raise FileNotFoundError(f"No experiment_* directories found in {exp_path}")

    # Sort by directory name (experiment_02, experiment_03, etc.)
    experiment_dirs.sort()
    return experiment_dirs[-1]


def generate_replacements(source_exp: str, target_exp: str, exp_num: int) -> List[Tuple[str, str]]:
    """Generate list of (old, new) string replacements."""
    # Extract experiment numbers
    source_num = int(re.search(r'\d+', source_exp).group())

    return [
        # Experiment names
        (f"Experiment {source_num:02d}", f"Experiment {exp_num:02d}"),
        (f"Experiment {source_num}", f"Experiment {exp_num}"),
        (f"EXPERIMENT {source_num:02d}", f"EXPERIMENT {exp_num:02d}"),
        (f"EXPERIMENT {source_num}", f"EXPERIMENT {exp_num}"),

        # File prefixes
        (f"EXP_{source_num:02d}", f"EXP_{exp_num:02d}"),
        (f"EXPERIMENT_{source_num:02d}", f"EXPERIMENT_{exp_num:02d}"),

        # Directory names
        (f"experiment_{source_num:02d}", f"experiment_{exp_num:02d}"),
        (f"exp-{source_num:02d}", f"exp-{exp_num:02d}"),
    ]


def update_all_files(work_dir: Path, replacements: List[Tuple[str, str]]) -> None:
    """Update all text files with the given replacements."""
    text_extensions = {'.md', '.txt', '.py', '.json', '.sh'}

    for file_path in work_dir.rglob('*'):
        if not file_path.is_file():
            continue

        if file_path.suffix not in text_extensions:
            continue

        # Skip __pycache__ and .git directories
        if '__pycache__' in file_path.parts or '.git' in file_path.parts:
            continue

        try:
            content = file_path.read_text()
            updated = content

            for old, new in replacements:
                updated = updated.replace(old, new)

            if updated != content:
                file_path.write_text(updated)
                print(f"    Updated: {file_path.relative_to(work_dir)}")

        except (UnicodeDecodeError, PermissionError):
            # Skip binary files or files we can't read
            pass


def update_phase_constraint(work_dir: Path, capability: str) -> None:
    """Update phase_constraint.txt with the new capability."""
    constraint_file = work_dir / "prompts" / "phase_constraint.txt"

    if not constraint_file.exists():
        print(f"    Warning: {constraint_file} not found")
        return

    content = constraint_file.read_text()

    # Find the capability line and replace it
    # Look for pattern like: "- Key Point Analysis" or "- Evidence Detection"
    content = re.sub(
        r'(You must choose EXACTLY ONE capability from:\n)- [^\n]+',
        f'\\1- {capability}',
        content
    )

    # Update the note about expected complexity if present
    content = re.sub(
        r'NOTE: [^\n]+ is more complex than [^\n]+\.',
        f'NOTE: {capability} capability for Experiment.',
        content
    )

    constraint_file.write_text(content)


def validate_file_references(work_dir: Path) -> List[str]:
    """
    Validate that all file references in prompts actually exist.
    Returns list of validation errors.
    """
    errors = []
    prompts_dir = work_dir / "prompts"

    if not prompts_dir.exists():
        return [f"Prompts directory not found: {prompts_dir}"]

    # Pattern to match file references in markdown
    # Matches: ../../../path/to/file.md or ./file.json or file.py
    file_ref_pattern = r'(?:\.\.\/)+[^\s\)]+\.[a-zA-Z]+|\.\/[^\s\)]+\.[a-zA-Z]+|(?<!\w)[A-Z_]+\w*\.(md|json|txt|py)'

    for prompt_file in prompts_dir.glob('*.md'):
        content = prompt_file.read_text()

        # Find all potential file references
        refs = re.findall(file_ref_pattern, content)

        for ref in refs:
            # Handle tuple from regex groups
            if isinstance(ref, tuple):
                ref = ref[0] if ref[0] else ref[1]

            # Resolve path relative to work_dir
            if ref.startswith('../'):
                # Relative path
                ref_path = work_dir / ref
            elif ref.startswith('./'):
                # Current directory
                ref_path = work_dir / ref[2:]
            else:
                # Assume it's in current directory
                ref_path = work_dir / ref

            # Normalize path
            try:
                ref_path = ref_path.resolve()
                if not ref_path.exists():
                    errors.append(
                        f"{prompt_file.name}: Referenced file does not exist: {ref}"
                    )
            except (OSError, ValueError):
                # Path resolution failed
                pass

    return errors


def main():
    parser = argparse.ArgumentParser(
        description='Set up a new experiment from an existing one'
    )
    parser.add_argument(
        '--source',
        required=True,
        help='Source experiment directory name (e.g., exp-02)'
    )
    parser.add_argument(
        '--target',
        required=True,
        help='Target experiment directory name (e.g., exp-04)'
    )
    parser.add_argument(
        '--capability',
        required=True,
        help='Name of capability to implement (e.g., "Claim Detection")'
    )
    parser.add_argument(
        '--num',
        type=int,
        required=True,
        help='Experiment number (e.g., 4)'
    )
    parser.add_argument(
        '--base-dir',
        type=Path,
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
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
