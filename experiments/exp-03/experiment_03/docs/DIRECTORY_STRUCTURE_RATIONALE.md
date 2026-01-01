# Directory Structure - Design Rationale

**Purpose**: Explain the logic behind each folder/file placement in autonomous coding systems

**Comparison**: `autonomous-coding/` (original) vs `experiment_03/` (our version)

---

## Original Design: autonomous-coding/

### Design Philosophy

The original `autonomous-coding/` was designed as a **minimal, flat structure** for rapid prototyping:

```
autonomous-coding/
├── generations/          ← Output: Where projects are created
├── prompts/              ← Input: Agent instructions
├── agent.py              ← Core: Agent logic
├── autonomous_agent_demo.py  ← Entry: Main runner
├── client.py             ← Interface: Claude SDK wrapper
├── progress.py           ← Tracking: Test counting
├── prompts.py            ← Helper: Prompt loading
├── security.py           ← Safety: Sandbox restrictions
├── test_security.py      ← Tests: Security validation
├── .env                  ← Config: API keys
├── requirements.txt      ← Deps: Python packages
└── README.md             ← Docs: Getting started
```

### Folder-by-Folder Analysis

#### 📁 `generations/` - The Project Factory

**Location**: Root level (sibling to code files)

**Purpose**:
- Isolated workspace for each generated project
- Each generation gets its own `.git/` repository
- Complete isolation between projects

**Design Rationale**:
```
autonomous-coding/
└── generations/
    └── legal-workbench-v2/
        ├── .git/              ← ISOLATED GIT REPO
        ├── server/
        ├── public/
        ├── test/
        ├── feature_list.json
        └── app_spec.txt
```

**Why at root level?**
1. **Clear separation**: Generated code ≠ infrastructure code
2. **Easy cleanup**: Delete `generations/` without touching infrastructure
3. **Gitignore friendly**: Add `generations/` to `.gitignore` to exclude outputs
4. **Parallel projects**: Can run multiple generations simultaneously

**Creator's Intent**:
> "Keep generated projects completely separate from the agent infrastructure. The agent creates projects inside generations/, each with its own git history, so they can be developed, tested, and deployed independently."

---

#### 📁 `prompts/` - The Agent Brain

**Location**: Root level (sibling to generations/)

**Purpose**:
- Store prompt templates for different agent types
- Define agent behavior and workflow
- Version control agent instructions

**Structure**:
```
prompts/
├── app_spec.txt           ← Project specification template
├── initializer_prompt.md  ← Initializer agent instructions
└── coding_prompt.md       ← Coding agent instructions
```

**Why at root level?**
1. **Shared resource**: All generations use the same prompts
2. **Easy access**: Agent code can load from known location
3. **Version controlled**: Prompts are part of infrastructure
4. **Modifiable**: Users can customize agent behavior by editing prompts

**Creator's Intent**:
> "Prompts are the DNA of agents. Put them at root so they're easy to find, edit, and version control. When you change a prompt, all future generations use the new behavior."

---

#### 📄 Root-Level Python Files - The Engine

**Files**: `agent.py`, `autonomous_agent_demo.py`, `client.py`, `progress.py`, `prompts.py`, `security.py`

**Why flat structure?**
1. **Simplicity**: Easy to navigate for newcomers
2. **Quick imports**: `from agent import run_session`
3. **No over-engineering**: Don't create packages until needed
4. **Discoverability**: All code visible at one level

**Creator's Intent**:
> "This is a quickstart, not a framework. Keep it simple. When someone opens the folder, they should immediately see agent.py, understand what it does, and be able to modify it."

**File Responsibilities**:

| File | Purpose | Why Root Level |
|------|---------|---------------|
| `agent.py` | Core agent loop | Main logic - most important file |
| `autonomous_agent_demo.py` | Entry point | What users run - should be obvious |
| `client.py` | Claude SDK wrapper | Core abstraction - frequently imported |
| `progress.py` | Test tracking | Simple utility - doesn't need folder |
| `prompts.py` | Prompt loading | Helper for prompts/ folder |
| `security.py` | Sandbox rules | Core safety - critical visibility |

---

#### 📄 Configuration Files

**Files**: `.env`, `.env.example`, `requirements.txt`, `.gitignore`

**Location**: Root (standard practice)

**Rationale**:
- **Standard convention**: Everyone expects these at root
- **Tool compatibility**: Tools look for `.env`, `requirements.txt` at root
- **Discoverability**: First thing users see when opening folder

---

#### 📄 Documentation Files

**Files**: `README.md`, `AZURE_FOUNDRY.md`

**Location**: Root

**Rationale**:
- **GitHub convention**: README.md displays on repo page
- **Quick start**: Users see docs before diving into code
- **Feature docs**: AZURE_FOUNDRY.md explains optional feature

---

## Evolved Design: experiment_03/

### Design Philosophy Shift

The experiment structure evolved from **"minimal quickstart"** to **"research infrastructure"**:

```
experiment_03/
├── docs/                 ← NEW: Comprehensive documentation
├── prompts/              ← EXPANDED: Multiple agent types
├── reports/              ← NEW: Analysis and findings
├── runs/                 ← RENAMED: generations → runs
├── scripts/              ← NEW: Automation and utilities
├── *.py                  ← ENHANCED: Added experiment_logger.py
└── [configs]             ← Same: .env, requirements.txt, etc.
```

### New Folder Rationale

#### 📁 `docs/` - Knowledge Base

**NEW FOLDER** - Not in original

**Purpose**:
- Document experiment methodology
- Track architectural decisions
- Record critical requirements
- Maintain experiment history

**Structure**:
```
docs/
├── CRITICAL_REQUIREMENTS.md      ← Non-negotiable infrastructure
├── EXPERIMENT_03_STRATEGY.md     ← Experiment design
├── EXP_03_MANIFESTO.md           ← Core principles
├── README.md                     ← Quick overview
└── DIRECTORY_STRUCTURE_RATIONALE.md  ← This file
```

**Why needed?**
1. **Research context**: Experiments need documentation
2. **Onboarding**: New researchers need context
3. **Decision log**: Why we made certain choices
4. **Institutional knowledge**: Preserve learnings

**Creator's Intent** (ours):
> "Unlike a quickstart that users run once, experiments are ongoing research. We need to document hypotheses, methodology, results, and lessons learned. Put all this in docs/ to separate it from code."

---

#### 📁 `scripts/` - Automation Layer

**NEW FOLDER** - Not in original

**Purpose**:
- Automate repetitive tasks
- Provide utility functions
- Enable experiment setup
- Validate configurations

**Structure**:
```
scripts/
├── README.md                      ← Script documentation
├── autonomous_agent_demo.py       ← Main runner (moved from root)
├── check_feature_parity.py        ← Feature validation
├── monitor.py                     ← Real-time monitoring
├── setup_new_experiment.py        ← Experiment duplication
├── split_large_docs.py            ← Document processing
└── validate_experiment.py         ← Configuration checks
```

**Why needed?**
1. **Complexity growth**: More utilities as experiments mature
2. **Separation of concerns**: Scripts ≠ core infrastructure
3. **Discoverability**: All utilities in one place
4. **Maintenance**: Easier to find and update scripts

**Original vs New**:
```
autonomous-coding/
├── autonomous_agent_demo.py  ← At root (only one script)

experiment_03/
└── scripts/
    ├── autonomous_agent_demo.py      ← Moved here
    ├── check_feature_parity.py       ← Added
    ├── monitor.py                    ← Added
    ├── setup_new_experiment.py       ← Added
    ├── split_large_docs.py           ← Added
    └── validate_experiment.py        ← Added
```

**Creator's Intent** (ours):
> "As we added validation, monitoring, and setup scripts, root became cluttered. Move all executable scripts to scripts/ to keep root clean and make utilities discoverable."

---

#### 📁 `reports/` - Research Findings

**NEW FOLDER** - Not in original

**Purpose**:
- Store experiment results
- Document bug fixes
- Track performance analysis
- Maintain experiment timeline

**Structure**:
```
reports/
├── archive/                               ← Old reports
└── 2026-01-01_git-isolation-fix.md       ← Date-prefixed reports
```

**Why needed?**
1. **Research output**: Experiments produce findings
2. **Historical record**: Track what we learned when
3. **Separate from docs**: Reports = results, docs = methodology
4. **Date prefixed**: Automatic chronological ordering

**Creator's Intent** (ours):
> "Experiments generate reports: bug analyses, performance comparisons, design decisions. These are distinct from permanent documentation - they're timestamped findings. Put them in reports/ with YYYY-MM-DD_ prefixes for automatic ordering."

---

#### 📁 `runs/` - Renamed from `generations/`

**RENAMED** - Was `generations/` in original

**Why rename?**
1. **Clarity**: "runs" more clearly indicates experiment runs
2. **Research terminology**: "run" is standard in research
3. **Date-prefixed**: `runs/2026-01-01_name` shows when run happened
4. **Separation**: Each run is an isolated experiment

**Structure evolution**:
```
# Original
generations/
└── legal-workbench-v2/    ← Descriptive name

# Experiment
runs/
├── 2026-01-01_key-point-analysis/    ← Date + description
├── 2026-01-01_mvp-full/              ← Date + description
└── archive/                          ← Old runs
```

**Creator's Intent** (ours):
> "Rename to 'runs' for clarity and add date prefixes. This makes it obvious when each experiment ran and allows automatic chronological sorting. Much better for research workflows."

---

### Why Different Structures?

#### autonomous-coding/: Quickstart Mindset

**Goal**: Get users running quickly

**Principles**:
- Minimal structure
- Flat organization
- Obvious entry points
- Easy to modify
- Self-contained

**Trade-offs**:
- Less organization
- Harder to scale
- No research infrastructure
- Minimal documentation

---

#### experiment_03/: Research Infrastructure Mindset

**Goal**: Enable systematic research

**Principles**:
- Comprehensive documentation
- Clear organization
- Automation support
- Validation infrastructure
- Historical tracking

**Trade-offs**:
- More complex structure
- Steeper learning curve
- More files to maintain

---

## Critical Differences

### 1. Documentation Strategy

| Aspect | autonomous-coding | experiment_03 |
|--------|------------------|---------------|
| Location | README.md at root | docs/ folder |
| Scope | Getting started | Comprehensive methodology |
| Maintenance | Minimal | Ongoing updates |
| Purpose | User onboarding | Research knowledge base |

### 2. Script Organization

| Aspect | autonomous-coding | experiment_03 |
|--------|------------------|---------------|
| Location | Root level | scripts/ folder |
| Count | 1-2 scripts | 6+ scripts |
| Purpose | Run experiments | Automation suite |
| Documentation | Inline comments | scripts/README.md |

### 3. Output Management

| Aspect | autonomous-coding | experiment_03 |
|--------|------------------|---------------|
| Folder | generations/ | runs/ + reports/ |
| Naming | Descriptive | Date-prefixed |
| Organization | Flat | Archive system |
| Purpose | Project output | Experiment tracking |

### 4. Infrastructure Files

| File Type | autonomous-coding | experiment_03 |
|-----------|------------------|---------------|
| Core logic | agent.py (simple) | agent.py (enhanced) |
| Logging | print() statements | experiment_logger.py |
| Validation | test_security.py | check_feature_parity.py, validate_experiment.py |

---

## Key Insights

### What autonomous-coding Got Right

1. ✅ **Flat structure**: Easy to understand
2. ✅ **Isolated generations**: Each project has own .git
3. ✅ **Prompts separate**: Easy to customize behavior
4. ✅ **Security first**: sandbox.py at root for visibility
5. ✅ **Standard configs**: .env, requirements.txt at root

### What We Improved in experiment_03

1. ✅ **Documentation infrastructure**: docs/ folder
2. ✅ **Script organization**: scripts/ folder
3. ✅ **Research output**: reports/ folder
4. ✅ **Date-prefixed naming**: Automatic chronological order
5. ✅ **Validation infrastructure**: Feature parity, experiment validation
6. ✅ **Enhanced logging**: experiment_logger.py
7. ✅ **Automation**: setup_new_experiment.py

### What We Lost (Temporarily)

1. ❌ **Git isolation** - Fixed with `_initialize_git_repo()`
2. ❌ **Simplicity** - More folders = steeper learning curve
3. ❌ **Self-documenting** - Need to read docs/ to understand

---

## Design Recommendations

### For Quickstarts (Public Use)

**Keep it like autonomous-coding**:
- Flat structure
- Minimal folders
- README.md at root
- Everything visible at one level
- Focus on "get running fast"

### For Research Infrastructure (Internal Use)

**Evolve like experiment_03**:
- Organized folders (docs/, scripts/, reports/, runs/)
- Comprehensive documentation
- Automation infrastructure
- Validation tooling
- Historical tracking

### For Production Systems

**Go further**:
```
production-system/
├── docs/              ← Documentation
├── src/               ← Source code (not at root!)
│   ├── agents/
│   ├── tools/
│   └── utils/
├── tests/             ← Test suite
├── scripts/           ← Utilities
├── config/            ← Configuration
├── data/              ← Data files
└── deployments/       ← Deployment configs
```

---

## Conclusion

### The Fundamental Trade-off

**Simplicity vs Organization**

- **autonomous-coding**: Optimized for simplicity (quickstart users)
- **experiment_03**: Optimized for organization (researchers)

Both are correct for their purposes. The key is matching structure to intent:

- **Teaching/demos**: Use flat structure
- **Research**: Use organized structure
- **Production**: Use full engineering structure

### What We Learned

1. **Context matters**: Structure should match usage pattern
2. **Evolution is natural**: Simple → organized as needs grow
3. **Document rationale**: Future you will forget why
4. **Validate structure**: Use check_feature_parity.py
5. **Automate setup**: Use setup_new_experiment.py

---

**Last Updated**: 2026-01-01
**Maintained By**: Experiment Infrastructure Team
