# Feature Comparison: autonomous-coding vs experiment_03

**Last Updated**: 2026-01-01

---

## ✅ What We Have (Feature Parity)

| Feature | autonomous-coding | experiment_03 | Status |
|---------|------------------|---------------|---------|
| **Core Agent Loop** | ✅ agent.py | ✅ agent.py | ✅ SAME |
| **Claude SDK Client** | ✅ client.py | ✅ client.py | ✅ SAME |
| **Progress Tracking** | ✅ progress.py | ✅ progress.py | ✅ SAME |
| **Prompt Loading** | ✅ prompts.py | ✅ prompts.py | ✅ SAME |
| **Security Sandbox** | ✅ security.py | ✅ security.py | ✅ SAME |
| **Git Initialization** | ✅ In prompts | ✅ In agent.py | ✅ **IMPROVED** |
| **Isolated Projects** | ✅ generations/ | ✅ runs/ | ✅ RENAMED |
| **Agent Prompts** | ✅ prompts/ | ✅ prompts/ | ✅ **EXPANDED** |
| **Main Runner** | ✅ autonomous_agent_demo.py | ✅ scripts/autonomous_agent_demo.py | ✅ MOVED |
| **Configuration** | ✅ .env, requirements.txt | ✅ .env, requirements.txt | ✅ SAME |
| **Documentation** | ✅ README.md | ✅ README.md + docs/ | ✅ **ENHANCED** |

---

## 🎉 What We Added (New Features)

| Feature | Location | Purpose |
|---------|----------|---------|
| **Experiment Logger** | experiment_logger.py | Multi-level logging (live.log, agent-thoughts.log, session JSON) |
| **Feature Parity Checker** | scripts/check_feature_parity.py | Validate critical features present |
| **Experiment Validator** | scripts/validate_experiment.py | Check configuration before running |
| **Setup Automation** | scripts/setup_new_experiment.py | Automated experiment duplication |
| **Document Splitter** | scripts/split_large_docs.py | Split large docs to avoid token limits |
| **Monitor Script** | scripts/monitor.py | Real-time experiment monitoring |
| **Documentation Folder** | docs/ | Comprehensive research documentation |
| **Reports Folder** | reports/ | Timestamped experiment findings |
| **Critical Requirements** | docs/CRITICAL_REQUIREMENTS.md | Non-negotiable infrastructure list |
| **Structure Rationale** | docs/DIRECTORY_STRUCTURE_RATIONALE.md | Design philosophy documentation |
| **Git Fix Report** | reports/2026-01-01_git-isolation-fix.md | Complete fix documentation |
| **Scripts README** | scripts/README.md | Comprehensive script documentation |

---

## 🔧 What We Changed (Improvements)

### 1. Git Initialization

**Before (autonomous-coding)**:
```markdown
# In prompts/initializer_prompt.md
"Initialize a git repo and make the first commit"
```
- Relied on agent following instructions
- No automatic initialization
- Could be forgotten

**After (experiment_03)**:
```python
# In agent.py
def _initialize_git_repo(project_dir: Path):
    subprocess.run(["git", "init"], cwd=project_dir)
```
- ✅ Automatic initialization
- ✅ Guaranteed to happen
- ✅ Creates .gitignore too

### 2. Logging System

**Before (autonomous-coding)**:
```python
# Basic print statements
print("Tool call:", tool_name)
```
- No structured logging
- Hard to analyze post-hoc
- No machine-readable format

**After (experiment_03)**:
```python
# experiment_logger.py
logger.log_tool_call(tool_name, inputs, status)
logger.log_thought(reasoning)
logger.log_decision(decision, reasoning)
```
- ✅ Multi-level logging
- ✅ Structured JSON output
- ✅ Real-time + historical logs
- ✅ Agent thoughts tracked

### 3. Project Organization

**Before (autonomous-coding)**:
```
autonomous-coding/
├── generations/
│   └── project-name/
```
- No date tracking
- No archive system
- Hard to find when run happened

**After (experiment_03)**:
```
experiment_03/
├── runs/
│   ├── 2026-01-01_key-point-analysis/
│   ├── 2026-01-01_mvp-full/
│   └── archive/
```
- ✅ Date-prefixed
- ✅ Automatic chronological order
- ✅ Archive system
- ✅ Clear naming convention

### 4. Validation Infrastructure

**Before (autonomous-coding)**:
```python
# test_security.py (only security tests)
```
- Only tests security
- No feature validation
- No configuration checks

**After (experiment_03)**:
```python
# Multiple validation layers
check_feature_parity.py      # Critical features
validate_experiment.py        # Configuration
test_security.py              # Security (same)
```
- ✅ Feature parity checking
- ✅ Configuration validation
- ✅ Pre-flight checklists
- ✅ Automated prevention

### 5. Prompt System

**Before (autonomous-coding)**:
```
prompts/
├── app_spec.txt
├── initializer_prompt.md
└── coding_prompt.md
```
- 2 agents (initializer, coder)
- General purpose
- No specialization

**After (experiment_03)**:
```
prompts/
├── spec_librarian_prompt.md   ← NEW: Extract from docs
├── spec_reviewer_prompt.md    ← NEW: Filter legacy details
├── coding_prompt.md           ← Enhanced with git
├── oracle_prompt.md           ← NEW: Future use
└── phase_constraint.txt       ← NEW: Experiment control
```
- ✅ 3-agent pipeline
- ✅ Specialized agents
- ✅ Document-driven approach
- ✅ Phase constraints

---

## 📊 Comparison Summary

### autonomous-coding: Quickstart Design

**Strengths**:
- ✅ Simple, flat structure
- ✅ Easy to understand
- ✅ Quick to get started
- ✅ Minimal dependencies

**Limitations**:
- ❌ No research infrastructure
- ❌ Basic logging
- ❌ Manual validation
- ❌ Limited automation

**Best For**:
- Demos and tutorials
- One-off experiments
- Learning agent patterns
- Public quickstarts

---

### experiment_03: Research Infrastructure

**Strengths**:
- ✅ Comprehensive logging
- ✅ Automated validation
- ✅ Research documentation
- ✅ Experiment tracking
- ✅ Prevention infrastructure

**Limitations**:
- ❌ More complex
- ❌ Steeper learning curve
- ❌ More files to maintain

**Best For**:
- Systematic research
- Long-running experiments
- Team collaboration
- Reproducible science

---

## 🎯 Are We Missing Anything?

### From autonomous-coding

**✅ NO** - We have everything from the original, plus improvements:

| Original Feature | Our Version | Status |
|-----------------|-------------|---------|
| Git per project | ✅ Fixed and automated | ✅ BETTER |
| Agent loop | ✅ Same + enhanced logging | ✅ BETTER |
| Security sandbox | ✅ Same | ✅ SAME |
| Progress tracking | ✅ Same | ✅ SAME |
| Prompt system | ✅ Expanded (3 agents) | ✅ BETTER |

**Nothing is missing. Everything is either:**
1. ✅ **Preserved** (kept the same)
2. ✅ **Enhanced** (improved version)
3. ✅ **Added** (new capabilities)

### Missing from IDEAL State?

Some potential additions (not in either version):

| Feature | Status | Priority |
|---------|--------|----------|
| **Test suite** | ❌ Missing | 🔴 HIGH |
| **CI/CD integration** | ❌ Missing | 🟡 MEDIUM |
| **Performance metrics** | ❌ Missing | 🟡 MEDIUM |
| **Cost tracking** | ❌ Missing | 🟡 MEDIUM |
| **Multi-experiment comparison** | ❌ Missing | 🟢 LOW |

---

## 🚀 Evolution Path

### Phase 1: Quickstart (autonomous-coding)
- Minimal, flat structure
- Focus on "get running"
- Basic functionality

### Phase 2: Research Infrastructure (experiment_03) ← WE ARE HERE
- Organized structure
- Comprehensive logging
- Validation infrastructure
- Research documentation

### Phase 3: Production System (future)
- Test suite
- CI/CD integration
- Performance monitoring
- Cost optimization
- Multi-experiment analysis

---

## 📚 References

- **Original**: `/workspaces/claude-quickstarts/autonomous-coding/`
- **Enhanced**: `/workspaces/claude-quickstarts/experiments/exp-03/experiment_03/`
- **Rationale**: `docs/DIRECTORY_STRUCTURE_RATIONALE.md`
- **Git Fix**: `reports/2026-01-01_git-isolation-fix.md`
- **Critical Requirements**: `docs/CRITICAL_REQUIREMENTS.md`

---

**Conclusion**: We have **100% feature parity** with autonomous-coding PLUS significant improvements for research workflows. Nothing is missing from the original; everything is either preserved or enhanced.
