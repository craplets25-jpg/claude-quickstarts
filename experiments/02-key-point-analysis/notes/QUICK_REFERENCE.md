# Quick Reference - Experiment Infrastructure

**Last Updated**: 2026-01-01

---

## 📋 Pre-Flight Checklist

Before running ANY experiment:

```bash
# 1. Check feature parity
python scripts/check_feature_parity.py

# 2. Validate configuration  
python scripts/validate_experiment.py

# 3. Verify symlinks exist
ls -la deep-wiki-spec-files reference-files

# 4. Test git initialization
python -c "from agent import _initialize_git_repo; from pathlib import Path; _initialize_git_repo(Path('runs/test')); print('✓ Git works')"
```

---

## 🚀 Starting New Experiment

```bash
# Automated (RECOMMENDED)
python scripts/setup_new_experiment.py \
  --source exp-03 \
  --target exp-04 \
  --capability "Claim Detection" \
  --num 4

# Manual
cd experiments/exp-04/experiment_04
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-01_my-run \
  --max-iterations 20 \
  --model sonnet
```

---

## 🔍 Monitoring Active Experiment

```bash
# Check live log
tail -f runs/YYYY-MM-DD_name/logs/live.log

# Check agent thoughts
tail -f runs/YYYY-MM-DD_name/logs/agent-thoughts.log

# Check progress
python -c "from progress import count_passing_tests; p,t = count_passing_tests('runs/YYYY-MM-DD_name'); print(f'{p}/{t} tests passing')"

# Check git commits
cd runs/YYYY-MM-DD_name && git log --oneline -10
```

---

## 📁 Directory Structure Quick Guide

```
experiment_03/
├── docs/                  ← Methodology, requirements, rationale
├── prompts/               ← Agent behavior definitions
├── reports/               ← Timestamped findings (YYYY-MM-DD_*.md)
├── runs/                  ← Experiment runs (YYYY-MM-DD_*)
│   └── YYYY-MM-DD_name/
│       └── .git/          ← Each run has isolated git!
├── scripts/               ← Automation and utilities
│   ├── autonomous_agent_demo.py       ← Main runner
│   ├── check_feature_parity.py        ← Feature validation
│   ├── setup_new_experiment.py        ← Experiment duplication
│   ├── validate_experiment.py         ← Configuration check
│   └── split_large_docs.py            ← Document processing
├── agent.py               ← Core agent loop + git initialization
├── experiment_logger.py   ← Multi-level logging
└── [other core files]     ← client.py, progress.py, security.py, etc.
```

---

## 🐛 Troubleshooting

### "Run doesn't have .git directory"

```bash
# Check if git initialization is working
python scripts/check_feature_parity.py

# Expected: ✅ agent.py initializes git repositories
```

### "Agent can't find files"

```bash
# Check symlinks
ls -la deep-wiki-spec-files  # Should be symlink
ls -la reference-files        # Should be symlink

# Check paths in prompts
grep -r "../../../" prompts/  # Should find canonical artifacts
```

### "Tests not being marked complete"

```bash
# Check feature_list.json
cat runs/YYYY-MM-DD_name/feature_list.json | grep "passes"

# Check coding prompt has update instruction
grep -A 10 "Update ALL Passing Tests" prompts/coding_prompt.md
```

---

## 📊 Key Concepts

### Git Isolation

Each run has its own `.git/` repository:

```bash
runs/2026-01-01_run-1/.git/  ← Independent repo
runs/2026-01-01_run-2/.git/  ← Independent repo
```

**Benefits**:
- Isolated version history
- Agent commits incrementally
- Easy cleanup (delete run = delete history)
- No contamination between experiments

### Date-Prefixed Naming

All runs and reports use `YYYY-MM-DD_` prefix:

```bash
runs/2026-01-01_key-point-analysis/    ← Automatic chronological order
reports/2026-01-01_git-fix.md          ← Easy to find by date
```

### 3-Agent Pipeline

1. **SPEC LIBRARIAN** - Derives requirements from docs
2. **SPEC REVIEWER** - Filters tech-specific details
3. **CODING AGENT** - Implements behavior-only requirements

---

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| `docs/README.md` | Quick overview |
| `docs/CRITICAL_REQUIREMENTS.md` | Non-negotiable infrastructure |
| `docs/DIRECTORY_STRUCTURE_RATIONALE.md` | Design philosophy (300+ lines) |
| `docs/QUICK_REFERENCE.md` | This file |
| `FEATURE_COMPARISON.md` | autonomous-coding vs experiment_03 |
| `scripts/README.md` | Script documentation |
| `reports/2026-01-01_git-isolation-fix.md` | Git isolation bug fix record |

---

## 🔧 Common Commands

```bash
# Create new experiment from template
python scripts/setup_new_experiment.py \
  --source exp-03 --target exp-04 \
  --capability "Claim Detection" --num 4

# Validate experiment before running
python scripts/validate_experiment.py

# Check feature parity with baseline
python scripts/check_feature_parity.py

# Run experiment
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-01_test \
  --max-iterations 20 \
  --model sonnet

# Monitor experiment
tail -f runs/2026-01-01_test/logs/live.log

# Check progress
cd runs/2026-01-01_test
git log --oneline
python -m pytest -v
```

---

## ⚠️ Common Mistakes

1. **Forgetting to validate** before running
   - Always run `check_feature_parity.py` and `validate_experiment.py`

2. **Not using date prefixes** for runs
   - Always use `YYYY-MM-DD_` format for runs and reports

3. **Manual experiment copying** instead of using `setup_new_experiment.py`
   - Manual copying misses critical features (like we did with git!)

4. **Assuming parity** without checking
   - Use `check_feature_parity.py` to verify all features present

5. **Ignoring validation errors**
   - Fix errors before running - they indicate real problems

---

## 🎯 Quick Wins

1. **Use automated setup**:
   ```bash
   python scripts/setup_new_experiment.py --source exp-03 --target exp-04 --capability "Claim Detection" --num 4
   ```

2. **Always validate**:
   ```bash
   python scripts/check_feature_parity.py && python scripts/validate_experiment.py
   ```

3. **Monitor in real-time**:
   ```bash
   tail -f runs/YYYY-MM-DD_name/logs/agent-thoughts.log
   ```

4. **Check git commits**:
   ```bash
   cd runs/YYYY-MM-DD_name && git log --oneline --graph
   ```

---

**For detailed information, see**:
- `docs/DIRECTORY_STRUCTURE_RATIONALE.md` - Complete design philosophy
- `docs/CRITICAL_REQUIREMENTS.md` - Must-have infrastructure
- `FEATURE_COMPARISON.md` - Feature parity analysis
- `scripts/README.md` - Script usage guide

---

**Questions?** Check the comprehensive documentation in `docs/` folder.
