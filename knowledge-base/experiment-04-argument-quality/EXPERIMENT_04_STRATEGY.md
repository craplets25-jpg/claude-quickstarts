# Experiment 04: Strategy for MVP Delivery

## Part 1: Experiment Results Analysis

### What Worked Well

| Aspect | Evidence | Impact |
|--------|----------|--------|
| **3-Agent Pipeline** | Librarian → Reviewer → Coder executed cleanly | Separation of concerns works |
| **Diagram Citations** | 71 Mermaid diagrams identified, 2 primary cited | Structural truth captured |
| **Tech-Agnostic Filtering** | Only 3/18 cards needed changes | Spec Librarian learned the rule |
| **Derivation vs Invention** | No IBM URLs in final invariants | Core hypothesis validated |
| **Test Derivation** | 18 tests, all behavior-focused | Triangulation works |

### What Needs Improvement

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Path Discovery** | Agent searches for files repeatedly | Copy canonical files to project dir |
| **JSON Format Variance** | feature_list.json was object not array | Standardize output schemas |
| **Progress Tracking Bug** | AttributeError on malformed JSON | Added format handling |
| **Single Test Per Session** | Only marked 1 test passing despite 12 working | Update all passing tests |

### Metrics from Test Run 03

- **Requirement Cards**: 18 (within 10-25 limit ✓)
- **Feature Tests**: 18 (within 10-20 limit ✓)
- **Cards Modified by Reviewer**: 3 (83% already clean)
- **Tests Passing After 1 Coding Session**: 12/18 (67%)
- **Pipeline Stages Completed**: 3/3 (100%)

---

## Part 2: DeepWiki Document Structure

### 12 Major Domains Identified

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DEBATER SDK DOCUMENTATION                            │
│                          (5,030 lines, 280 TOC entries)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. SDK OVERVIEW & GETTING STARTED                                          │
│     └── Purpose, Architecture, Installation, Authentication                 │
│                                                                             │
│  2. KEY POINT ANALYSIS (PRIMARY) ───────────────────────────── [COMPLEX]   │
│     ├── Core Components (KpAnalysisClient, TaskFuture, Utils)               │
│     ├── Domain Management (create, configure, cleanup)                      │
│     ├── Comment Upload & Processing                                         │
│     ├── Job Submission & Execution (async workflow)                         │
│     └── Result Retrieval & Status                                           │
│                                                                             │
│  3. KPA RESULTS & OUTPUT                                                    │
│     ├── KpaResult Data Model                                                │
│     ├── Data Transformation Pipeline                                        │
│     └── Export (CSV, JSON, DOCX, Graphs)                                    │
│                                                                             │
│  4. ADMIN CLIENT                                                            │
│     └── Reporting, User Management, System Monitoring                       │
│                                                                             │
│  5. SIMPLE NLP SERVICES ─────────────────────────────────────── [MVP!]     │
│     ├── Evidence Detection        ← IN PROGRESS                             │
│     ├── Claim Detection           ← SAME PATTERN                            │
│     ├── Argument Quality          ← SAME PATTERN                            │
│     ├── Pro/Con Analysis          ← SAME PATTERN                            │
│     └── Claim Boundaries          ← SAME PATTERN                            │
│                                                                             │
│  6. TEXT ANALYSIS CLIENTS                                                   │
│     ├── Clustering (moderate complexity)                                    │
│     ├── Term Relater                                                        │
│     ├── Term Wikifier                                                       │
│     └── Theme Extraction                                                    │
│                                                                             │
│  7. SDK ARCHITECTURE & INTERNALS                                            │
│     ├── AbstractClient Base Class                                           │
│     ├── Client Factory Pattern                                              │
│     ├── Batch Processing                                                    │
│     └── Service Communication Layer                                         │
│                                                                             │
│  8. ERROR HANDLING                                                          │
│     ├── Exception Hierarchy                                                 │
│     ├── Error Patterns Across Clients                                       │
│     └── Best Practices                                                      │
│                                                                             │
│  9. UTILITIES & HELPERS                                                     │
│     ├── Display & Output                                                    │
│     ├── Data Processing                                                     │
│     └── File System Operations                                              │
│                                                                             │
│ 10. PROJECT CONFIGURATION                                                   │
│     └── Dependencies, Build, Packaging                                      │
│                                                                             │
│ 11. PACKAGE STRUCTURE                                                       │
│     └── Module Organization, Import Hierarchy                               │
│                                                                             │
│ 12. RELEASE & LICENSE                                                       │
│     └── Version History, License Terms                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Artifact Inventory

### Complete Artifact Sets (Example + Response + Client + DeepWiki)

| Capability | Example | Response | Client File | Lines | Complexity |
|------------|---------|----------|-------------|-------|------------|
| Evidence Detection | ✓ | ✓ | claim_and_evidence_detection_client.py | 37 | **SIMPLE** |
| Claim Detection | ✓ | ✓ | claim_and_evidence_detection_client.py | 37 | **SIMPLE** |
| Argument Quality | ✓ | ✓ | argument_quality_client.py | 30 | **SIMPLE** |
| Pro/Con | ✓ | ✓ | pro_con_client.py | 32 | **SIMPLE** |
| Claim Boundaries | ✓ | ✓ | claim_boundaries_client.py | 25 | **SIMPLE** |
| Term Relater | ✓ | ✓ | term_relater_client.py | 47 | SIMPLE |
| Term Wikifier | ✓ | ✓ | term_wikifier_client.py | 41 | SIMPLE |
| Index Searcher | ✓ | ✓ | index_searcher_client.py | 52 | SIMPLE |
| Theme Extraction | ✓ | ✓ | theme_extraction_client.py | 89 | MODERATE |
| Clustering | ✓ | ✓ | clustering_client.py | 163 | MODERATE |
| Embedding | ✓ | ✗ | embedding_client.py | 80 | MODERATE |
| Key Points (KPA) | ✓ | ✓ | keypoints_client.py | 750+ | **COMPLEX** |
| Narrative Gen | ✗ | ✗ | narrative_generation_client.py | 360+ | COMPLEX |

### Shared Architecture Pattern

All SIMPLE clients follow the same pattern:

```python
# 1. Factory creates client
debater_api = DebaterApi(api_key)
client = debater_api.get_[service]_client()

# 2. Client has run() method
results = client.run(input_data)

# 3. Results are scores/values
for result in results:
    print(result)
```

This means: **Implement one, reuse for all.**

---

## Part 4: MVP Strategy

### MVP Definition: "Simple Text Analysis Suite"

**5 capabilities, all sharing the same pattern:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEXT ANALYSIS MVP                            │
│                                                                 │
│  Input: Text + Topic                                            │
│         ↓                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  Evidence   │  │    Claim    │  │  Argument   │     │   │
│  │  │  Detection  │  │  Detection  │  │   Quality   │     │   │
│  │  │   Score     │  │   Score     │  │   Score     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  │                                                         │   │
│  │  ┌─────────────┐  ┌─────────────┐                      │   │
│  │  │   Pro/Con   │  │    Claim    │                      │   │
│  │  │  Analysis   │  │ Boundaries  │                      │   │
│  │  │   Label     │  │   Spans     │                      │   │
│  │  └─────────────┘  └─────────────┘                      │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│         ↓                                                       │
│  Output: Analysis Report                                        │
│  - Evidence score: 0.89                                         │
│  - Claim score: 0.76                                            │
│  - Argument quality: 0.82                                       │
│  - Stance: PRO                                                  │
│  - Claim boundaries: [(0, 45), (67, 120)]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Why This MVP?

| Criterion | Evidence Detection Only | Text Analysis Suite (5) |
|-----------|------------------------|-------------------------|
| **Usable?** | Barely (single score) | Yes (complete analysis) |
| **Demonstrable?** | Limited | Rich output |
| **Effort Multiplier** | 1x | ~1.5x (shared infra) |
| **Value Multiplier** | 1x | 5x |
| **Pattern Reuse** | N/A | 80% code shared |

### MVP Phases

```
Phase 1: FOUNDATION (current)
├── Evidence Detection Client      ← 67% complete (12/18 tests)
├── Abstract Base Class            ← Done
├── Factory Pattern (DebaterApi)   ← Done
└── Test Infrastructure            ← Done

Phase 2: EXPANSION (next)
├── Claim Detection Client         ← Same file as Evidence!
├── Argument Quality Client        ← Same pattern
├── Pro/Con Client                 ← Same pattern
└── Claim Boundaries Client        ← Same pattern

Phase 3: INTEGRATION
├── Unified Text Analyzer API      ← Wraps all 5 clients
├── Single input, multiple outputs
└── Simple CLI or API endpoint
```

---

## Part 5: Expansion Strategy for Longer Runs

### Phase Constraint Updates

Update `phase_constraint.txt` to allow expanding scope:

```txt
PHASE 1 SCOPE: Choose ONE capability from:
- Evidence Detection    ← STARTED
- Claim Detection       ← NEXT (same client file)
- Argument Quality
- Pro/Con Analysis
- Claim Boundaries

After completing one capability (all tests pass),
you may proceed to the next in the list.

STOP after completing all 5.
```

### Session Planning

| Session | Agent | Task | Expected Output |
|---------|-------|------|-----------------|
| 1 | Spec Librarian | Derive specs for ALL 5 capabilities | 50-80 requirement cards, 50-80 tests |
| 2 | Spec Reviewer | Filter tech details | Cleaned cards |
| 3-10 | Coding Agent | Implement tests (5-10 per session) | Working code |
| 11 | Coding Agent | Integration wrapper | Unified API |

### Harness Configuration

```bash
# For MVP delivery, run until done (no max-iterations)
python autonomous_agent_demo.py \
  --project-dir ./generations/mvp-run-01 \
  --max-iterations 15

# Monitor progress
python monitor.py generations/mvp-run-01
```

### Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Capabilities Implemented | 5 | Count of working clients |
| Tests Passing | 80%+ | feature_list.json passes |
| No Invented Features | 0 | Review legacy_notes separation |
| Usable Demo | Yes | Can analyze text input |

---

## Part 6: Implementation Plan

### Immediate Next Steps

1. **Complete Evidence Detection** (6 remaining tests)
   ```bash
   python autonomous_agent_demo.py --project-dir ./generations/test-run-03 --max-iterations 5
   ```

2. **Update Phase Constraint for Multi-Capability**
   - Allow sequential capability implementation
   - Define clear boundaries between capabilities

3. **Create Capability-Specific Phase Specs**
   ```
   prompts/
   ├── phase_constraint.txt          # Overall scope
   ├── capability_evidence.txt       # Evidence Detection spec
   ├── capability_claim.txt          # Claim Detection spec
   ├── capability_argument.txt       # Argument Quality spec
   ├── capability_procon.txt         # Pro/Con spec
   └── capability_boundaries.txt     # Claim Boundaries spec
   ```

4. **Run Extended Spec Librarian Session**
   - Derive requirements for all 5 capabilities at once
   - Produce comprehensive requirement_cards.json
   - Produce comprehensive feature_list.json (50-80 tests)

5. **Run Spec Reviewer**
   - Ensure all 5 capabilities have tech-agnostic specs

6. **Run Coding Agent Loop**
   - 10-15 sessions to implement all tests
   - Monitor with `monitor.py`

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Agent drifts to other capabilities | Phase constraint locks to list of 5 |
| Tests become interdependent | Each capability has isolated test file |
| Spec bloat (too many requirements) | Hard limit: 20 cards per capability |
| Session timeout | Save progress frequently, resumable |

---

## Part 7: Recommended Experiment Run

### Command

```bash
cd /workspaces/claude-quickstarts/experiments/exp-04/experiment_04

# Fresh MVP run
python autonomous_agent_demo.py \
  --project-dir ./generations/mvp-01 \
  --max-iterations 20
```

### Expected Timeline

| Iteration | Agent | Focus |
|-----------|-------|-------|
| 1 | Spec Librarian | Derive specs for all 5 capabilities |
| 2 | Spec Reviewer | Filter tech details |
| 3-5 | Coding Agent | Evidence Detection (complete) |
| 6-8 | Coding Agent | Claim Detection |
| 9-11 | Coding Agent | Argument Quality |
| 12-14 | Coding Agent | Pro/Con |
| 15-17 | Coding Agent | Claim Boundaries |
| 18-20 | Coding Agent | Integration & cleanup |

### Deliverable

A working Python package that can:

```python
from text_analyzer import TextAnalyzer

analyzer = TextAnalyzer(api_key="...")
result = analyzer.analyze("Cannabis should be legalized because...")

print(result.evidence_score)      # 0.89
print(result.claim_score)         # 0.76
print(result.argument_quality)    # 0.82
print(result.stance)              # "PRO"
print(result.claim_boundaries)    # [(0, 45)]
```

---

## Conclusion

The experiment has validated that **derivation-based spec generation works**. The next step is to **scale up** by:

1. Expanding scope from 1 capability to 5
2. Running more coding sessions
3. Producing a usable MVP

The shared architecture pattern means we can deliver **5x the functionality** with approximately **1.5x the effort**.

**Recommended action:** Update the phase constraint and start an extended MVP run.
