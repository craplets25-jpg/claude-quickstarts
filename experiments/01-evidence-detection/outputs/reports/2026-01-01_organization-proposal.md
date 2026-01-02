# Organization Proposal for Experiment 02

**Created**: 2026-01-01
**Purpose**: Establish consistent naming and folder structure

---

## Current Problems

1. **Inconsistent naming**: `test-run-03` vs `test-fix-verify` vs `mvp-01`
2. **No dates in filenames**: Can't tell when reports were created
3. **Scattered reports**: Analysis docs in root, some in runs folder
4. **No auto-sorting**: Files don't sort chronologically
5. **Mixed purposes**: Verification runs mixed with actual test runs

---

## Proposed Structure

```
experiments/exp-02/experiment_02/
│
├── prompts/                          # Agent prompts (unchanged)
│   ├── coding_prompt.md
│   ├── spec_librarian_prompt.md
│   └── spec_reviewer_prompt.md
│
├── deep-wiki-spec-files/             # Canonical artifacts (unchanged)
│   ├── TOC-debater-early-access-program-sdk-H2-H4.md
│   └── debater-early-access-program-sdk-Deepwiki.md
│
├── runs/                             # ALL experiment runs (NEW)
│   │
│   ├── 2026-01-01_test-run-03/      # Original test
│   │   ├── logs/
│   │   ├── requirement_cards.json
│   │   ├── feature_list.json
│   │   ├── *.py
│   │   └── README.md                # What this run tested
│   │
│   ├── 2026-01-01_verify-prompt-fixes/  # Verification run
│   │   ├── logs/
│   │   ├── requirement_cards.json
│   │   ├── feature_list.json
│   │   └── README.md
│   │
│   └── 2026-01-01_mvp-full/         # Full MVP (upcoming)
│       ├── logs/
│       ├── requirement_cards.json
│       ├── feature_list.json
│       ├── *.py
│       └── README.md
│
├── reports/                          # Analysis & documentation (NEW)
│   │
│   ├── 2026-01-01_code-quality-evaluation.md
│   ├── 2026-01-01_prompt-fixes-applied.md
│   ├── 2026-01-01_verification-report.md
│   ├── 2026-01-01_organization-proposal.md
│   │
│   └── archive/                      # Old/superseded reports
│       └── ...
│
├── docs/                             # Strategy & manifesto (NEW)
│   ├── EXPERIMENT_02_STRATEGY.md
│   ├── EXP_02_MANIFESTO.md
│   └── README.md                     # Overview of experiment
│
├── scripts/                          # Utilities (NEW)
│   ├── monitor.py
│   ├── autonomous_agent_demo.py
│   └── README.md
│
└── [other python files]              # Core code (unchanged)
    ├── agent.py
    ├── client.py
    ├── experiment_logger.py
    ├── progress.py
    ├── prompts.py
    └── security.py
```

---

## Naming Conventions

### Run Directories
**Format**: `YYYY-MM-DD_description-with-dashes`

**Examples**:
- `2026-01-01_test-run-03` (moved from `test-run-03`)
- `2026-01-01_verify-prompt-fixes` (moved from `test-fix-verify`)
- `2026-01-01_mvp-full` (upcoming)
- `2026-01-02_hotfix-validation` (future)

**Rules**:
- Date prefix ensures chronological sorting
- Description uses kebab-case (lowercase with dashes)
- Max 4 words in description
- Each run has a README.md explaining its purpose

### Report Files
**Format**: `YYYY-MM-DD_title-in-kebab-case.md`

**Examples**:
- `2026-01-01_code-quality-evaluation.md`
- `2026-01-01_prompt-fixes-applied.md`
- `2026-01-01_verification-report.md`
- `2026-01-02_mvp-progress-summary.md`

**Rules**:
- Date prefix for sorting
- Descriptive title
- Always markdown format
- Include "Created: YYYY-MM-DD" in header

### Log Files
**Format**: Managed by `experiment_logger.py` (already good)

**Current format**:
- `session_LIB_001_20260101_183135.json`
- `experiment_log.jsonl`
- `decisions.md`
- `live.log`

**Keep as-is** - timestamps already embedded

---

## Migration Plan

### Phase 1: Reorganize Existing Files (Now)

1. Create new directories
2. Move existing runs with date prefixes
3. Move reports to reports/
4. Move strategy docs to docs/
5. Update .gitignore

### Phase 2: Update Scripts (Now)

1. Update default paths in `autonomous_agent_demo.py`
2. Update default paths in `monitor.py`
3. Add helper for creating run directories

### Phase 3: Create Templates (Now)

1. Run README template
2. Report template with metadata
3. Quick-start guide

---

## Run README Template

```markdown
# Run: [Description]

**Date**: YYYY-MM-DD
**Duration**: [Start - End]
**Iterations**: N
**Status**: [Completed / In Progress / Aborted]

## Purpose

[Why this run was created]

## Configuration

- Max iterations: N
- Model: claude-sonnet-4-5
- Prompts version: [git commit or description]

## Results

### Metrics
- Requirement cards: X
- Feature tests: Y
- Tests passing: Z/Y (P%)

### Key Findings
- [Finding 1]
- [Finding 2]

## Files Generated

- requirement_cards.json - [description]
- feature_list.json - [description]
- *.py - [list of code files]
- logs/ - [what's in logs]

## Next Steps

[What should happen after this run]

## Related Reports

- [Link to analysis report]
- [Link to follow-up run]
```

---

## Report Template

```markdown
# [Report Title]

**Created**: YYYY-MM-DD HH:MM
**Author**: [Human / Claude]
**Type**: [Analysis / Verification / Strategy / Evaluation]
**Status**: [Draft / Final / Superseded]

---

## Summary

[2-3 sentence summary]

---

## [Main Content Sections]

...

---

## Related Documents

- **Related Runs**:
  - [Link to run]
- **Supersedes**:
  - [Link to old report, if any]
- **Referenced By**:
  - [Links to reports that reference this]

---

## Changelog

### YYYY-MM-DD
- Initial version

### YYYY-MM-DD
- [Updates made]
```

---

## Implementation Steps

### Step 1: Create Directory Structure

```bash
cd /workspaces/claude-quickstarts/experiments/exp-02/experiment_02

# Create new directories
mkdir -p runs reports docs scripts

# Create archive
mkdir -p reports/archive
```

### Step 2: Move Existing Runs

```bash
# Move test-run-03
mv generations/test-run-03 runs/2026-01-01_test-run-03

# Move test-fix-verify (just completed)
mv generations/test-fix-verify runs/2026-01-01_verify-prompt-fixes

# Keep generations/ for new runs (or delete if empty)
```

### Step 3: Move Reports

```bash
# Move analysis reports
mv CODE_QUALITY_EVALUATION.md reports/2026-01-01_code-quality-evaluation.md
mv PROMPT_FIXES_APPLIED.md reports/2026-01-01_prompt-fixes-applied.md
mv VERIFICATION_REPORT.md reports/2026-01-01_verification-report.md
mv TEST_VERIFICATION_TRACKING.md reports/2026-01-01_test-verification-tracking.md
mv ORGANIZATION_PROPOSAL.md reports/2026-01-01_organization-proposal.md
```

### Step 4: Move Strategy Docs

```bash
# Move strategy/manifesto
mv EXPERIMENT_02_STRATEGY.md docs/EXPERIMENT_02_STRATEGY.md
mv EXP_02_MANIFESTO.md docs/EXP_02_MANIFESTO.md
```

### Step 5: Move Scripts

```bash
# Move utilities
mv monitor.py scripts/monitor.py
mv autonomous_agent_demo.py scripts/autonomous_agent_demo.py
```

### Step 6: Create READMEs

Create README.md in each run directory explaining its purpose.

### Step 7: Update .gitignore

```bash
# Add to .gitignore
echo "runs/*/logs/*.log" >> .gitignore
echo "runs/*/__pycache__/" >> .gitignore
echo "reports/archive/" >> .gitignore
```

---

## Benefits

### Auto-Sorting
```bash
$ ls -l runs/
2026-01-01_test-run-03/
2026-01-01_verify-prompt-fixes/
2026-01-01_mvp-full/
2026-01-02_hotfix/
```
Chronological order automatically!

### Clarity
- Clear separation: runs vs reports vs docs vs scripts
- Each run has context (README)
- Reports have metadata (date, status, type)

### Discoverability
- New team member: read docs/README.md
- Find latest run: `ls -t runs/ | head -1`
- Find verification reports: `ls reports/*verification*`

### Maintenance
- Archive old reports easily
- Compare runs by date
- Track evolution over time

---

## After Migration

### Quick Reference Commands

```bash
# View all runs chronologically
ls -lt runs/

# View latest run
ls -t runs/ | head -1

# View all reports
ls -lt reports/

# View latest report
ls -t reports/*.md | head -1

# Monitor latest run
RUN=$(ls -t runs/ | head -1)
python scripts/monitor.py runs/$RUN

# Create new run directory with README
DATE=$(date +%Y-%m-%d)
mkdir -p runs/${DATE}_my-new-run
cat > runs/${DATE}_my-new-run/README.md << 'EOF'
# Run: My New Run
**Date**: $(date +%Y-%m-%d)
...
EOF
```

---

## Rollback Plan

If migration causes issues:

```bash
# Restore original structure
mv runs/2026-01-01_test-run-03 generations/test-run-03
mv runs/2026-01-01_verify-prompt-fixes generations/test-fix-verify
mv reports/*.md .
mv docs/*.md .
mv scripts/*.py .
```

All changes are just file moves - no data loss.

---

## Questions for User

1. ✅ Approve this structure?
2. ✅ Any additional directories needed?
3. ✅ Naming convention acceptable?
4. ✅ Should we keep `generations/` or delete it?
5. ✅ Any files I missed in the migration plan?

---

## Next Steps After Approval

1. Execute migration commands
2. Update script paths
3. Create READMEs for existing runs
4. Create docs/README.md with overview
5. Test that monitor.py and autonomous_agent_demo.py still work
6. Commit the reorganization
7. Run full MVP test with new structure
