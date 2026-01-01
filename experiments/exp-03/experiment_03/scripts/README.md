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
  - Simple name: `my-run` → creates in `runs/my-run/`
  - With runs/ prefix: `runs/my-run` → creates in `runs/my-run/`
  - Absolute path: `/full/path/to/run` → uses as-is
- `--max-iterations`: Maximum number of sessions (default: unlimited)
- `--model`: Claude model to use (default: claude-sonnet-4-5)

**What it does**:
1. Creates project directory
2. Copies phase_constraint.txt and EXP_03_MANIFESTO.md
3. Initializes logging system
4. Runs 3-agent pipeline:
   - Session 1: SPEC LIBRARIAN (derives requirements from docs)
   - Session 2: SPEC REVIEWER (filters tech-specific details)
   - Sessions 3+: CODING AGENT (implements tests incrementally)

**Example runs**:
```bash
# Full MVP run (20 iterations)
python scripts/autonomous_agent_demo.py \
  --project-dir 2026-01-01_mvp-full \
  --max-iterations 20

# Quick verification (2 iterations)
python scripts/autonomous_agent_demo.py \
  --project-dir 2026-01-01_quick-test \
  --max-iterations 2

# With runs/ prefix (equivalent to above)
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
  --project-dir $(date +%Y-%m-%d)_my-experiment \
  --max-iterations 10

# Creates: runs/2026-01-01_my-experiment/
```

### Monitoring in separate terminal:
```bash
# Terminal 1: Run experiment
python scripts/autonomous_agent_demo.py --project-dir 2026-01-01_mvp-full --max-iterations 20

# Terminal 2: Monitor
python scripts/monitor.py runs/2026-01-01_mvp-full

# Terminal 3: Watch decisions
tail -f runs/2026-01-01_mvp-full/logs/decisions.md

# Terminal 4: Watch live log
tail -f runs/2026-01-01_mvp-full/logs/live.log

# Terminal 5: Watch agent thoughts (new!)
tail -f runs/2026-01-01_mvp-full/logs/agent-thoughts.log
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

**agent-thoughts.log** (NEW!)
- Agent narrative reasoning
- "Now I'll..." style thoughts
- Timestamped with proper formatting

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

---

## setup_new_experiment.py

**Purpose**: Automated experiment setup to prevent naming bugs

**Problem**: Manually copying experiments and updating file references leads to bugs like the EXP_02_MANIFESTO.md issue where prompts reference files that don't exist.

**Solution**: Automatically copy, update all references, validate file existence.

**Usage**:
```bash
# Create Experiment 04 from Experiment 03
python scripts/setup_new_experiment.py \
  --source exp-03 \
  --target exp-04 \
  --capability "Claim Detection" \
  --num 4

# Create Experiment 05 with custom base directory
python scripts/setup_new_experiment.py \
  --source exp-03 \
  --target exp-05 \
  --capability "Argument Quality" \
  --num 5 \
  --base-dir /custom/path/to/experiments/
```

**Arguments**:
- `--source`: Source experiment directory name (e.g., `exp-03`) (required)
- `--target`: Target experiment directory name (e.g., `exp-04`) (required)
- `--capability`: Name of capability to implement (e.g., "Claim Detection") (required)
- `--num`: Experiment number (e.g., 4) (required)
- `--base-dir`: Base experiments directory (optional, defaults to parent directory)

**What it does**:
1. ✅ Validates source experiment exists
2. ✅ Creates target experiment root directory
3. ✅ Creates symlinks to shared resources (deep-wiki-spec-files, reference-files)
4. ✅ Copies experiment working directory
5. ✅ Cleans up runs/, reports/, generations/ directories
6. ✅ **Updates ALL file references** (EXP_03 → EXP_04, experiment_03 → experiment_04)
7. ✅ Updates phase_constraint.txt with new capability
8. ✅ **Validates all file references** to prevent missing file bugs
9. ✅ Generates setup summary with next steps

**Example output**:
```
=== Setting up exp-04 from exp-03 ===
Capability: Claim Detection
Experiment Number: 4

✓ Creating /workspaces/.../exp-04
✓ Creating symlinks to shared resources...
✓ Copying experiment_03 → experiment_04
✓ Cleaning up runs/, reports/, generations/...
✓ Updating file references...
    Updated: prompts/coding_prompt.md
    Updated: prompts/spec_librarian_prompt.md
    Updated: docs/README.md
✓ Updating phase_constraint.txt for 'Claim Detection'...
✓ Validating file references...
✓ All file references validated successfully

============================================================
✅ Experiment 4 setup complete!
============================================================

Location: /workspaces/.../exp-04/experiment_04
Capability: Claim Detection

Next steps:
  1. cd experiments/exp-04/experiment_04
  2. Review and customize prompts if needed
  3. Run: python scripts/autonomous_agent_demo.py --project-dir runs/YYYY-MM-DD_run-name
```

**Benefits**:
- ✅ No manual find/replace needed
- ✅ Catches missing file references before experiment runs
- ✅ Consistent experiment structure
- ✅ Automatic metadata updates
- ✅ Symlinks shared resources (no duplication)

---

## check_feature_parity.py

**Purpose**: Ensure experiment has all critical features from autonomous-coding baseline

**Problem**: When copying experiments, critical features can be accidentally omitted (like git initialization), causing silent failures.

**Solution**: Compare experiment against `autonomous-coding/` baseline to verify all critical features present.

**Usage**:
```bash
# Check current experiment
python scripts/check_feature_parity.py

# Always run after creating new experiment
python scripts/check_feature_parity.py
```

**What it checks**:
1. ✅ **Git initialization** - Each run has isolated git repo
2. ✅ **Git usage in prompts** - Agents told to use git commands
3. ✅ **Agent commits** - Prompts instruct committing progress
4. ✅ **Project isolation** - Runs have `.git/` directories
5. ✅ **Progress tracking** - progress.py exists and works

**Example output (PASSING)**:
```
=== Checking Feature Parity ===
Baseline: /workspaces/.../autonomous-coding
Experiment: experiment_03

Checking git initialization...
Checking git usage in prompts...
Checking agent commit behavior...
Checking project isolation...
Checking progress tracking...

============================================================
FEATURE PARITY REPORT
============================================================

✓ INFO (7):
  ✓ Baseline has git initialization in prompts
  ✓ Prompts instruct agents to use git
  ✓ agent.py initializes git repositories
  ✓ Both use git commands: git log
  ✓ Coding prompt mentions committing
  ✓ Runs have isolated .git directories
  ✓ Progress tracking present

✅ Feature parity check PASSED
Experiment has all critical features from baseline.

============================================================
```

**Example output (FAILING)**:
```
============================================================
FEATURE PARITY REPORT
============================================================

❌ CRITICAL ERRORS (4):
  ❌ CRITICAL: Experiment prompts don't mention 'git init' - runs won't have isolated git repos
  ❌ CRITICAL: agent.py doesn't initialize git for project directories
  ❌ CRITICAL: Baseline prompts mention git commands ['git log'], but experiment prompts don't
  ❌ CRITICAL: Run directories don't have .git/ - not isolated repositories

❌ Feature parity check FAILED
These missing features could cause experiments to fail.
Fix critical errors before running experiments.
============================================================
```

**When to use**:
- ✅ **After** creating new experiment with `setup_new_experiment.py`
- ✅ **Before** running any experiment for the first time
- ✅ **After** major changes to infrastructure
- ✅ **When** copying experiments manually

**Integration**:
- Automatically run by `setup_new_experiment.py`
- Part of pre-flight checklist

---

## validate_experiment.py

**Purpose**: Validate experiment setup and catch configuration bugs

**Problem**: Missing files (like EXP_02_MANIFESTO.md) or broken symlinks cause experiments to fail mid-run, wasting time and API costs.

**Solution**: Comprehensive validation before running experiments.

**Usage**:
```bash
# Validate current experiment (from experiment_XX directory)
python scripts/validate_experiment.py

# Validate specific experiment
python scripts/validate_experiment.py --experiment-dir /path/to/experiment_03

# Run from scripts/ directory (auto-detects parent)
cd scripts/
python validate_experiment.py  # Validates ../
```

**What it validates**:
1. ✅ **Directory structure** - Required directories exist (prompts/, docs/, scripts/, runs/)
2. ✅ **Required files** - Core files present (agent.py, client.py, .env, requirements.txt)
3. ✅ **Prompt files** - All prompt templates exist
4. ✅ **File references** - All files referenced in prompts actually exist
5. ✅ **Experiment consistency** - Experiment numbers match across files
6. ✅ **Symlinks** - Shared resources symlinked correctly

**Example output**:
```
=== Validating Experiment: experiment_03 ===

Checking directory structure...
Checking required files...
Checking file references in prompts...
Checking experiment number consistency...
Checking symlinks...

============================================================
VALIDATION REPORT
============================================================

✅ All validations passed!

Experiment is properly configured and ready to run.

============================================================
```

**Example with errors**:
```
============================================================
VALIDATION REPORT
============================================================

❌ ERRORS (2):
  Missing required file: prompts/phase_constraint.txt
  prompts/coding_prompt.md: Referenced file missing: EXP_02_MANIFESTO.md
    Expected at: /workspaces/.../experiment_03/EXP_02_MANIFESTO.md

⚠  WARNINGS (1):
  docs/README.md: Found reference to Experiment 02, but directory is experiment_03

❌ Found 2 error(s) that must be fixed.
Please address the errors before running the experiment.

============================================================
```

**When to use**:
- ✅ **Before** every experiment run (catch bugs early)
- ✅ **After** setting up new experiment
- ✅ **After** manually editing prompts or moving files
- ✅ **In CI/CD** to validate experiment configurations

**Integration with setup_new_experiment.py**:
The setup script automatically runs validation and reports any issues, so new experiments are validated before use.

---

## Best Practices

**Setting up new experiments**:
1. Use `setup_new_experiment.py` (not manual copying)
2. Review generated files for experiment-specific customizations
3. Run `validate_experiment.py` to confirm everything is correct
4. Test with a short run (`--max-iterations 2`) before full run

**Avoiding bugs**:
- ✅ Use automated setup script
- ✅ Validate before running
- ✅ Keep symlinks for shared resources (don't copy)
- ✅ Follow date-prefixed naming: `YYYY-MM-DD_description`
- ✅ Clean up old runs periodically

**File organization**:
```
experiments/
├── exp-03/
│   ├── deep-wiki-spec-files/ → ../exp-02/deep-wiki-spec-files/
│   ├── reference-files/ → ../exp-02/reference-files/
│   └── experiment_03/
│       ├── prompts/
│       ├── docs/
│       ├── scripts/
│       ├── runs/
│       │   └── 2026-01-01_key-point-analysis/  ← Date-prefixed!
│       └── reports/
│           └── 2026-01-01_final-report.md      ← Date-prefixed!
└── exp-04/  ← Created by setup_new_experiment.py
    └── ...
```
