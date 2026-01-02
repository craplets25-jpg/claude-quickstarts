# Experiment 04: Argument Quality - READY TO RUN

## ✅ Setup Complete

Experiment 04 has been properly configured for autonomous agent execution.

### What's Been Created

**1. Proper Experiment Structure (copied from exp-02)**
- ✅ All workflow prompts (spec_librarian, spec_reviewer, coding, oracle)
- ✅ Phase constraints and manifesto (updated to Experiment 04)
- ✅ Agent infrastructure (agent.py, prompts.py, logger, progress)
- ✅ Autonomous agent runner (scripts/autonomous_agent_demo.py)
- ✅ Symlinks to shared resources (DeepWiki, reference files)

**2. Architecture Scaffold (with strong warnings)**
- ✅ `debater_sdk/ARCHITECTURE.md` - **"SCAFFOLD IS NOT THE SPEC"**
- ✅ `debater_sdk/base.py` - Abstract base with `_call_llm()` helper
- ✅ `debater_sdk/sdk.py` - Factory pattern
- ✅ `debater_sdk/services/` - Service stubs with warnings
- ✅ **All documentation stripped down** - forces agent to read DeepWiki

**3. Adapted Prompts**
- ✅ phase_constraint.txt - Only allows Argument Quality
- ✅ spec_librarian_prompt.md - Updated examples for Argument Quality
- ✅ Prompts already configured for deepwiki-navigator skill

### Key Design Decisions

**Scaffold Philosophy:**
- Scaffold defines STRUCTURE (architecture pattern)
- DeepWiki defines REQUIREMENTS (behavior)
- Agent must read DeepWiki, not assume from scaffold

**Warnings Added:**
```
⚠️ THIS SCAFFOLD IS NOT THE SPECIFICATION.
Read DeepWiki to derive requirements.
```

**What We're Building:**
- Service LOGIC using LLMs (not API client wrappers)
- Reference: Client → HTTP → Service
- Our: Service → LLM (Claude) → Results

### How to Run

```bash
cd /workspaces/claude-quickstarts/experiments/04-argument-quality/experiment_04

python scripts/autonomous_agent_demo.py \
  --project-dir runs/2026-01-02_argument-quality \
  --model sonnet \
  --max-iterations 20
```

### What the Agent Will Do

**Phase 1: Spec Librarian**
1. Use deepwiki-navigator skill to extract Argument Quality sections
2. Read examples and reference client
3. Derive requirement_cards.json (with AQ-001, AQ-002, etc.)
4. Create feature_list.json (tests)

**Phase 2: Coding**
1. Implement `ArgumentQualityService._process_batch()`
2. Design LLM prompts for quality scoring
3. Pass tests one by one
4. Iterate until complete

### Expected Outcome

- ArgumentQualityService fully implemented
- All P0 tests passing
- Service uses Claude to score argument quality
- Architecture follows the scaffold pattern
- Behavior matches DeepWiki requirements

---

**Status:** READY FOR AUTONOMOUS RUN
**Date:** 2026-01-02
**Capability:** Argument Quality (P0)
