# Quick Start Guide - Creating and Running Experiments

## 🆕 Creating a New Experiment (e.g., Experiment 05)

### Prerequisites
- Experiment 04 exists and has all critical features (it's the source of truth)
- You know the capability you want to implement

### Steps

```bash
# 1. Navigate to setup scripts
cd /workspaces/claude-quickstarts/experiments/_shared/infrastructure/scripts

# 2. Run setup script (ALWAYS use exp-04 as source!)
python setup_new_experiment.py \
  --source 04-argument-quality \
  --target 05-your-capability \
  --capability "Your Capability Name" \
  --num 5
```

**The script will:**
- ✅ Validate exp-04 has all critical features (git, skills, prompts)
- ✅ Copy experiment_04 to experiment_05
- ✅ Update all references (EXP_04 → EXP_05)
- ✅ Remove docs/ from agent playground
- ✅ Clean up old runs/
- ✅ Create fresh directory structure
- ✅ Run feature parity check
- ✅ Validate file references
- ❌ FAIL if source is incomplete (tells you to use exp-04)

```bash
# 3. Create knowledge-base documentation
mkdir -p /workspaces/claude-quickstarts/knowledge-base/experiment-05-your-capability/reports

cd /workspaces/claude-quickstarts/knowledge-base/experiment-05-your-capability

# Create your docs
cat > MANIFESTO.md <<'EOF'
# Experiment 05 Manifesto

## Core Principles
- [Your principles here]
EOF

cat > STRATEGY.md <<'EOF'
# Experiment 05 Strategy

## Approach
- [Your strategy here]
EOF

# 4. Navigate to experiment playground
cd /workspaces/claude-quickstarts/experiments/05-your-capability/experiment_05

# 5. (Optional) Customize prompts if needed
# Review: prompts/spec_librarian_prompt.md
# Review: prompts/phase_constraint.txt

# 6. Run the experiment!
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-02_your-run-name \
  --model sonnet \
  --max-iterations 20
```

### What Gets Created

```
experiments/
└── 05-your-capability/
    └── experiment_05/              # Agent playground (CLEAN)
        ├── agent.py                # ✅ Has git init
        ├── prompts/                # ✅ All prompts
        ├── scripts/                # ✅ Runner + validation
        └── runs/                   # Each run = own git repo

knowledge-base/
└── experiment-05-your-capability/  # Documentation
    ├── MANIFESTO.md
    ├── STRATEGY.md
    └── reports/
```

---

## 🔄 Re-running Experiment 04 with Fresh Run

### Clean Run (Recommended)

```bash
cd /workspaces/claude-quickstarts/experiments/04-argument-quality/experiment_04

# Create new run with descriptive name
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-02_argument-quality-v2 \
  --model sonnet \
  --max-iterations 20
```

**This will:**
- ✅ Create `runs/2026-01-02_argument-quality-v2/` directory
- ✅ Initialize isolated git repository inside
- ✅ Run full pipeline: Spec Librarian → Spec Reviewer → Coding
- ✅ Generate fresh requirement_cards.json with rich context
- ✅ Generate fresh feature_list.json with full traceability
- ✅ Agent will commit progress to run's git repo

### Monitoring Progress

```bash
# Terminal 1: Run the experiment
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-02_run \
  --model sonnet \
  --max-iterations 20

# Terminal 2: Monitor logs
tail -f runs/2026-01-02_run/logs/live.log

# Terminal 3: Watch git commits
cd runs/2026-01-02_run
watch -n 5 'git log --oneline -10'
```

### Verification Checklist

After the run completes:

```bash
cd runs/2026-01-02_run

# ✅ Check git was initialized
ls -la .git/
git log --oneline

# ✅ Check outputs
ls -l requirement_cards.json feature_list.json

# ✅ Verify rich context in feature_list.json
python3 << 'EOF'
import json
with open('feature_list.json') as f:
    tests = json.load(f)
    first_test = tests[0]
    print("Test has sources:", "sources" in first_test)
    print("Test has invariants:", "invariants" in first_test)
    print("Test has legacy_notes:", "legacy_notes" in first_test)
EOF

# ✅ Check tests
pytest test_*.py -v

# ✅ Review progress
cat claude-progress.txt
```

---

## 🔧 Troubleshooting

### Issue: "Source experiment missing critical features"

```
❌ CRITICAL: Source agent.py doesn't initialize git repositories
```

**Solution:** You tried to copy from exp-02 or exp-03. Use exp-04 instead:

```bash
python setup_new_experiment.py \
  --source 04-argument-quality \  # ← Use this!
  --target 05-new-exp \
  --capability "New Cap" \
  --num 5
```

### Issue: "Feature parity check failed"

The new experiment is missing features. Usually means:
1. Source was incomplete (use exp-04)
2. Something went wrong during copy

**Solution:**
```bash
# Delete incomplete experiment
rm -rf /workspaces/claude-quickstarts/experiments/05-incomplete

# Start over with exp-04 as source
python setup_new_experiment.py --source 04-argument-quality ...
```

### Issue: No .git/ in run directory

**Check:**
```bash
cd experiments/*/experiment_*/runs/some-run
ls -la .git  # Should exist!
```

**If missing:**
```bash
# Check agent.py has git initialization
cd ../..
grep "_initialize_git_repo" agent.py

# Should see: def _initialize_git_repo(project_dir: Path) -> None:
```

**If not present:** Your experiment wasn't copied from exp-04. Delete and recreate.

### Issue: Agent doesn't use deepwiki-navigator skill

**Check symlink:**
```bash
cd experiments/*/experiment_*/
ls -l custom_skills/deepwiki-navigator

# Should point to: ../../../_shared/skills/deepwiki-navigator
```

**Check prompt mentions it:**
```bash
grep "deepwiki-navigator\|capability_scanner" prompts/spec_librarian_prompt.md
```

### Issue: feature_list.json missing context

This means spec_librarian_prompt.md is outdated. Check it includes:

```markdown
"sources": { ... },
"invariants": [ ... ],
"non_guarantees": [ ... ],
"legacy_notes": [ ... ]
```

If missing, you didn't copy from exp-04. Delete and recreate.

---

## ✅ Pre-Flight Checklist

Before running ANY new experiment:

```bash
cd /workspaces/claude-quickstarts/experiments/XX-capability/experiment_XX

# 1. Validate experiment setup
python scripts/check_feature_parity.py
# Should output: ✅ Feature parity check PASSED

# 2. Check git initialization
grep "_initialize_git_repo" agent.py
# Should find the function

# 3. Check git in prompts
grep "git commit" prompts/coding_prompt.md
# Should find commit instructions

# 4. Check symlinks
ls -l custom_skills/deepwiki-navigator
# Should be a symlink

# 5. Test run with limit
python scripts/autonomous_agent_demo.py \
  --project-dir runs/test-run \
  --max-iterations 2 \
  --model sonnet

# 6. Verify git in test run
ls -la runs/test-run/.git
# Should exist!

# If all pass → Safe to run full experiment
# If any fail → Fix before proceeding
```

---

## 📝 Documentation Best Practices

### During Experiment Setup

1. **Create knowledge-base docs first:**
   ```bash
   mkdir -p knowledge-base/experiment-XX-capability/reports
   ```

2. **Write strategy before running:**
   - Why this capability?
   - What's the approach?
   - What are the expected challenges?

3. **Document as you go:**
   - Add notes to reports/ after each run
   - Capture issues immediately
   - Record learnings while fresh

### After Experiment Completes

1. **Analyze results:**
   ```bash
   cd runs/YYYY-MM-DD_name
   cat claude-progress.txt
   git log --oneline
   grep "PASS\|FAIL" logs/*.log
   ```

2. **Create report:**
   ```bash
   cd knowledge-base/experiment-XX-capability/reports
   cat > YYYY-MM-DD_results.md
   ```

3. **Update knowledge-base/README.md:**
   - Add experiment to index
   - Mark as complete
   - Add key learnings to "Cross-Experiment Learnings"

---

## 📦 Understanding Scaffold vs Git Isolation

**Two levels that work together:**

| Level | What | When | Purpose |
|-------|------|------|---------|
| **Experiment** | `debater_sdk/` scaffold | Setup time | Inherit previous work |
| **Run** | `.git/` repository | Run time | Track agent progress |

**In practice:**
```
exp-05 created from exp-04:
├── debater_sdk/           ← COPIED from exp-04 (cumulative scaffold)
│   └── services/
│       └── argument_quality/  ← Built in exp-04
└── runs/
    └── 2026-01-02_name/
        ├── .git/          ← CREATED at run start (isolated)
        └── debater_sdk/   ← Agent may modify this
            └── services/
                └── evidence/  ← Built during THIS run
```

**The scaffold is your starting point. Git tracks what you build from it.**

For detailed explanation, see: [Scaffold & Git Model](SCAFFOLD_AND_GIT_MODEL.md)

---

## 🎯 Success Criteria

Your experiment is properly set up when:

- ✅ Feature parity check passes
- ✅ Test run creates .git/ directory
- ✅ Agent commits show up in git log
- ✅ feature_list.json has sources, invariants, legacy_notes
- ✅ deepwiki-navigator symlink works
- ✅ No docs/ in agent playground
- ✅ Documentation exists in knowledge-base/

---

## 📞 Quick Commands Reference

```bash
# Create new experiment
cd experiments/_shared/infrastructure/scripts
python setup_new_experiment.py --source 04-argument-quality --target 05-new --capability "New" --num 5

# Run experiment
cd experiments/XX-capability/experiment_XX
python scripts/autonomous_agent_demo.py --project-dir runs/YYYY-MM-DD_name --model sonnet --max-iterations 20

# Validate setup
python scripts/check_feature_parity.py

# Monitor progress
tail -f runs/*/logs/live.log

# Check git commits
cd runs/YYYY-MM-DD_name && git log --oneline

# Run tests
cd runs/YYYY-MM-DD_name && pytest test_*.py -v
```

---

**Last Updated:** 2026-01-02
**Source of Truth:** Experiment 04 - Argument Quality
**Validation:** Always run feature parity check before experiments
