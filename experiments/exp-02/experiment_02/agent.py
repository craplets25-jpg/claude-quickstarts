"""
Agent Session Logic
===================

Core agent interaction functions for running autonomous coding sessions.

Pipeline: SPEC LIBRARIAN → SPEC REVIEWER → CODING AGENT

Features:
- Comprehensive logging of all agent interactions
- Decision tracking for post-hoc analysis
- Real-time monitoring support via live.log
"""

import asyncio
from pathlib import Path
from typing import Optional

from claude_code_sdk import ClaudeSDKClient

from client import create_client
from progress import print_session_header, print_progress_summary
from prompts import (
    get_initializer_prompt,
    get_reviewer_prompt,
    get_coding_prompt,
    copy_spec_to_project,
)
from experiment_logger import ExperimentLogger


# Configuration
AUTO_CONTINUE_DELAY_SECONDS = 3


def determine_session_type(project_dir: Path) -> str:
    """
    Determine which session type to run based on project state.

    Returns:
        "SPEC LIBRARIAN" - if no requirement_cards.json exists
        "SPEC REVIEWER" - if requirement_cards.json exists but no review_notes.txt
        "CODING AGENT" - if both exist (specs are reviewed and ready)
    """
    requirement_cards = project_dir / "requirement_cards.json"
    review_notes = project_dir / "review_notes.txt"
    feature_list = project_dir / "feature_list.json"

    if not requirement_cards.exists() or not feature_list.exists():
        return "SPEC LIBRARIAN"
    elif not review_notes.exists():
        return "SPEC REVIEWER"
    else:
        return "CODING AGENT"


async def run_agent_session(
    client: ClaudeSDKClient,
    message: str,
    project_dir: Path,
    logger: Optional[ExperimentLogger] = None,
) -> tuple[str, str]:
    """
    Run a single agent session using Claude Agent SDK.

    Args:
        client: Claude SDK client
        message: The prompt to send
        project_dir: Project directory path
        logger: Optional experiment logger for tracking interactions

    Returns:
        (status, response_text) where status is:
        - "continue" if agent should continue working
        - "error" if an error occurred
    """
    print("Sending prompt to Claude Agent SDK...\n")

    # Track pending tool calls for logging
    pending_tool_calls = {}

    try:
        # Send the query
        await client.query(message)

        # Collect response text and show tool use
        response_text = ""
        async for msg in client.receive_response():
            msg_type = type(msg).__name__

            # Handle AssistantMessage (text and tool use)
            if msg_type == "AssistantMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    block_type = type(block).__name__

                    if block_type == "TextBlock" and hasattr(block, "text"):
                        response_text += block.text
                        print(block.text, end="", flush=True)

                        # Log thoughts/reasoning if they contain decision indicators
                        if logger and any(kw in block.text.lower() for kw in
                                         ["i will", "i'll", "deciding", "choosing",
                                          "my approach", "strategy", "plan is"]):
                            # Extract a summary for logging
                            text_preview = block.text[:200].replace('\n', ' ')
                            logger.log_thought(text_preview)

                    elif block_type == "ToolUseBlock" and hasattr(block, "name"):
                        tool_name = block.name
                        tool_id = getattr(block, "id", str(id(block)))
                        tool_input = getattr(block, "input", {})

                        print(f"\n[Tool: {tool_name}]", flush=True)
                        if hasattr(block, "input"):
                            input_str = str(block.input)
                            if len(input_str) > 200:
                                print(f"   Input: {input_str[:200]}...", flush=True)
                            else:
                                print(f"   Input: {input_str}", flush=True)

                        # Store pending tool call for result matching
                        pending_tool_calls[tool_id] = {
                            "name": tool_name,
                            "input": tool_input if isinstance(tool_input, dict) else {"raw": str(tool_input)}
                        }

            # Handle UserMessage (tool results)
            elif msg_type == "UserMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    block_type = type(block).__name__

                    if block_type == "ToolResultBlock":
                        result_content = getattr(block, "content", "")
                        is_error = getattr(block, "is_error", False)
                        tool_use_id = getattr(block, "tool_use_id", None)

                        # Check if command was blocked by security hook
                        blocked = "blocked" in str(result_content).lower()

                        if blocked:
                            print(f"   [BLOCKED] {result_content}", flush=True)
                        elif is_error:
                            # Show errors (truncated)
                            error_str = str(result_content)[:500]
                            print(f"   [Error] {error_str}", flush=True)
                        else:
                            # Tool succeeded - just show brief confirmation
                            print("   [Done]", flush=True)

                        # Log the tool call with result
                        if logger and tool_use_id and tool_use_id in pending_tool_calls:
                            tool_info = pending_tool_calls[tool_use_id]
                            logger.log_tool_call(
                                tool_name=tool_info["name"],
                                inputs=tool_info["input"],
                                output=str(result_content)[:500] if result_content else None,
                                is_error=is_error,
                                blocked=blocked
                            )

                            # Track artifact modifications
                            if tool_info["name"] in ("Edit", "Write"):
                                file_path = tool_info["input"].get("file_path", "unknown")
                                if tool_info["name"] == "Write":
                                    logger.log_artifact_created(file_path)
                                else:
                                    logger.log_artifact_modified(file_path)

                            del pending_tool_calls[tool_use_id]

        print("\n" + "-" * 70 + "\n")
        return "continue", response_text

    except Exception as e:
        error_msg = str(e)
        print(f"Error during agent session: {error_msg}")
        if logger:
            logger.log_error("Session error", error_msg)
        return "error", error_msg


async def run_autonomous_agent(
    project_dir: Path,
    model: str,
    max_iterations: Optional[int] = None,
) -> None:
    """
    Run the autonomous agent loop.

    Pipeline:
    1. SPEC LIBRARIAN - Derives requirements from canonical artifacts
    2. SPEC REVIEWER - Filters tech-specific details to legacy_notes
    3. CODING AGENT - Implements behavior-only requirements

    Args:
        project_dir: Directory for the project
        model: Claude model to use
        max_iterations: Maximum number of iterations (None for unlimited)
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 02: DOCUMENT-DRIVEN DERIVATION")
    print("=" * 70)
    print(f"\nProject directory: {project_dir}")
    print(f"Model: {model}")
    if max_iterations:
        print(f"Max iterations: {max_iterations}")
    else:
        print("Max iterations: Unlimited (will run until completion)")
    print()

    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)

    # Initialize logger
    logger = ExperimentLogger(project_dir)
    logger.log_info("Experiment started", {
        "project_dir": str(project_dir),
        "model": model,
        "max_iterations": max_iterations,
    })

    # Determine initial session type
    session_type = determine_session_type(project_dir)
    previous_session_type = None

    if session_type == "SPEC LIBRARIAN":
        print("Fresh start - will use Spec Librarian agent")
        print()
        print("=" * 70)
        print("  PIPELINE: SPEC LIBRARIAN → SPEC REVIEWER → CODING AGENT")
        print("  ")
        print("  Stage 1: Derive requirements from canonical artifacts")
        print("  Stage 2: Filter tech-specific details to legacy_notes")
        print("  Stage 3: Implement behavior-only requirements")
        print("=" * 70)
        print()
        # Copy the constraint files into the project directory
        copy_spec_to_project(project_dir)
        logger.log_decision(
            "Starting with SPEC LIBRARIAN phase",
            reasoning="No requirement_cards.json exists - fresh start"
        )
    elif session_type == "SPEC REVIEWER":
        print("Specs exist - will run Spec Reviewer to filter tech details")
        print()
        logger.log_decision(
            "Starting with SPEC REVIEWER phase",
            reasoning="requirement_cards.json exists but no review_notes.txt"
        )
    else:
        print("Specs reviewed - continuing with Coding Agent")
        print_progress_summary(project_dir)
        logger.log_decision(
            "Starting with CODING AGENT phase",
            reasoning="Both requirement_cards.json and review_notes.txt exist"
        )

    # Main loop
    iteration = 0

    while True:
        iteration += 1

        # Check max iterations
        if max_iterations and iteration > max_iterations:
            print(f"\nReached max iterations ({max_iterations})")
            print("To continue, run the script again without --max-iterations")
            logger.log_info("Reached max iterations", {"max": max_iterations})
            break

        # Determine session type for this iteration
        session_type = determine_session_type(project_dir)

        # Check if all tests are passing (early stopping condition)
        if session_type == "CODING AGENT" and iteration > 3:
            progress = get_progress(project_dir)
            if progress['total'] > 0 and progress['passing'] == progress['total']:
                print(f"\n✅ All tests passing ({progress['passing']}/{progress['total']})!")
                print("Implementation complete. Stopping experiment.")
                logger.log_info("Early stop: All tests passing", {
                    "passing": progress['passing'],
                    "total": progress['total'],
                    "percentage": 100.0
                })
                logger.end_session(status="completed", summary="All tests passing - implementation complete")
                break

        # Log phase transitions
        if previous_session_type and previous_session_type != session_type:
            logger.log_phase_transition(
                from_phase=previous_session_type,
                to_phase=session_type,
                reason=f"Pipeline progression after iteration {iteration - 1}"
            )

        # Print session header
        print_session_header(iteration, session_type)

        # Start logging session
        session_id = logger.start_session(session_type, iteration)
        logger.log_info(f"Session {session_id} started")

        # Create client (fresh context)
        client = create_client(project_dir, model)

        # Choose prompt based on session type
        if session_type == "SPEC LIBRARIAN":
            prompt = get_initializer_prompt()
            logger.log_decision(
                "Using Spec Librarian prompt",
                reasoning="Deriving requirements from canonical artifacts"
            )
        elif session_type == "SPEC REVIEWER":
            prompt = get_reviewer_prompt()
            logger.log_decision(
                "Using Spec Reviewer prompt",
                reasoning="Filtering tech-specific details to legacy_notes"
            )
        else:
            prompt = get_coding_prompt()
            logger.log_decision(
                "Using Coding Agent prompt",
                reasoning="Implementing behavior-only requirements"
            )

        # Run session with async context manager
        async with client:
            status, response = await run_agent_session(client, prompt, project_dir, logger)

        # Handle status
        if status == "continue":
            print(f"\nAgent will auto-continue in {AUTO_CONTINUE_DELAY_SECONDS}s...")
            print_progress_summary(project_dir)
            logger.end_session("completed", f"Session completed successfully")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        elif status == "error":
            print("\nSession encountered an error")
            print("Will retry with a fresh session...")
            logger.end_session("error", f"Session encountered an error")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        previous_session_type = session_type

        # Small delay between sessions
        if max_iterations is None or iteration < max_iterations:
            print("\nPreparing next session...\n")
            await asyncio.sleep(1)

    # Final summary
    print("\n" + "=" * 70)
    print("  SESSION COMPLETE")
    print("=" * 70)
    print(f"\nProject directory: {project_dir}")
    print_progress_summary(project_dir)

    # Log final summary
    logger.log_info("Experiment completed", {
        "total_iterations": iteration,
        "final_phase": session_type,
    })

    print(f"\nLogs available at: {project_dir}/logs/")
    print("  - live.log: Real-time activity log")
    print("  - decisions.md: Human-readable decisions")
    print("  - experiment_log.jsonl: Session summaries")
    print("\nDone!")
