# Scaffold and Git Model - Two-Level Architecture

## Overview

This document explains how the **cumulative scaffold** (debater_sdk/) and **independent git per run** work together without conflicting.

---

## The Two-Level Model

### Level 1: EXPERIMENT Level - Cumulative Scaffold

The `debater_sdk/` scaffold is **copied between experiments** at setup time.

```
exp-04 (Argument Quality)     exp-05 (Evidence Detection)    exp-06 (KPA)
├── debater_sdk/              ├── debater_sdk/               ├── debater_sdk/
│   ├── base.py      ──COPY─► │   ├── base.py       ──COPY─► │   ├── base.py
│   ├── sdk.py                │   ├── sdk.py                 │   ├── sdk.py
│   └── services/             │   └── services/              │   └── services/
│       └── argument_quality/ │       ├── argument_quality/  │       ├── argument_quality/
│                             │       └── evidence/  ◄─NEW   │       ├── evidence/
│                             │                              │       └── kpa/  ◄─NEW
```

**Key characteristics:**
- Scaffold grows incrementally across experiments
- Each new experiment **inherits** the previous experiment's work
- Copy happens via `setup_new_experiment.py`
- This is a ONE-TIME copy at experiment creation

### Level 2: RUN Level - Git Isolation

Each run within an experiment has its **own isolated `.git/` repository**.

```
exp-05/
├── debater_sdk/              # Scaffold (copied from exp-04)
├── agent.py                  # Creates .git/ in each run
└── runs/
    ├── 2026-01-02_evidence-v1/
    │   ├── .git/             # Agent's commits for THIS run
    │   ├── test_evidence.py  # Agent created this
    │   └── feature_list.json
    │
    ├── 2026-01-02_evidence-v2/
    │   ├── .git/             # Agent's commits for THIS run
    │   └── ...
    │
    └── 2026-01-03_evidence-final/
        ├── .git/             # Agent's commits for THIS run
        └── ...
```

**Key characteristics:**
- Each run is ISOLATED from other runs
- Git tracks what the agent builds/changes during that run
- Agent commits progress incrementally
- Allows diffing between runs to see what changed

---

## Why They Don't Conflict

| Aspect | Scaffold (Experiment Level) | Git (Run Level) |
|--------|----------------------------|-----------------|
| **When** | At experiment creation | During each run |
| **What** | Copies debater_sdk/ directory | Tracks agent's changes |
| **How often** | Once per experiment | Once per run |
| **Purpose** | Inherit previous work | Track current work |
| **Mechanism** | File copy | Git versioning |

**The scaffold is input, git tracks output:**
1. Scaffold provides the **starting point** for the agent
2. Git tracks what the agent **builds from that starting point**

---

## Workflow Example

### Creating Experiment 05

```bash
# 1. Setup copies scaffold from exp-04
python setup_new_experiment.py \
  --source 04-argument-quality \
  --target 05-evidence-detection \
  --capability "Evidence Detection" \
  --num 5

# Result: exp-05/debater_sdk/ = copy of exp-04/debater_sdk/
```

### Running Experiment 05

```bash
cd experiments/05-evidence-detection

# 2. Each run gets isolated git
python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-02_evidence-v1 \
  --model sonnet \
  --max-iterations 20

# Result:
# - runs/2026-01-02_evidence-v1/.git/ created
# - Agent works on Evidence Detection
# - Agent commits progress to run's git
# - debater_sdk/ may be modified (agent adds Evidence service)
```

### After Successful Run

```bash
# The successful run's work exists in:
# - runs/2026-01-02_evidence-v1/debater_sdk/services/evidence/

# To propagate to exp-06, you would:
# 1. Copy the successful implementation to exp-05's main debater_sdk/
# 2. Use exp-05 as source for exp-06 setup

# OR simply use the successful run's scaffold directly
```

---

## The Complete Picture

```
claude-quickstarts/
├── experiments/
│   ├── _shared/                    # Shared resources
│   │   └── infrastructure/
│   │       └── scripts/
│   │           └── setup_new_experiment.py  # Copies scaffold
│   │
│   ├── 04-argument-quality/        # SOURCE OF TRUTH
│   │   ├── debater_sdk/            # Has Argument Quality service
│   │   │   └── services/
│   │   │       └── argument_quality/
│   │   ├── agent.py                # Creates .git/ in runs/
│   │   └── runs/
│   │       └── YYYY-MM-DD_name/
│   │           └── .git/           # Agent's commits
│   │
│   └── 05-evidence-detection/      # Created from exp-04
│       ├── debater_sdk/            # Inherited from exp-04
│       │   └── services/
│       │       └── argument_quality/  # From exp-04
│       │       └── evidence/          # Built by agent
│       ├── agent.py
│       └── runs/
│           └── YYYY-MM-DD_name/
│               └── .git/           # Agent's commits
```

---

## FAQ

### Q: Does the run's git track changes to debater_sdk/?

**A:** Yes! The run's git tracks ALL changes the agent makes, including to debater_sdk/. This is intentional - it shows what the agent built.

### Q: How do I know which run's debater_sdk/ to use for the next experiment?

**A:** Use the **successful run** - the one where all tests pass. That run's debater_sdk/ contains the complete implementation.

### Q: What if multiple runs have different implementations?

**A:** Each run is an independent attempt. Compare them:
```bash
# Compare two runs
diff -r runs/run-1/debater_sdk/ runs/run-2/debater_sdk/

# Use git to see what each run built
cd runs/run-1
git log --oneline
git diff HEAD~5 HEAD -- debater_sdk/
```

### Q: Should I commit the experiment-level debater_sdk/ to the main repo?

**A:** The experiment's debater_sdk/ is the **starting scaffold**. After a successful run, you might want to:
1. Keep the run's implementation as the "gold" version
2. Copy the successful implementation back to the experiment's scaffold
3. Use that as the source for the next experiment

### Q: Why not just have one big git repo for everything?

**A:** Run isolation provides:
- **Clean diffs**: See exactly what one agent session produced
- **Reproducibility**: Each run is self-contained
- **Comparison**: Easy to compare different attempts
- **Recovery**: If one run fails, others are unaffected

---

## Summary

| Level | What | When | Purpose |
|-------|------|------|---------|
| **Experiment** | debater_sdk/ scaffold | At setup | Inherit previous work |
| **Run** | .git/ repository | At run start | Track agent progress |

**Think of it as:**
- Scaffold = "what you start with" (inherited)
- Git = "what you build" (tracked)

---

**Last Updated:** 2026-01-02
**Related:**
- `knowledge-base/QUICK_START.md` - How to create experiments
- `knowledge-base/README.md` - Critical features checklist
- `experiments/_shared/infrastructure/scripts/setup_new_experiment.py` - Setup script
