# Experiment 02: Documentation

**Experiment**: Document-Driven Derivation
**Hypothesis**: Derivation instead of Invention
**Status**: Active

---

## Overview

Experiment 02 tests whether AI agents can derive working implementations from canonical documentation (diagrams, examples, API docs) without inventing features.

**Core Principle**: If it's not in the diagrams, examples, or documentation, it's not a requirement.

---

## Documents in This Folder

### EXPERIMENT_02_STRATEGY.md

**Purpose**: Complete analysis and strategy for MVP delivery

**Contents**:
- Part 1: Experiment results analysis (test-run-03)
- Part 2: DeepWiki document structure (12 major domains)
- Part 3: Artifact inventory (13 capabilities identified)
- Part 4: MVP strategy (5 simple text analysis capabilities)
- Part 5: Expansion strategy for longer runs
- Part 6: Implementation plan
- Part 7: Recommended experiment run

**Key Sections**:
- What worked well (3-agent pipeline, diagram citations, tech-agnostic filtering)
- What needs improvement (path discovery, JSON format, progress tracking)
- MVP definition: Text Analysis Suite (5 capabilities)
- Success criteria and metrics

### EXP_02_MANIFESTO.md

**Purpose**: Core principles and constraints

**Contents**:
- Derivation paradigm rules
- Ontology (canonical sources only)
- Forbidden behaviors
- Phase constraints

**Key Rule**: "No requirement exists until you can cite its source in diagrams, examples, or documentation."

---

## Key Concepts

### 1. Derivation vs Invention

**Derivation** (✅ Allowed):
- Reading diagrams to understand data flow
- Extracting input/output shapes from examples
- Observing validation patterns from response files
- Citing line numbers and sources

**Invention** (❌ Forbidden):
- Adding features not in documentation
- Copying vendor-specific URLs/endpoints
- Making assumptions about implementation
- Creating tests for non-existent requirements

### 2. Three-Agent Pipeline

```
SPEC LIBRARIAN          SPEC REVIEWER           CODING AGENT
┌─────────────┐        ┌─────────────┐         ┌─────────────┐
│ Read docs   │   →    │ Filter tech │    →    │ Implement   │
│ Find        │        │ details to  │         │ tests one   │
│ diagrams    │        │ legacy_notes│         │ at a time   │
│ Derive      │        │             │         │             │
│ requirements│        │ Keep only   │         │ Update ALL  │
│ Create tests│        │ behavior    │         │ passing     │
└─────────────┘        └─────────────┘         └─────────────┘
```

### 3. Diagram-First Approach

**71 Mermaid diagrams** in DeepWiki are PRIMARY sources because:
1. Diagrams show STRUCTURE (inheritance, composition, data flow)
2. Diagrams are UNAMBIGUOUS (A → B → C is precise)
3. Diagrams are TECH-AGNOSTIC (patterns, not implementation)
4. Diagrams capture what text omits

**Example**: Processing Pipeline diagram (lines 2686-2711) shows:
```
Input → Validation → Transform → BatchProcess → Results → Output
```

This single diagram generates multiple requirements:
- ED-002: Input format
- ED-003: Validation (empty strings)
- ED-006: Batch processing
- ED-007: Order preservation

### 4. Tech-Agnostic Filtering

**INVARIANTS** (keep as requirements):
- Input/output shapes
- Validation rules
- Ordering guarantees
- Error conditions
- Architectural patterns

**LEGACY_NOTES** (move here):
- Specific URLs: `https://motion-evidence.debater.res.ibm.com`
- Timeouts: `100 seconds`
- Method names: `run_in_batch`
- Error messages: `"empty input argument in pair"`

---

## Success Metrics

From test-run-03:
- ✅ 18 requirement cards (within 10-25 limit)
- ✅ 18 feature tests (within 10-20 limit)
- ✅ 83% cards already tech-agnostic (only 3 needed changes)
- ✅ 67% tests passing after 1 coding session
- ✅ 100% pipeline stages completed

---

## MVP Target

**5 Capabilities** (all sharing same pattern):
1. Evidence Detection ← Started
2. Claim Detection
3. Argument Quality
4. Pro/Con Analysis
5. Claim Boundaries

**Expected Deliverable**:
```python
from text_analyzer import TextAnalyzer

analyzer = TextAnalyzer(api_key="...")
result = analyzer.analyze("Cannabis should be legalized...")

print(result.evidence_score)      # 0.89
print(result.claim_score)         # 0.76
print(result.argument_quality)    # 0.82
print(result.stance)              # "PRO"
print(result.claim_boundaries)    # [(0, 45)]
```

---

## Related Directories

- `../runs/` - All experiment runs with date prefixes
- `../reports/` - Analysis reports and evaluations
- `../prompts/` - Agent prompt templates
- `../scripts/` - Monitoring and execution utilities

---

## Quick Links

- [View all runs](../runs/)
- [View all reports](../reports/)
- [Experiment Strategy](./EXPERIMENT_02_STRATEGY.md)
- [Manifesto (Core Rules)](./EXP_02_MANIFESTO.md)

---

## Timeline

- **2026-01-01 AM**: Initial design and planning
- **2026-01-01 PM**: test-run-03 (validated approach)
- **2026-01-01 PM**: Prompt fixes applied
- **2026-01-01 PM**: verify-prompt-fixes (validated fixes)
- **2026-01-01 PM**: Next → full MVP run (20 iterations)

---

## Contact

For questions about this experiment:
1. Read this README first
2. Check EXPERIMENT_02_STRATEGY.md for detailed analysis
3. Review recent reports in ../reports/
4. Examine latest run in ../runs/
