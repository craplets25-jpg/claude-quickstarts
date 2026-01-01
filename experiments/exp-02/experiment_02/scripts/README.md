# Scripts

Utility scripts for running and monitoring experiments.

---

## autonomous_agent_demo.py

**Purpose**: Main experiment runner for the 3-agent pipeline

**Usage**:
```bash
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-01_my-run \
  --max-iterations 20 \
  --model claude-sonnet-4-5
```

**Arguments**:
- `--project-dir`: Where to create the experiment run (required)
- `--max-iterations`: Maximum number of sessions (default: unlimited)
- `--model`: Claude model to use (default: claude-sonnet-4-5)

**What it does**:
1. Creates project directory
2. Copies phase_constraint.txt and EXP_02_MANIFESTO.md
3. Initializes logging system
4. Runs 3-agent pipeline:
   - Session 1: SPEC LIBRARIAN (derives requirements from docs)
   - Session 2: SPEC REVIEWER (filters tech-specific details)
   - Sessions 3+: CODING AGENT (implements tests incrementally)

**Example runs**:
```bash
# Full MVP run (20 iterations, ~5-6 hours)
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-01_mvp-full \
  --max-iterations 20

# Quick verification (2 iterations, ~10 minutes)
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-01_quick-test \
  --max-iterations 2

# Unlimited (runs until all tests pass)
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-01_complete-run
```

**Stopping criteria**:
- Max iterations reached (if specified)
- All tests passing
- User interrupts (Ctrl+C)

---

## monitor.py

**Purpose**: Real-time monitoring dashboard for experiment runs

**Usage**:
```bash
python scripts/monitor.py runs/2026-01-01_my-run [options]
```

**Display Modes**:
```bash
# Full dashboard (default)
python scripts/monitor.py runs/2026-01-01_mvp-full

# Focus on agent decisions
python scripts/monitor.py runs/2026-01-01_mvp-full --mode decisions

# Watch live activity log
python scripts/monitor.py runs/2026-01-01_mvp-full --mode live

# Compact overview
python scripts/monitor.py runs/2026-01-01_mvp-full --mode compact
```

**Options**:
- `--mode`: Display mode (full|decisions|live|compact)
- `--refresh`: Refresh interval in seconds (default: 2)

**What it shows**:

**Full Mode**:
- Session statistics (total sessions, by type)
- Tool usage histogram
- File status
- Requirement cards count
- Feature tests progress (X/Y passing, percentage)
- Recent decisions (last 8)
- Live log (last 10 lines)

**Decisions Mode**:
- Agent decisions with reasoning (last 50)
- Phase transitions
- Option selections

**Live Mode**:
- Real-time activity log (last 40 lines)
- Color-coded by severity (ERROR, DECISION, TOOL, etc.)

**Compact Mode**:
- Minimal overview of key metrics
- Faster refresh for quick checks

**Keyboard shortcuts**:
- `Ctrl+C`: Stop monitoring

---

## split_large_docs.py

**Purpose**: Split large markdown documentation files into logical sections

**Problem**: Large files (like DeepWiki at 188KB/51,000 tokens) exceed Claude's 25,000 token read limit, forcing agents to use inefficient Grep/offset reads.

**Solution**: Automatically split documents by header structure into manageable sections.

**Usage**:
```bash
# Split by H2 headers (##) - default
python scripts/split_large_docs.py ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md

# Split by H3 headers (###) for even smaller sections
python scripts/split_large_docs.py ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md --level 3

# Custom output directory
python scripts/split_large_docs.py input.md --output-dir my-split-docs/
```

**Arguments**:
- `input_file`: Markdown file to split (required)
- `--level`: Header level to split on (2, 3, or 4, default: 2)
- `--output-dir`: Output directory (default: `<filename>-sections/`)

**What it does**:
1. Parses markdown file and identifies all headers
2. Splits on specified header level (H2, H3, or H4)
3. Creates separate file for each section
4. Preserves metadata (source file, line numbers)
5. Generates INDEX.md with section summaries
6. Estimates token count per section

**Example output**:
```
debater-early-access-program-sdk-Deepwiki-sections/
├── INDEX.md                                    # Section index with previews
├── 001_purpose-and-scope.md                   # ~173 tokens
├── 002_overall-sdk-architecture.md            # ~760 tokens
├── 055_architecture-overview.md               # ~596 tokens (with diagrams!)
└── ... (105 sections total)
```

**Benefits**:
- ✅ Agents can read entire sections without token limits
- ✅ Logical organization by topic
- ✅ Preserves source file line numbers for traceability
- ✅ INDEX.md provides overview of all sections
- ✅ Each section includes metadata comments
- ✅ Mermaid diagrams preserved in correct sections

**Real results from DeepWiki split**:
- **Original**: 188KB, ~51,000 tokens (exceeded limit)
- **After split**: 105 sections, avg ~443 tokens each
- **Largest section**: ~1,261 tokens (well within limit)
- **Sections with Evidence Detection diagrams**: #55 (Architecture Overview)

**When to use**:
- Before starting new experiment with large documentation
- When agents struggle with "file too large" errors
- When you want agents to find information faster
- When documentation has clear hierarchical structure

**Example workflow**:
```bash
# 1. Split the large doc
python scripts/split_large_docs.py ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md

# 2. Update prompts to reference the sections directory
# Instead of: "Read debater-early-access-program-sdk-Deepwiki.md"
# Use: "Read files in debater-early-access-program-sdk-Deepwiki-sections/"

# 3. Agent can now efficiently:
#    - Read INDEX.md to find relevant sections
#    - Read specific sections without token limits
#    - Find diagrams and code examples quickly
```

---

## Quick Reference

### Starting a new experiment:
```bash
# From exp-02/experiment_02/ directory
python scripts/autonomous_agent_demo.py \
  --project-dir runs/$(date +%Y-%m-%d)_my-experiment \
  --max-iterations 10
```

### Monitoring in separate terminal:
```bash
# Terminal 1: Run experiment
python scripts/autonomous_agent_demo.py --project-dir runs/2026-01-01_mvp-full --max-iterations 20

# Terminal 2: Monitor
python scripts/monitor.py runs/2026-01-01_mvp-full

# Terminal 3: Watch decisions
tail -f runs/2026-01-01_mvp-full/logs/decisions.md

# Terminal 4: Watch live log
tail -f runs/2026-01-01_mvp-full/logs/live.log
```

### Finding latest run:
```bash
# List all runs chronologically
ls -lt runs/

# Get path of latest run
LATEST=$(ls -t runs/ | head -1)
echo "runs/$LATEST"

# Monitor latest run
python scripts/monitor.py runs/$LATEST
```

---

## Log Files Created

Every run creates a `logs/` directory with:

**decisions.md**
- Human-readable markdown
- Agent decisions with reasoning
- Phase transitions

**live.log**
- Real-time activity log
- Tool calls with status
- Timestamps in HH:MM:SS format

**experiment_log.jsonl**
- JSON Lines format
- One line per session
- Session summaries with metrics

**session_<TYPE>_<NUM>_<TIMESTAMP>.json**
- Detailed session logs
- All tool calls with inputs/outputs
- All decisions with reasoning
- Artifacts created/modified

---

## Tips

**Long runs**:
- Use `nohup` or `screen` to keep running if SSH disconnects
- Monitor with `--mode compact` for less CPU usage
- Check logs directory size periodically

**Debugging**:
- Use `--mode live` to see real-time tool calls
- Check `session_*.json` for detailed interaction logs
- Read `decisions.md` to understand agent reasoning

**Performance**:
- Monitor refreshes every 2 seconds by default
- Increase `--refresh 5` if system is slow
- Live log can grow large on long runs
