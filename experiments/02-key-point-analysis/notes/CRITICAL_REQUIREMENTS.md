# Critical Infrastructure Requirements

This document lists **non-negotiable** infrastructure requirements that MUST be present in every experiment. Missing any of these will cause experiments to fail or lose critical capabilities.

---

## ✅ Requirement 1: Isolated Git Repository Per Run

**Status**: ✅ IMPLEMENTED (as of 2026-01-01)

### Why Critical

Each experiment run MUST have its own isolated git repository. This is a fundamental architectural requirement because:

1. **Agent Progress Tracking**: Agents commit incrementally after implementing each test
2. **Version History**: Each run has independent version history
3. **Rollback Capability**: Easy to rollback if something breaks
4. **Clean Separation**: No contamination between different experiment runs
5. **Easy Cleanup**: Can delete entire run directory without affecting others

### How It's Implemented

**In `agent.py` (lines 183-258)**:
```python
def _initialize_git_repo(project_dir: Path) -> None:
    """Initialize a git repository in the project directory."""
    git_dir = project_dir / ".git"

    if git_dir.exists():
        return

    subprocess.run(["git", "init"], cwd=project_dir, check=True)
    (project_dir / ".gitignore").write_text(gitignore_content)
```

Called automatically when creating project directory (line 216):
```python
# Create project directory
project_dir.mkdir(parents=True, exist_ok=True)

# Initialize git repository for this run (isolated from parent repo)
_initialize_git_repo(project_dir)
```

**In `prompts/coding_prompt.md` (Step 6b)**:
- Agents are instructed to commit after each test
- Example commit messages provided
- Git commands: `git status`, `git add`, `git commit`, `git log`

### Verification

Run feature parity check:
```bash
python scripts/check_feature_parity.py
```

Should show:
```
✓ agent.py initializes git repositories
✓ Prompts instruct agents to use git
✓ Runs have isolated .git directories
```

### What Went Wrong

**Original Issue** (2026-01-01):
- Experiment 02/03 were copied from `autonomous-coding/`
- Git initialization code was NOT copied
- Runs committed to parent repo (`/workspaces/claude-quickstarts/.git`)
- No isolation between runs
- Lost autonomous-coding's git-per-run capability

**Impact**:
- ❌ All runs shared same git history
- ❌ Couldn't independently version runs
- ❌ Harder to track what changed in each run
- ❌ Couldn't delete run without losing commits

### How to Prevent

1. **Always run** `python scripts/check_feature_parity.py` after creating new experiment
2. **Verify** new runs have `.git/` directory: `ls -la runs/YYYY-MM-DD_run-name/.git`
3. **Test** git works in run: `cd runs/test && git status`
4. **Never skip** feature parity checks when copying experiments

---

## ✅ Requirement 2: Comprehensive Logging

**Status**: ✅ IMPLEMENTED

### Why Critical

Experiments must log all agent interactions for post-hoc analysis and debugging.

### Implementation

- `experiment_logger.py`: Multi-level logging system
- `logs/live.log`: Real-time tool calls
- `logs/agent-thoughts.log`: Narrative reasoning
- `logs/session_*.json`: Complete structured logs

### Verification

Check after running experiment:
```bash
ls -la runs/YYYY-MM-DD_name/logs/
# Should show: live.log, agent-thoughts.log, session_*.json
```

---

## ✅ Requirement 3: Progress Tracking

**Status**: ✅ IMPLEMENTED

### Why Critical

Agents must track which tests pass to avoid duplicate work.

### Implementation

- `progress.py`: Count passing tests
- `feature_list.json`: Source of truth for test status
- `claude-progress.txt`: Human-readable progress notes

### Verification

```bash
python -c "from progress import count_passing_tests; print(count_passing_tests('runs/test'))"
```

---

## ✅ Requirement 4: Security Sandbox

**Status**: ✅ IMPLEMENTED

### Why Critical

Agents run arbitrary code and must be restricted to allowed commands.

### Implementation

- `security.py`: Command allowlist and filesystem restrictions
- `.claude_settings.json`: Per-run security configuration
- Sandbox mode enabled by default

### Verification

Check security settings created:
```bash
cat runs/YYYY-MM-DD_name/.claude_settings.json
```

---

## 🔧 Requirement 5: Path Resolution

**Status**: ✅ IMPLEMENTED

### Why Critical

Agents must find canonical artifacts (DeepWiki, examples) using correct relative paths.

### Implementation

- Symlinks to shared resources: `deep-wiki-spec-files/`, `reference-files/`
- Prompts use `../../../` to reach from `experiment_XX/runs/NAME/` to `exp-XX/`
- Path handling in `autonomous_agent_demo.py`

### Verification

```bash
ls -la deep-wiki-spec-files  # Should be symlink
ls -la reference-files        # Should be symlink
```

---

## 📋 Pre-Flight Checklist

Before running ANY experiment, verify:

- [ ] `python scripts/check_feature_parity.py` passes
- [ ] `python scripts/validate_experiment.py` passes
- [ ] Symlinks exist: `deep-wiki-spec-files/`, `reference-files/`
- [ ] Prompts reference correct paths (`../../../...`)
- [ ] Test run creates `.git/`: `ls runs/test/.git`
- [ ] Git commands work in run: `cd runs/test && git status`

---

## 🚨 Emergency Recovery

If you discover a critical feature is missing:

1. **STOP all running experiments immediately**
2. **Run** `python scripts/check_feature_parity.py` to identify issues
3. **Compare** with `autonomous-coding/` baseline
4. **Fix** the missing feature in experiment infrastructure
5. **Verify** with validation scripts
6. **Document** what was missing and how it was fixed
7. **Update** this document with new requirement

---

## 🔍 How We Caught This Bug

1. User noticed: "that is strange because when i go into the background task shown in the terminal i see nothing happening"
2. Investigation: Checked if runs have git with `ls -la runs/*/. git`
3. Discovered: No `.git/` directories in experiment runs
4. Compared: autonomous-coding has `generations/legal-workbench-v2/.git/`
5. Root cause: Git initialization never copied from autonomous-coding
6. Fixed: Added `_initialize_git_repo()` function
7. Verified: Created `check_feature_parity.py` script

---

## 📚 Related Documentation

- [Feature Parity Checker](../scripts/check_feature_parity.py)
- [Experiment Validator](../scripts/validate_experiment.py)
- [Setup New Experiment](../scripts/setup_new_experiment.py)
- [Scripts README](../scripts/README.md)

---

**Last Updated**: 2026-01-01
**Maintained By**: Experiment Infrastructure Team
