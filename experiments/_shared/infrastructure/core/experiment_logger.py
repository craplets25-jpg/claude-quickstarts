"""
Experiment Logger
=================

Comprehensive logging system for capturing agent interactions, decisions,
and thought processes during autonomous coding sessions.

Features:
- Structured JSON logs for each session
- Tool call logging with inputs/outputs
- Decision tracking (what the agent chose and why)
- Phase transition logging
- Real-time file writing for live monitoring
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class LogLevel(Enum):
    """Log levels for filtering and display."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    DECISION = "DECISION"
    TOOL = "TOOL"
    ERROR = "ERROR"
    MILESTONE = "MILESTONE"


@dataclass
class LogEntry:
    """A single log entry with structured data."""
    timestamp: str
    level: str
    category: str
    message: str
    data: Optional[dict] = None
    session_id: str = ""
    iteration: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "timestamp": self.timestamp,
            "level": self.level,
            "category": self.category,
            "message": self.message,
            "session_id": self.session_id,
            "iteration": self.iteration,
        }
        if self.data:
            result["data"] = self.data
        return result


@dataclass
class SessionLog:
    """Complete log for a single agent session."""
    session_id: str
    session_type: str  # SPEC LIBRARIAN, SPEC REVIEWER, CODING AGENT
    iteration: int
    start_time: str
    end_time: Optional[str] = None
    status: str = "running"  # running, completed, error
    entries: list = field(default_factory=list)
    tool_calls: list = field(default_factory=list)
    decisions: list = field(default_factory=list)
    artifacts_created: list = field(default_factory=list)
    artifacts_modified: list = field(default_factory=list)
    summary: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "session_type": self.session_type,
            "iteration": self.iteration,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "entries": [e.to_dict() if hasattr(e, 'to_dict') else e for e in self.entries],
            "tool_calls": self.tool_calls,
            "decisions": self.decisions,
            "artifacts_created": self.artifacts_created,
            "artifacts_modified": self.artifacts_modified,
            "summary": self.summary,
        }


class ExperimentLogger:
    """
    Main logger class for experiment sessions.

    Usage:
        logger = ExperimentLogger(project_dir)
        logger.start_session("SPEC LIBRARIAN", iteration=1)
        logger.log_decision("Chose Evidence Detection as starting capability")
        logger.log_tool_call("Read", {"file_path": "..."}, "file contents...")
        logger.end_session()
    """

    def __init__(self, project_dir: Path):
        """Initialize logger for a project directory."""
        self.project_dir = Path(project_dir)
        self.logs_dir = self.project_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.current_session: Optional[SessionLog] = None
        self.session_counter = 0

        # Create master log file path
        self.master_log_path = self.logs_dir / "experiment_log.jsonl"
        self.decisions_log_path = self.logs_dir / "decisions.md"
        self.live_log_path = self.logs_dir / "live.log"
        self.agent_thoughts_path = self.logs_dir / "agent-thoughts.log"

    def _timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    def _generate_session_id(self, session_type: str, iteration: int) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = {
            "SPEC LIBRARIAN": "LIB",
            "SPEC REVIEWER": "REV",
            "CODING AGENT": "CODE",
        }.get(session_type, "SESS")
        return f"{prefix}_{iteration:03d}_{timestamp}"

    def start_session(self, session_type: str, iteration: int) -> str:
        """
        Start a new logging session.

        Args:
            session_type: One of "SPEC LIBRARIAN", "SPEC REVIEWER", "CODING AGENT"
            iteration: The iteration number

        Returns:
            The session ID
        """
        self.session_counter += 1
        session_id = self._generate_session_id(session_type, iteration)

        self.current_session = SessionLog(
            session_id=session_id,
            session_type=session_type,
            iteration=iteration,
            start_time=self._timestamp(),
        )

        # Log session start
        self._log_entry(LogLevel.MILESTONE, "session", f"Session started: {session_type}")

        # Write to decisions log
        self._write_decisions_header(session_type, iteration)

        return session_id

    def end_session(self, status: str = "completed", summary: Optional[str] = None) -> None:
        """End the current session and finalize logs."""
        if not self.current_session:
            return

        self.current_session.end_time = self._timestamp()
        self.current_session.status = status
        self.current_session.summary = summary

        # Log session end
        self._log_entry(LogLevel.MILESTONE, "session", f"Session ended: {status}")

        # Write session log to file
        self._write_session_log()

        # Write to master log
        self._append_to_master_log()

        self.current_session = None

    def log_decision(self, decision: str, reasoning: Optional[str] = None,
                     options_considered: Optional[list] = None) -> None:
        """
        Log a decision made by the agent.

        Args:
            decision: What was decided
            reasoning: Why this decision was made
            options_considered: Other options that were considered
        """
        if not self.current_session:
            return

        decision_entry = {
            "timestamp": self._timestamp(),
            "decision": decision,
            "reasoning": reasoning,
            "options_considered": options_considered,
        }

        self.current_session.decisions.append(decision_entry)

        data = {"reasoning": reasoning} if reasoning else None
        self._log_entry(LogLevel.DECISION, "decision", decision, data)

        # Append to decisions markdown
        self._append_decision_to_md(decision, reasoning, options_considered)

    def log_tool_call(self, tool_name: str, inputs: dict,
                      output: Optional[str] = None,
                      is_error: bool = False,
                      blocked: bool = False) -> None:
        """
        Log a tool call with its inputs and outputs.

        Args:
            tool_name: Name of the tool called
            inputs: Input parameters
            output: Tool output (may be truncated)
            is_error: Whether the tool call resulted in an error
            blocked: Whether the tool call was blocked by security
        """
        if not self.current_session:
            return

        tool_entry = {
            "timestamp": self._timestamp(),
            "tool": tool_name,
            "inputs": self._sanitize_inputs(inputs),
            "output_preview": self._truncate(output, 500) if output else None,
            "is_error": is_error,
            "blocked": blocked,
        }

        self.current_session.tool_calls.append(tool_entry)

        status = "BLOCKED" if blocked else ("ERROR" if is_error else "OK")
        self._log_entry(
            LogLevel.TOOL,
            "tool_call",
            f"{tool_name} [{status}]",
            {"inputs": self._summarize_inputs(inputs)}
        )

    def log_artifact_created(self, filepath: str, artifact_type: str = "file") -> None:
        """Log when an artifact is created."""
        if not self.current_session:
            return

        self.current_session.artifacts_created.append({
            "timestamp": self._timestamp(),
            "path": filepath,
            "type": artifact_type,
        })

        self._log_entry(LogLevel.INFO, "artifact", f"Created: {filepath}")

    def log_artifact_modified(self, filepath: str, change_summary: Optional[str] = None) -> None:
        """Log when an artifact is modified."""
        if not self.current_session:
            return

        self.current_session.artifacts_modified.append({
            "timestamp": self._timestamp(),
            "path": filepath,
            "change_summary": change_summary,
        })

        self._log_entry(LogLevel.INFO, "artifact", f"Modified: {filepath}")

    def log_phase_transition(self, from_phase: str, to_phase: str, reason: str) -> None:
        """Log a pipeline phase transition."""
        self._log_entry(
            LogLevel.MILESTONE,
            "phase_transition",
            f"Transition: {from_phase} → {to_phase}",
            {"reason": reason}
        )

        self._append_decision_to_md(
            f"Phase transition: {from_phase} → {to_phase}",
            reason, None
        )

    def log_thought(self, thought: str) -> None:
        """Log agent's thought process / reasoning."""
        if not self.current_session:
            return

        self._log_entry(LogLevel.DEBUG, "thought", thought)

        # Also write to agent-thoughts.log with readable format
        self._write_agent_thoughts(thought)

    def log_info(self, message: str, data: Optional[dict] = None) -> None:
        """Log general information."""
        self._log_entry(LogLevel.INFO, "info", message, data)

    def log_error(self, message: str, error_details: Optional[str] = None,
                  exception: Optional[Exception] = None, context: Optional[dict] = None) -> None:
        """
        Log an error with full context and traceback.

        Args:
            message: High-level error description
            error_details: Additional error details (optional)
            exception: Exception object to extract traceback from (optional)
            context: Additional context dictionary (optional)

        Example:
            try:
                dangerous_operation()
            except Exception as e:
                logger.log_error(
                    "Failed to process file",
                    exception=e,
                    context={"file_path": path, "operation": "read"}
                )
        """
        import traceback

        # Build error data dictionary
        error_data = {}

        if error_details:
            error_data["details"] = error_details

        if exception:
            error_data["exception_type"] = type(exception).__name__
            error_data["exception_message"] = str(exception)
            error_data["full_traceback"] = traceback.format_exc()

        if context:
            error_data["context"] = context

        self._log_entry(
            LogLevel.ERROR,
            "error",
            message,
            error_data if error_data else None
        )

        # Also print to console for immediate visibility
        print(f"\n{'='*80}")
        print(f"❌ ERROR: {message}")
        if exception:
            print(f"Exception: {type(exception).__name__}: {str(exception)}")
        if context:
            print(f"Context: {context}")
        if exception:
            print(f"\nFull traceback written to: {self.log_dir / 'live.log'}")
            print(f"{'='*80}\n")

    def _log_entry(self, level: LogLevel, category: str, message: str,
                   data: Optional[dict] = None) -> None:
        """Internal method to create and store a log entry."""
        entry = LogEntry(
            timestamp=self._timestamp(),
            level=level.value,
            category=category,
            message=message,
            data=data,
            session_id=self.current_session.session_id if self.current_session else "",
            iteration=self.current_session.iteration if self.current_session else 0,
        )

        if self.current_session:
            self.current_session.entries.append(entry)

        # Write to live log for real-time monitoring
        self._write_live_log(entry)

    def _write_live_log(self, entry: LogEntry) -> None:
        """Write entry to live log file for real-time monitoring."""
        timestamp = entry.timestamp.split("T")[1][:8]  # HH:MM:SS
        level = entry.level.ljust(8)

        line = f"[{timestamp}] {level} | {entry.category}: {entry.message}"
        if entry.data:
            # Add compact data representation
            data_str = json.dumps(entry.data, separators=(',', ':'))
            if len(data_str) > 100:
                data_str = data_str[:100] + "..."
            line += f" | {data_str}"

        with open(self.live_log_path, "a") as f:
            f.write(line + "\n")

    def _write_agent_thoughts(self, thought: str) -> None:
        """Write agent's narrative reasoning to agent-thoughts.log."""
        timestamp = self._timestamp().split("T")[1][:8]  # HH:MM:SS

        # Handle multi-line thoughts with proper indentation
        lines = thought.split('\n')
        with open(self.agent_thoughts_path, "a") as f:
            # First line with timestamp
            f.write(f"[{timestamp}] {lines[0]}\n")
            # Continuation lines indented to align with text
            for line in lines[1:]:
                if line.strip():  # Only write non-empty lines
                    f.write(f"           {line}\n")

    def _write_session_log(self) -> None:
        """Write the current session log to a JSON file."""
        if not self.current_session:
            return

        session_file = self.logs_dir / f"session_{self.current_session.session_id}.json"
        with open(session_file, "w") as f:
            json.dump(self.current_session.to_dict(), f, indent=2)

    def _append_to_master_log(self) -> None:
        """Append session summary to master log (JSONL format)."""
        if not self.current_session:
            return

        summary = {
            "session_id": self.current_session.session_id,
            "session_type": self.current_session.session_type,
            "iteration": self.current_session.iteration,
            "start_time": self.current_session.start_time,
            "end_time": self.current_session.end_time,
            "status": self.current_session.status,
            "tool_calls_count": len(self.current_session.tool_calls),
            "decisions_count": len(self.current_session.decisions),
            "artifacts_created": len(self.current_session.artifacts_created),
            "artifacts_modified": len(self.current_session.artifacts_modified),
        }

        with open(self.master_log_path, "a") as f:
            f.write(json.dumps(summary) + "\n")

    def _write_decisions_header(self, session_type: str, iteration: int) -> None:
        """Write a header for the session in decisions.md."""
        header = f"""

## Session {iteration}: {session_type}
**Started:** {self._timestamp()}

### Decisions Made:
"""
        with open(self.decisions_log_path, "a") as f:
            f.write(header)

    def _append_decision_to_md(self, decision: str, reasoning: Optional[str],
                                options: Optional[list]) -> None:
        """Append a decision to the markdown log."""
        timestamp = self._timestamp().split("T")[1][:8]

        md = f"\n**[{timestamp}]** {decision}\n"
        if reasoning:
            md += f"  - *Reasoning:* {reasoning}\n"
        if options:
            md += f"  - *Options considered:* {', '.join(options)}\n"

        with open(self.decisions_log_path, "a") as f:
            f.write(md)

    def _sanitize_inputs(self, inputs: dict) -> dict:
        """Sanitize inputs to remove sensitive data and truncate large values."""
        sanitized = {}
        for key, value in inputs.items():
            if key.lower() in ("api_key", "password", "secret", "token"):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, str) and len(value) > 1000:
                sanitized[key] = value[:1000] + "... [truncated]"
            else:
                sanitized[key] = value
        return sanitized

    def _summarize_inputs(self, inputs: dict) -> dict:
        """Create a brief summary of inputs for logging."""
        summary = {}
        for key, value in inputs.items():
            if key.lower() in ("api_key", "password", "secret", "token"):
                summary[key] = "[REDACTED]"
            elif isinstance(value, str):
                if len(value) > 50:
                    summary[key] = value[:50] + "..."
                else:
                    summary[key] = value
            else:
                summary[key] = str(value)[:50]
        return summary

    def _truncate(self, text: str, max_length: int) -> str:
        """Truncate text to max length."""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "... [truncated]"


def get_session_summary(project_dir: Path) -> dict:
    """
    Get a summary of all sessions in a project.

    Args:
        project_dir: Project directory

    Returns:
        Dictionary with session statistics
    """
    logs_dir = Path(project_dir) / "logs"
    master_log = logs_dir / "experiment_log.jsonl"

    if not master_log.exists():
        return {"sessions": [], "total": 0}

    sessions = []
    with open(master_log, "r") as f:
        for line in f:
            if line.strip():
                sessions.append(json.loads(line))

    return {
        "sessions": sessions,
        "total": len(sessions),
        "by_type": {
            "SPEC LIBRARIAN": sum(1 for s in sessions if s["session_type"] == "SPEC LIBRARIAN"),
            "SPEC REVIEWER": sum(1 for s in sessions if s["session_type"] == "SPEC REVIEWER"),
            "CODING AGENT": sum(1 for s in sessions if s["session_type"] == "CODING AGENT"),
        }
    }
