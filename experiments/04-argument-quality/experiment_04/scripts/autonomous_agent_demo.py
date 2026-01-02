#!/usr/bin/env python3
"""
Autonomous Coding Agent Demo - Experiment 04: Document-Driven Derivation
=========================================================================

A minimal harness demonstrating long-running autonomous coding with Claude.
This version enforces DERIVATION instead of INVENTION - all specifications
must come from canonical artifacts, not agent imagination.

Example Usage:
    python autonomous_agent_demo.py --project-dir ./evidence_detection
    python autonomous_agent_demo.py --project-dir ./evidence_detection --max-iterations 5
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent import run_autonomous_agent


def load_env_file() -> None:
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    # Remove quotes if present
                    value = value.strip().strip('"').strip("'")
                    # Only set if not already set in environment
                    if key.strip() and not os.environ.get(key.strip()):
                        os.environ[key.strip()] = value


# Configuration
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"  # For standard Anthropic API
DEFAULT_FOUNDRY_MODEL = "claude-sonnet-4-5"   # Common Foundry deployment name


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Experiment 04: Document-Driven Derivation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXPERIMENT 04: DERIVATION, NOT INVENTION
=========================================

This experiment enforces that all specifications are DERIVED from
canonical artifacts:
  - DeepWiki documentation (theory/intent)
  - Example files (behavioral witnesses)
  - Client code structure (architectural boundaries)

Agents may NOT invent capabilities, inputs, outputs, or architectures.

Examples:
  # Start fresh project (Evidence Detection phase)
  python autonomous_agent_demo.py --project-dir ./evidence_detection

  # Limit iterations for testing
  python autonomous_agent_demo.py --project-dir ./evidence_detection --max-iterations 5

Environment Variables:
  Standard Anthropic API:
    ANTHROPIC_API_KEY            Your Anthropic API key

  Azure Foundry:
    ANTHROPIC_FOUNDRY_API_KEY    Your Azure Foundry API key
    CLAUDE_CODE_USE_FOUNDRY      Set to 1 to use Azure Foundry
    ANTHROPIC_FOUNDRY_RESOURCE   Your Azure Foundry resource name
    CLAUDE_MODEL                 Your deployment name
        """,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path("./evidence_detection"),
        help="Directory for the project (default: generations/evidence_detection)",
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
        default=None,
        help="Claude model/deployment to use",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    # Load .env file if present
    load_env_file()

    args = parse_args()

    # Check for API key (supports both standard and Azure Foundry)
    has_standard_key = os.environ.get("ANTHROPIC_API_KEY")
    has_foundry_key = os.environ.get("ANTHROPIC_FOUNDRY_API_KEY")
    use_foundry = os.environ.get("CLAUDE_CODE_USE_FOUNDRY") == "1"

    if not has_standard_key and not has_foundry_key:
        print("Error: No API key found")
        print("\nFor standard Anthropic API:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nFor Azure Foundry:")
        print("  export ANTHROPIC_FOUNDRY_API_KEY='your-api-key'")
        print("  export CLAUDE_CODE_USE_FOUNDRY=1")
        print("  export ANTHROPIC_FOUNDRY_RESOURCE='your-resource-name'")
        print("  export CLAUDE_MODEL='your-deployment-name'")
        return

    # Determine model to use
    model = args.model or os.environ.get("CLAUDE_MODEL")

    if not model:
        if use_foundry:
            model = DEFAULT_FOUNDRY_MODEL
            print(f"No model specified, using Foundry default: {model}")
        else:
            model = DEFAULT_MODEL

    print(f"Using model/deployment: {model}")
    if use_foundry:
        print("(Azure Foundry mode)")
    print()

    # Handle project directory paths
    project_dir = args.project_dir

    # If absolute path, use as-is
    if project_dir.is_absolute():
        pass
    # If relative path starting with "runs/", use as-is (new structure)
    elif str(project_dir).startswith("runs/"):
        pass
    # If just a directory name, place in runs/ (new structure)
    elif "/" not in str(project_dir):
        project_dir = Path("runs") / project_dir
    # Otherwise use as provided (for backwards compatibility)
    else:
        pass

    # Run the agent
    try:
        asyncio.run(
            run_autonomous_agent(
                project_dir=project_dir,
                model=model,
                max_iterations=args.max_iterations,
            )
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        print("To resume, run the same command again")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()
