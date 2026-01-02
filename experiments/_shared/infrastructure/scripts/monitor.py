#!/usr/bin/env python3
"""
Real-time Experiment Monitor
=============================

Monitors an experiment run and displays updates in a readable format.
Includes live logging, decisions, and tool call tracking.

Usage:
    python monitor.py [project_dir]
    python monitor.py [project_dir] --mode decisions  # Focus on decisions
    python monitor.py [project_dir] --mode live       # Focus on live log

Example:
    python monitor.py generations/test-run-03
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def colorize(text: str, color: str) -> str:
    """Add ANSI color codes to text."""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m',
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def get_file_info(filepath):
    """Get file size and modification time."""
    try:
        stat = filepath.stat()
        size = stat.st_size
        mtime = time.strftime('%H:%M:%S', time.localtime(stat.st_mtime))
        return f"{size:,} bytes, modified {mtime}"
    except:
        return "not found"


def read_file_tail(filepath, lines=20):
    """Read last N lines of a file."""
    try:
        with open(filepath, 'r') as f:
            content = f.readlines()
            return ''.join(content[-lines:])
    except:
        return "(file not found or empty)"


def count_json_items(filepath):
    """Count items in a JSON array file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return len(data)
            elif isinstance(data, dict) and 'tests' in data:
                return len(data['tests'])
            return "not a list"
    except:
        return "error"


def get_session_stats(project_dir: Path) -> dict:
    """Get statistics from the experiment log."""
    log_file = project_dir / 'logs' / 'experiment_log.jsonl'
    stats = {
        'total_sessions': 0,
        'by_type': {},
        'last_session': None,
    }

    if not log_file.exists():
        return stats

    try:
        sessions = []
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip():
                    sessions.append(json.loads(line))

        stats['total_sessions'] = len(sessions)
        for session in sessions:
            session_type = session.get('session_type', 'UNKNOWN')
            stats['by_type'][session_type] = stats['by_type'].get(session_type, 0) + 1

        if sessions:
            stats['last_session'] = sessions[-1]

        return stats
    except:
        return stats


def format_live_log_line(line: str) -> str:
    """Format a live log line with colors."""
    if 'ERROR' in line:
        return colorize(line, 'red')
    elif 'DECISION' in line:
        return colorize(line, 'cyan')
    elif 'MILESTONE' in line:
        return colorize(line, 'magenta')
    elif 'TOOL' in line:
        return colorize(line, 'yellow')
    elif '[Done]' in line or 'OK' in line:
        return colorize(line, 'green')
    elif 'BLOCKED' in line:
        return colorize(line, 'red')
    return line


def show_decisions(project_dir: Path, num_lines: int = 30) -> None:
    """Show the decisions log."""
    decisions_file = project_dir / 'logs' / 'decisions.md'

    if not decisions_file.exists():
        print("  (No decisions logged yet)")
        return

    try:
        with open(decisions_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            # Show last N lines
            for line in lines[-num_lines:]:
                if line.startswith('##'):
                    print(colorize(line, 'bold'))
                elif line.startswith('**'):
                    print(colorize(line, 'cyan'))
                elif line.startswith('  -'):
                    print(colorize(line, 'yellow'))
                else:
                    print(line)
    except Exception as e:
        print(f"  (Error reading decisions: {e})")


def show_live_log(project_dir: Path, num_lines: int = 25) -> None:
    """Show the live activity log."""
    live_file = project_dir / 'logs' / 'live.log'

    if not live_file.exists():
        print("  (No live log yet)")
        return

    try:
        with open(live_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-num_lines:]:
                print(format_live_log_line(line.rstrip()))
    except Exception as e:
        print(f"  (Error reading live log: {e})")


def show_tool_stats(project_dir: Path) -> dict:
    """Get tool call statistics from session logs."""
    logs_dir = project_dir / 'logs'
    tool_counts = {}

    if not logs_dir.exists():
        return tool_counts

    try:
        for session_file in logs_dir.glob('session_*.json'):
            with open(session_file, 'r') as f:
                session = json.load(f)
                for tool_call in session.get('tool_calls', []):
                    tool_name = tool_call.get('tool', 'unknown')
                    tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
    except:
        pass

    return tool_counts


def monitor_experiment(project_dir: Path, refresh_seconds: int = 2, mode: str = 'full'):
    """Monitor an experiment directory and display updates.

    Args:
        project_dir: Path to the experiment directory
        refresh_seconds: How often to refresh the display
        mode: Display mode - 'full', 'decisions', 'live', or 'compact'
    """

    print(f"Monitoring: {project_dir}")
    print(f"Mode: {mode}")
    print(f"Refresh: every {refresh_seconds} seconds")
    print("Press Ctrl+C to stop\n")
    time.sleep(2)

    while True:
        try:
            clear_screen()

            print("=" * 80)
            print(f"  EXPERIMENT MONITOR - {project_dir.name}")
            print(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}  |  Mode: {mode}")
            print("=" * 80)
            print()

            # Check if directory exists
            if not project_dir.exists():
                print("Waiting for experiment to start...")
                print(f"   Directory does not exist yet: {project_dir}")
                time.sleep(refresh_seconds)
                continue

            # DECISIONS MODE - Focus on agent decisions
            if mode == 'decisions':
                print(colorize("AGENT DECISIONS", 'bold'))
                print("-" * 80)
                show_decisions(project_dir, num_lines=50)
                print()

            # LIVE MODE - Focus on live activity log
            elif mode == 'live':
                print(colorize("LIVE ACTIVITY LOG", 'bold'))
                print("-" * 80)
                show_live_log(project_dir, num_lines=40)
                print()

            # FULL or COMPACT MODE - Show everything
            else:
                # Session statistics
                stats = get_session_stats(project_dir)
                if stats['total_sessions'] > 0:
                    print(colorize("SESSION STATISTICS", 'bold'))
                    print("-" * 80)
                    print(f"  Total sessions: {stats['total_sessions']}")
                    for stype, count in stats['by_type'].items():
                        print(f"    {stype}: {count}")
                    if stats['last_session']:
                        last = stats['last_session']
                        print(f"  Last: {last.get('session_type')} - {last.get('status')}")
                        print(f"         Tool calls: {last.get('tool_calls_count', 0)}, "
                              f"Decisions: {last.get('decisions_count', 0)}")
                    print()

                # Tool usage statistics
                tool_stats = show_tool_stats(project_dir)
                if tool_stats:
                    print(colorize("TOOL USAGE", 'bold'))
                    print("-" * 80)
                    for tool, count in sorted(tool_stats.items(), key=lambda x: -x[1])[:8]:
                        bar = '#' * min(count, 30)
                        print(f"  {tool:15} {bar} ({count})")
                    print()

                # Files to monitor (compact view in full mode)
                if mode == 'compact':
                    files = {
                        'requirement_cards.json': 'Cards',
                        'feature_list.json': 'Tests',
                        'review_notes.txt': 'Review',
                    }
                else:
                    files = {
                        'phase_constraint.txt': 'Phase Constraint',
                        'requirement_cards.json': 'Requirement Cards',
                        'feature_list.json': 'Feature Tests',
                        'review_notes.txt': 'Review Report',
                    }

                print(colorize("FILES", 'bold'))
                print("-" * 80)
                for filename, label in files.items():
                    filepath = project_dir / filename
                    if filepath.exists():
                        info = get_file_info(filepath)
                        print(f"  {label:20} {colorize('OK', 'green')} {info}")
                    else:
                        print(f"  {label:20} {colorize('pending', 'yellow')}")
                print()

                # Show requirement cards count
                req_cards_file = project_dir / 'requirement_cards.json'
                if req_cards_file.exists():
                    count = count_json_items(req_cards_file)
                    print(colorize(f"REQUIREMENT CARDS: {count}", 'bold'))
                    print("-" * 80)
                    try:
                        with open(req_cards_file, 'r') as f:
                            cards = json.load(f)
                            for card in cards[:3]:  # Show first 3
                                print(f"  {card.get('id', '?')}: {card.get('title', 'No title')}")
                            if len(cards) > 3:
                                print(f"  ... and {len(cards) - 3} more")
                    except:
                        pass
                    print()

                # Show feature list count
                features_file = project_dir / 'feature_list.json'
                if features_file.exists():
                    try:
                        with open(features_file, 'r') as f:
                            data = json.load(f)
                            tests = data if isinstance(data, list) else data.get('tests', [])
                            passing = sum(1 for t in tests if t.get('passes', False))
                            total = len(tests)
                            pct = 100 * passing // total if total > 0 else 0

                            # Color-coded percentage
                            if pct >= 80:
                                pct_str = colorize(f"{pct}%", 'green')
                            elif pct >= 50:
                                pct_str = colorize(f"{pct}%", 'yellow')
                            else:
                                pct_str = colorize(f"{pct}%", 'red')

                            print(colorize(f"FEATURE TESTS: {passing}/{total} ({pct_str})", 'bold'))
                            print("-" * 80)

                            # Show first few tests
                            for test in tests[:5]:
                                status = colorize("PASS", 'green') if test.get('passes', False) else colorize("TODO", 'yellow')
                                print(f"  [{status}] {test.get('id', '?')}: {test.get('title', 'No title')[:50]}")
                            if len(tests) > 5:
                                print(f"  ... and {len(tests) - 5} more")
                    except Exception as e:
                        print(f"  (Error: {e})")
                    print()

                # Show recent decisions (compact view)
                logs_dir = project_dir / 'logs'
                if logs_dir.exists():
                    print(colorize("RECENT DECISIONS", 'bold'))
                    print("-" * 80)
                    show_decisions(project_dir, num_lines=8)
                    print()

                    print(colorize("LIVE LOG (last 10 lines)", 'bold'))
                    print("-" * 80)
                    show_live_log(project_dir, num_lines=10)
                    print()

            print("=" * 80)
            print(f"Modes: --mode full|decisions|live|compact")
            print(f"Refreshing in {refresh_seconds}s... (Ctrl+C to stop)")

            time.sleep(refresh_seconds)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(refresh_seconds)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor an experiment run in real-time with logging",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python monitor.py generations/mvp-01
  python monitor.py generations/mvp-01 --mode decisions   # Focus on decisions
  python monitor.py generations/mvp-01 --mode live        # Focus on live log
  python monitor.py generations/mvp-01 --mode compact     # Compact overview
  python monitor.py generations/mvp-01 --refresh 5        # Slower refresh

Modes:
  full      - Show everything: sessions, tools, files, tests, decisions, live log
  decisions - Focus on agent decisions and reasoning
  live      - Focus on real-time activity log with all tool calls
  compact   - Minimal overview of key metrics
        """
    )

    parser.add_argument(
        'project_dir',
        type=Path,
        nargs='?',
        default=Path('generations/mvp-01'),
        help='Project directory to monitor (default: generations/mvp-01)'
    )

    parser.add_argument(
        '--refresh',
        type=int,
        default=2,
        help='Refresh interval in seconds (default: 2)'
    )

    parser.add_argument(
        '--mode',
        type=str,
        default='full',
        choices=['full', 'decisions', 'live', 'compact'],
        help='Display mode (default: full)'
    )

    args = parser.parse_args()

    try:
        monitor_experiment(args.project_dir, args.refresh, args.mode)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")
        sys.exit(0)


if __name__ == '__main__':
    main()
