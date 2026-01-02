# Knowledge Base - Experiment Documentation

**Purpose:** Central repository for all experiment documentation, strategies, reports, and learnings.

**Structure:** Each experiment has its own directory containing strategy docs, design decisions, and reports. Agent playgrounds in `experiments/` remain clean and contain only code.

---

## 📚 Experiment Index

### Experiment 04 - Argument Quality (Current)
**Directory:** `experiment-04-argument-quality/`
**Status:** ✅ Active - Source of Truth
**Capability:** Argument Quality scoring using LLMs
**Agent Playground:** `/experiments/04-argument-quality/experiment_04/`

**Key Documents:**
- [Manifesto](experiment-04-argument-quality/EXP_04_MANIFESTO.md) - Core principles
- [Strategy](experiment-04-argument-quality/EXPERIMENT_04_STRATEGY.md) - Implementation approach
- [Setup Guide](experiment-04-argument-quality/READY_TO_RUN.md) - How to run
- [Scaffold & Git Model](SCAFFOLD_AND_GIT_MODEL.md) - How cumulative scaffold works with isolated git

**Reports:**
- `reports/` - Run analyses and findings

---

### Experiment 03 - Claims Detection
**Directory:** N/A (kept in original location)
**Status:** Archive
**Agent Playground:** `/experiments/exp-03/experiment_03/`

### Experiment 02 - Key Point Analysis
**Directory:** N/A (kept in original location)
**Status:** Archive
**Agent Playground:** `/experiments/exp-02/experiment_02/`

### Experiment 01 - Evidence Detection
**Directory:** N/A (kept in original location)
**Status:** Archive
**Agent Playground:** `/experiments/01-evidence-detection/`

---

## 🏆 Source of Truth - Experiment 04

**Experiment 04 is the canonical template for creating new experiments.**

### Critical Features Checklist

All new experiments MUST be copied from Experiment 04 to ensure these features:

#### ✅ Infrastructure Features
- [x] **Independent Git per Run** - Each run/ directory gets isolated `.git/`
  - Function: `_initialize_git_repo()` in `agent.py`
  - Creates `.git/` + `.gitignore` automatically

- [x] **Git Instructions in Prompts** - Agent commits progress incrementally
  - File: `prompts/coding_prompt.md` Step 6b
  - Commands: `git add`, `git commit`, `git log`

- [x] **Progress Tracking** - Real-time metrics and logging
  - File: `progress.py`
  - Tracks tests passing, session time, status

- [x] **Experiment Logger** - Structured logging of all agent actions
  - File: `logger.py`
  - Logs to `runs/*/logs/`

- [x] **Agent Session Management** - Phases with proper handoffs
  - File: `agent.py`
  - Phases: Spec Librarian → Spec Reviewer → Coding Agent

#### ✅ Skill Integration Features
- [x] **deepwiki-navigator Skill** - Extract DeepWiki sections efficiently
  - Symlink: `custom_skills/deepwiki-navigator` → `_shared/skills/`
  - Scripts: `capability_scanner.py`, `section_extractor.py`, `doc_parser.py`
  - Mentioned in prompts: `spec_librarian_prompt.md`

- [x] **Shared Data Access** - DeepWiki and reference files
  - Symlinks properly configured
  - Paths in prompts use correct relative paths

#### ✅ Prompt Features
- [x] **Spec Librarian Prompt** - Derives requirements from canonical artifacts
  - File: `prompts/spec_librarian_prompt.md`
  - Creates: `requirement_cards.json` with full traceability
  - Features: Diagram emphasis, triangulation, rich context

- [x] **Spec Reviewer Prompt** - Minimal filtering (branding only)
  - File: `prompts/spec_reviewer_prompt.md`
  - Removes: IBM branding, vendor URLs
  - Keeps: Claude/Python/Anthropic details, all other info

- [x] **Coding Prompt** - Test-driven implementation
  - File: `prompts/coding_prompt.md`
  - Features: One test at a time, git commits, progress tracking

- [x] **Phase Constraint** - Defines experiment scope
  - File: `prompts/phase_constraint.txt`
  - Specifies which capability to implement

#### ✅ Validation Features
- [x] **Feature Parity Checker** - Validates critical features present
  - File: `scripts/check_feature_parity.py`
  - Checks: Git init, git prompts, progress tracking, isolation

- [x] **Experiment Validator** - Validates setup before running
  - File: `scripts/validate_experiment.py`
  - Checks: Symlinks, file references, prompts

#### ✅ Architecture Features
- [x] **Scaffold with Warnings** - Structure without over-specification
  - Files: `debater_sdk/ARCHITECTURE.md`, `base.py`, `sdk.py`
  - Clear warnings: "SCAFFOLD IS NOT THE SPEC"
  - Forces agent to read DeepWiki

- [x] **Claude SDK Integration** - Anthropic + Foundry support
  - File: `client.py`
  - Supports both API key types
  - Proper base URL detection

---

## 🚀 Creating New Experiments

### Process

**Always use the setup script with Experiment 04 as source:**

```bash
cd /workspaces/claude-quickstarts/experiments/_shared/infrastructure/scripts

python setup_new_experiment.py \
  --source 04-argument-quality \
  --target 05-new-capability \
  --capability "New Capability Name" \
  --num 5
```

**The script automatically:**
1. ✅ Validates source (exp-04) has all critical features
2. ✅ Copies from source to target
3. ✅ Updates all references (EXP_04 → EXP_05, etc.)
4. ✅ Creates symlinks to shared resources
5. ✅ Runs feature parity check on new experiment
6. ✅ Validates file references
7. ✅ Reports any issues found

**If validation fails:** The script will refuse to continue and tell you to copy from a complete source.

### Manual Verification (if needed)

After setup, verify critical features:

```bash
cd /workspaces/claude-quickstarts/experiments/05-new-capability/experiment_05

# Check git initialization
grep "_initialize_git_repo" agent.py

# Check git in prompts
grep "git commit" prompts/coding_prompt.md

# Run feature parity check
python scripts/check_feature_parity.py
```

---

## 📖 Cross-Experiment Learnings

### Patterns That Work
- **Document-Driven Derivation** - All requirements from canonical artifacts, no invention
- **Triangulation** - Validate requirements across DeepWiki + Examples + Client code
- **Freedom Through Constraints** - Pre-define architecture, derive behavior from docs
- **One Test at a Time** - Incremental implementation prevents overwhelming agents
- **Rich Test Context** - Include sources, invariants, legacy_notes in feature_list.json
- **Minimal Spec Review** - Only remove branding, preserve technical details
- **Two-Level Model** - Scaffold cumulative at experiment level, git isolation at run level

### Common Issues & Solutions

#### Issue: New experiment missing git initialization
**Cause:** Copied from exp-02 which didn't have it
**Solution:** Always copy from exp-04 (has git), setup script now validates

#### Issue: Information lost between requirement_cards and feature_list
**Cause:** Spec reviewer was over-stripping
**Solution:** Updated spec_reviewer_prompt.md to be minimal (branding only)

#### Issue: Agent doesn't use deepwiki-navigator skill
**Cause:** Skill not mentioned in prompts
**Solution:** Explicitly instruct in spec_librarian_prompt.md

#### Issue: Runs share parent git repo
**Cause:** No git initialization in agent.py
**Solution:** Added `_initialize_git_repo()` function, called automatically

---

## 📝 Documentation Standards

### For Each Experiment

Create in `knowledge-base/experiment-XX-capability/`:

1. **MANIFESTO.md** - Core principles for this experiment
2. **STRATEGY.md** - Implementation approach and decisions
3. **READY_TO_RUN.md** - Setup instructions and prerequisites
4. **reports/** - Run analyses, findings, issues encountered

### For Each Run

Agent creates in `experiments/.../experiment_XX/runs/YYYY-MM-DD_name/`:

1. **requirement_cards.json** - Derived requirements with full traceability
2. **feature_list.json** - Test specifications with context
3. **claude-progress.txt** - Session notes and metrics
4. **test_*.py** - Test implementation
5. **logs/** - Detailed agent logs

**Note:** Run outputs stay in agent playground, analysis/reports go to knowledge-base

---

## 🔧 Maintenance

### When Adding New Critical Feature

1. Add to Experiment 04 first
2. Update this README's "Critical Features Checklist"
3. Update `check_feature_parity.py` to validate it
4. Update `setup_new_experiment.py` validation if needed
5. Document in "Cross-Experiment Learnings"

### When Feature Parity Check Fails

The setup script will refuse to continue. Either:
- Fix the source experiment to include the feature
- Copy from exp-04 instead (always complete)

---

## 📊 Experiment Status

| Experiment | Status | Has Git | Has Skills | Source of Truth |
|------------|--------|---------|------------|-----------------|
| 01 - Evidence Detection | Archive | ❌ | ❌ | No |
| 02 - Key Point Analysis | Archive | ❌ | ❌ | No |
| 03 - Claims Detection | Archive | ✅ | ❌ | No |
| 04 - Argument Quality | **Active** | ✅ | ✅ | **YES** |

**Legend:**
- ✅ Feature present
- ❌ Feature missing
- **Source of Truth** = Safe to copy for new experiments

---

## 📞 Quick Reference

### File Locations

```
claude-quickstarts/
├── knowledge-base/              # THIS - All documentation
│   ├── README.md               # You are here
│   └── experiment-04-*/        # Exp-04 docs
│
├── experiments/                # Agent playgrounds only
│   ├── _shared/
│   │   ├── infrastructure/    # Setup scripts
│   │   ├── skills/            # deepwiki-navigator
│   │   └── data/              # DeepWiki, reference files
│   │
│   └── 04-argument-quality/
│       └── experiment_04/      # Agent code (no docs!)
│           ├── agent.py
│           ├── prompts/
│           ├── scripts/
│           └── runs/          # Each has own .git/
```

### Key Scripts

- **Setup:** `experiments/_shared/infrastructure/scripts/setup_new_experiment.py`
- **Validate:** `experiments/*/experiment_*/scripts/check_feature_parity.py`
- **Run:** `experiments/*/experiment_*/scripts/autonomous_agent_demo.py`

### Getting Help

1. Check this README first
2. Review experiment-04 documentation
3. Check "Cross-Experiment Learnings" section
4. Review git isolation fix: `experiments/exp-03/experiment_03/reports/2026-01-01_git-isolation-fix.md`

---

**Last Updated:** 2026-01-02
**Maintained By:** Autonomous Coding Experiments Team
**Source of Truth:** Experiment 04 - Argument Quality
