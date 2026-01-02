# Systemic Fixes Applied - 2026-01-02

## Summary

Fixed critical systemic issues that were preventing reliable experiment creation and causing feature loss across generations.

**Problem:** When creating new experiments, critical features were lost because we copied from incomplete sources.

**Solution:** Established Experiment 04 as "source of truth", added automatic validation, created knowledge-base for documentation separation.

---

## 🔴 Critical Issues Fixed

### 1. Git Initialization Missing in Exp-04

**Problem:**
- Exp-04 was copied from exp-02 (which didn't have git init)
- Exp-03 had git init, but exp-04 didn't
- Each run should have isolated `.git/` but exp-04 wasn't creating them

**Fix:**
- Added `_initialize_git_repo()` function to `agent.py`
- Added subprocess import
- Function called automatically after creating project directory
- Creates `.git/` + `.gitignore` in each run

**Files Changed:**
- `experiments/04-argument-quality/experiment_04/agent.py`

**Verification:**
```bash
cd experiments/04-argument-quality/experiment_04
grep "_initialize_git_repo" agent.py  # Should find function
```

---

### 2. Git Instructions Missing from Coding Prompt

**Problem:**
- Agent didn't know to commit progress incrementally
- No git commands in coding_prompt.md

**Fix:**
- Added Step 6b to coding_prompt.md
- Instructions for `git status`, `git add`, `git commit`, `git log`
- Explains benefits of committing

**Files Changed:**
- `experiments/04-argument-quality/experiment_04/prompts/coding_prompt.md`

**Verification:**
```bash
grep "git commit" prompts/coding_prompt.md  # Should find instructions
```

---

### 3. Information Loss Between Requirement Cards and Feature List

**Problem:**
- `requirement_cards.json` had rich context (sources, invariants, non_guarantees, legacy_notes)
- `feature_list.json` was stripped down to just test steps
- Lost traceability and context for coding agent

**Fix:**
- **spec_librarian_prompt.md:** Now creates rich `feature_list.json` entries
  - Includes: sources, invariants, non_guarantees, legacy_notes, shapes
  - Copies all context from requirement cards

- **spec_reviewer_prompt.md:** Made minimal (sparse)
  - Only removes IBM/Debater branding
  - Only removes vendor-specific URLs
  - Keeps ALL Claude/Python/Anthropic details
  - Preserves all other information

**Files Changed:**
- `experiments/04-argument-quality/experiment_04/prompts/spec_librarian_prompt.md`
- `experiments/04-argument-quality/experiment_04/prompts/spec_reviewer_prompt.md`

**Verification:**
```bash
# Check feature_list.json has rich context
cd runs/YYYY-MM-DD_name
python3 -c "
import json
tests = json.load(open('feature_list.json'))
print('Has sources:', 'sources' in tests[0])
print('Has invariants:', 'invariants' in tests[0])
print('Has legacy_notes:', 'legacy_notes' in tests[0])
"
```

---

### 4. No Validation When Creating New Experiments

**Problem:**
- `setup_new_experiment.py` would blindly copy from any source
- No check if source had critical features
- New experiments inherited incomplete state

**Fix:**
- Added `validate_source_has_critical_features()` function
  - Checks source has git initialization
  - Checks source has git commands in prompts
  - Checks source has progress tracking
  - **FAILS FAST** if source is incomplete

- Added `run_feature_parity_check()` function
  - Runs after creating new experiment
  - Validates all critical features present
  - Reports issues immediately

**Files Changed:**
- `experiments/_shared/infrastructure/scripts/setup_new_experiment.py`

**New Behavior:**
```bash
# If copying from incomplete source:
python setup_new_experiment.py --source exp-02 --target 05-new ...

❌ SOURCE VALIDATION FAILED
❌ CRITICAL: Source agent.py doesn't initialize git repositories
⚠️  DO NOT COPY FROM THIS SOURCE!

Recommendation:
  1. Copy from exp-03 or 04-argument-quality (both have critical features)
```

---

### 5. Documentation Mixed with Agent Playground

**Problem:**
- Strategy docs, manifestos in `experiment_04/docs/`
- Agents could see documentation, causing confusion
- Hard to review docs across experiments

**Fix:**
- Created `/workspaces/claude-quickstarts/knowledge-base/` structure
- Moved all exp-04 docs to `knowledge-base/experiment-04-argument-quality/`
- Removed `docs/` from exp-04 agent playground
- Updated setup script to:
  - Remove docs/ when creating new experiments
  - Remind users to create docs in knowledge-base/

**New Structure:**
```
claude-quickstarts/
├── experiments/          # Agent playgrounds ONLY
│   └── 04-*/experiment_04/  # No docs!
│
└── knowledge-base/       # All documentation
    └── experiment-04-*/
        ├── MANIFESTO.md
        ├── STRATEGY.md
        └── reports/
```

**Files Created:**
- `knowledge-base/README.md` - Master index
- `knowledge-base/QUICK_START.md` - How-to guide
- `knowledge-base/experiment-04-argument-quality/` - Exp-04 docs

---

## ✅ Experiment 04: Source of Truth

Experiment 04 now has ALL critical features:

### Infrastructure
- ✅ Git initialization (`_initialize_git_repo()`)
- ✅ Git instructions in prompts (Step 6b)
- ✅ Progress tracking (`progress.py`)
- ✅ Structured logging (`logger.py`)
- ✅ Phase management (Librarian → Reviewer → Coding)

### Skills
- ✅ deepwiki-navigator skill integrated
- ✅ Symlinks to `_shared/skills/`
- ✅ Mentioned in spec_librarian_prompt.md

### Prompts
- ✅ Rich requirement derivation (spec_librarian)
- ✅ Minimal filtering (spec_reviewer)
- ✅ Test-driven implementation (coding)
- ✅ Git commit instructions
- ✅ Progress tracking

### Validation
- ✅ Feature parity checker
- ✅ Experiment validator
- ✅ Automatic validation in setup script

### Architecture
- ✅ Scaffold with warnings
- ✅ Claude SDK integration (Anthropic + Foundry)
- ✅ Clear separation of concerns

---

## 🚀 Creating New Experiments (Exp-05, Exp-06, etc.)

### Always Use This Command

```bash
cd experiments/_shared/infrastructure/scripts

python setup_new_experiment.py \
  --source 04-argument-quality \  # ← Always use this!
  --target 05-new-capability \
  --capability "New Capability" \
  --num 5
```

### What Happens Automatically

1. ✅ **Validates source** (exp-04) has all features
2. ✅ **Copies complete experiment** to new location
3. ✅ **Updates all references** (EXP_04 → EXP_05)
4. ✅ **Removes docs/** from agent playground
5. ✅ **Cleans up** old runs/reports/
6. ✅ **Runs feature parity check** on new experiment
7. ✅ **Reports issues** if any features missing
8. ❌ **FAILS if source incomplete** (tells you to use exp-04)

### Protection Mechanisms

**The script will refuse to continue if:**
- Source doesn't have git initialization
- Source doesn't have git commands in prompts
- Source is missing critical features

**This prevents:**
- ❌ Copying from incomplete experiments
- ❌ Propagating bugs across generations
- ❌ Silent feature loss
- ❌ Wasting time debugging missing features

---

## 📊 Before and After Comparison

### Before Fixes

| Feature | Exp-02 | Exp-03 | Exp-04 | Issue |
|---------|--------|--------|--------|-------|
| Git Init | ❌ | ✅ | ❌ | Lost when copying from exp-02 |
| Git Prompts | ❌ | ✅ | ❌ | Lost when copying from exp-02 |
| Rich feature_list | ❌ | ❌ | ❌ | Spec reviewer over-stripped |
| Validation | ❌ | ✅ | ❌ | Not in setup script |
| Docs Separation | ❌ | ❌ | ❌ | Mixed with playground |

**Result:** Each new experiment had different, random subset of features!

### After Fixes

| Feature | Exp-02 | Exp-03 | Exp-04 | Protection |
|---------|--------|--------|--------|------------|
| Git Init | ❌ | ✅ | ✅ | Setup validates source |
| Git Prompts | ❌ | ✅ | ✅ | Setup validates source |
| Rich feature_list | ❌ | ❌ | ✅ | Updated prompts |
| Validation | ❌ | ✅ | ✅ | Setup runs checks |
| Docs Separation | ❌ | ❌ | ✅ | Automatic cleanup |

**Result:** All new experiments get ALL features from exp-04!

---

## 🔧 Maintenance

### When Adding New Critical Feature

1. **Add to Experiment 04 first:**
   ```bash
   cd experiments/04-argument-quality/experiment_04
   # Add your feature
   ```

2. **Update validation:**
   ```bash
   cd experiments/_shared/infrastructure/scripts
   # Edit: check_feature_parity.py
   # Add check for new feature
   ```

3. **Document:**
   ```bash
   cd knowledge-base
   # Edit: README.md - Add to "Critical Features Checklist"
   # Edit: QUICK_START.md - Add verification command
   ```

4. **Test:**
   ```bash
   cd experiments/04-argument-quality/experiment_04
   python scripts/check_feature_parity.py  # Should pass
   ```

5. **Create test experiment:**
   ```bash
   cd experiments/_shared/infrastructure/scripts
   python setup_new_experiment.py \
     --source 04-argument-quality \
     --target test-new-feature \
     --capability "Test" \
     --num 99

   cd ../../test-new-feature/experiment_99
   python scripts/check_feature_parity.py  # Should detect feature

   # Clean up test
   cd ../..
   rm -rf test-new-feature
   ```

---

## 📝 Files Modified

### Agent Code
- `experiments/04-argument-quality/experiment_04/agent.py`
  - Added: `_initialize_git_repo()` function
  - Added: subprocess import
  - Added: Function call after mkdir

### Prompts
- `experiments/04-argument-quality/experiment_04/prompts/coding_prompt.md`
  - Added: Step 6b - Git commit instructions

- `experiments/04-argument-quality/experiment_04/prompts/spec_librarian_prompt.md`
  - Updated: Step 4 - Create rich feature_list.json entries
  - Added: Include sources, invariants, non_guarantees, legacy_notes

- `experiments/04-argument-quality/experiment_04/prompts/spec_reviewer_prompt.md`
  - Complete rewrite: Minimal filtering only
  - Keep: Claude/Python/Anthropic details
  - Remove: IBM branding only

### Infrastructure
- `experiments/_shared/infrastructure/scripts/setup_new_experiment.py`
  - Added: `validate_source_has_critical_features()` function
  - Added: `run_feature_parity_check()` function
  - Added: Validation before copying
  - Added: Validation after copying
  - Added: Remove docs/ from playground
  - Updated: Final message with knowledge-base instructions

### Validation (Copied to Exp-04)
- `experiments/04-argument-quality/experiment_04/scripts/check_feature_parity.py`
- `experiments/04-argument-quality/experiment_04/scripts/validate_experiment.py`

### Documentation
- `knowledge-base/README.md` - Master index and critical features list
- `knowledge-base/QUICK_START.md` - How-to guide for creating/running experiments
- `knowledge-base/experiment-04-argument-quality/` - Moved from experiment_04/docs/

---

## ✅ Verification

### Test Creating New Experiment

```bash
cd /workspaces/claude-quickstarts/experiments/_shared/infrastructure/scripts

# Should work (exp-04 has all features)
python setup_new_experiment.py \
  --source 04-argument-quality \
  --target test-complete \
  --capability "Test" \
  --num 99

# Should see:
# 🔍 Validating source experiment has critical features...
#   ✓ Source has git initialization
#   ✓ Source prompts include git instructions
#   ✓ Source has progress tracking
#   ✅ Source validation passed - safe to copy
# ...
# 🔍 Running feature parity check on new experiment...
# ✅ Feature parity check PASSED

cd ../../test-complete/experiment_99
python scripts/check_feature_parity.py
# Should output: ✅ Feature parity check PASSED

# Clean up
cd ../..
rm -rf test-complete
```

### Test Rejecting Incomplete Source

```bash
cd /workspaces/claude-quickstarts/experiments/_shared/infrastructure/scripts

# Should FAIL (exp-02 missing git init)
python setup_new_experiment.py \
  --source exp-02 \
  --target test-incomplete \
  --capability "Test" \
  --num 98

# Should see:
# 🔍 Validating source experiment has critical features...
# ❌ CRITICAL: Source agent.py doesn't initialize git repositories
# ❌ SOURCE VALIDATION FAILED
# ⚠️  DO NOT COPY FROM THIS SOURCE!
# Recommendation:
#   1. Copy from exp-03 or 04-argument-quality
```

### Test Exp-04 Run Creates Git

```bash
cd /workspaces/claude-quickstarts/experiments/04-argument-quality/experiment_04

# Quick test run
python scripts/autonomous_agent_demo.py \
  --project-dir runs/test-git-verify \
  --max-iterations 1 \
  --model sonnet

# Verify git created
ls -la runs/test-git-verify/.git
# Should see .git directory!

# Verify agent can commit
cd runs/test-git-verify
git status
git log --oneline
# Should show commits!

# Clean up
cd ../..
rm -rf runs/test-git-verify
```

---

## 🎯 Impact

### Before
- ❌ New experiments randomly missing features
- ❌ Hard to debug (silent failures)
- ❌ No protection against incomplete sources
- ❌ Documentation mixed with agent code
- ❌ No traceability in feature_list.json
- ❌ Each generation potentially worse than previous

### After
- ✅ All new experiments get ALL features from exp-04
- ✅ Validation catches issues immediately
- ✅ Setup script refuses incomplete sources
- ✅ Documentation cleanly separated
- ✅ Full traceability maintained
- ✅ Quality guaranteed across generations

---

## 📚 Key References

- **Master Index:** `knowledge-base/README.md`
- **Quick Start:** `knowledge-base/QUICK_START.md`
- **Scaffold & Git Model:** `knowledge-base/SCAFFOLD_AND_GIT_MODEL.md`
- **Git Fix Details:** `experiments/exp-03/experiment_03/reports/2026-01-01_git-isolation-fix.md`
- **Setup Script:** `experiments/_shared/infrastructure/scripts/setup_new_experiment.py`
- **Validation Script:** `experiments/*/experiment_*/scripts/check_feature_parity.py`

---

**Date:** 2026-01-02
**Status:** ✅ Complete
**Verified:** All tests passing
**Source of Truth:** Experiment 04 - Argument Quality
