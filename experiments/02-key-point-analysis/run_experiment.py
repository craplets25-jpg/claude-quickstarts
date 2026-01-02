#!/usr/bin/env python3
"""
Experiment 02: Key Point Analysis - Run Wrapper
================================================

This wrapper script uses shared infrastructure from _shared/infrastructure/
to run the Key Point Analysis experiment.

Usage:
    python run_experiment.py --project-dir outputs/runs/my-run
    python run_experiment.py --project-dir outputs/runs/my-run --max-iterations 10
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add shared infrastructure to Python path
EXPERIMENT_DIR = Path(__file__).parent
SHARED_INFRA = EXPERIMENT_DIR.parent / "_shared" / "infrastructure"
sys.path.insert(0, str(SHARED_INFRA))

# Import from shared infrastructure
from core import run_autonomous_agent

# Configuration
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


def load_env_file() -> None:
    """Load environment variables from .env file if it exists."""
    env_file = EXPERIMENT_DIR / "config" / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    value = value.strip().strip('"').strip("'")
                    if key.strip() and not os.environ.get(key.strip()):
                        os.environ[key.strip()] = value


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Experiment 02: Key Point Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXPERIMENT 02: KEY POINT ANALYSIS
==================================

Implements Key Point Analysis capability using document-driven derivation.

Structure:
  config/         - Configuration (prompts, settings)
  outputs/runs/   - Experiment runs (isolated git repos)
  outputs/reports/- Analysis reports
  notes/          - Human documentation

Examples:
  # Start new run
  python run_experiment.py --project-dir outputs/runs/kpa-test

  # Resume existing run
  python run_experiment.py --project-dir outputs/runs/kpa-test

  # Limit iterations for testing
  python run_experiment.py --project-dir outputs/runs/kpa-test --max-iterations 5

Environment Variables:
  ANTHROPIC_API_KEY            Your Anthropic API key
  CLAUDE_CODE_USE_FOUNDRY      Set to 1 to use Azure Foundry
  ANTHROPIC_FOUNDRY_API_KEY    Your Azure Foundry API key
  ANTHROPIC_FOUNDRY_RESOURCE   Your Azure Foundry resource name
  CLAUDE_MODEL                 Your deployment name
        """,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        required=True,
        help="Directory for the project run (will be created in outputs/runs/)",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of agent iterations (default: unlimited)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )

    return parser.parse_args()


async def main():
    """Main entry point."""
    # Load environment variables
    load_env_file()

    # Parse arguments
    args = parse_args()

    # Ensure API key is set
    if not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("ANTHROPIC_FOUNDRY_API_KEY"):
        print("\n❌ Error: ANTHROPIC_API_KEY or ANTHROPIC_FOUNDRY_API_KEY must be set")
        print("\nSet it in one of these ways:")
        print("  1. export ANTHROPIC_API_KEY=your_key")
        print("  2. Create config/.env with ANTHROPIC_API_KEY=your_key")
        sys.exit(1)

    # Determine config directory (this experiment's config/)
    config_dir = EXPERIMENT_DIR / "config"

    # Resolve project directory (make it absolute if relative)
    project_dir = args.project_dir
    if not project_dir.is_absolute():
        project_dir = EXPERIMENT_DIR / project_dir

    # Run the autonomous agent
    await run_autonomous_agent(
        project_dir=project_dir,
        config_dir=config_dir,
        model=args.model,
        max_iterations=args.max_iterations,
    )


if __name__ == "__main__":
    asyncio.run(main())
