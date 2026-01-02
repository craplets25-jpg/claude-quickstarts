# Custom Skills Analysis for Experiment 03

**Purpose**: Analyze how Claude custom skills could enhance our 3-agent pipeline

**Date**: 2026-01-02

---

## Overview: What Are Custom Skills?

**Custom skills** are specialized expertise packages that teach Claude organizational workflows and domain knowledge. They consist of:

- **SKILL.md** (required): YAML frontmatter + markdown instructions
- **Scripts** (optional): Python/JavaScript executable code
- **Resources** (optional): Templates, data files, documentation

### Key Benefits for Our Project

| Benefit | Application to Experiment 03 |
|---------|------------------------------|
| **Codify organizational knowledge** | Document our derivation paradigm rules |
| **Ensure consistency** | All agents follow same tech-agnostic filtering |
| **Automate complex workflows** | Standardize diagram parsing, test generation |
| **Version control** | Track improvements to agent instructions |

---

## Our 3-Agent Pipeline

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

---

## Skill Opportunity 1: Diagram Analysis (SPEC LIBRARIAN)

### Current Challenge

The SPEC LIBRARIAN must:
1. Find all 71 Mermaid diagrams in DeepWiki
2. Parse diagram syntax to understand structure
3. Extract data flow, inheritance, composition patterns
4. Convert diagram nodes into test requirements
5. Cite line numbers for traceability

**Problem**: Each agent reinvents diagram parsing approach

### Proposed Skill: `diagram-requirement-extraction`

```
diagram-requirement-extraction/
├── SKILL.md                    # Instructions for parsing Mermaid diagrams
├── EXAMPLES.md                 # 5-10 examples of good requirement extraction
├── scripts/
│   └── diagram_parser.py       # Helper to extract nodes/edges
└── templates/
    └── requirement_card.md     # Template for requirement cards
```

#### SKILL.md Contents

```yaml
---
name: diagram-requirement-extraction
description: Extract tech-agnostic behavioral requirements from Mermaid diagrams in technical documentation
---

# Diagram Requirement Extraction

## Purpose

Parse Mermaid diagrams to derive behavioral requirements without inventing features.

## Core Principle

> **Diagrams show STRUCTURE (inheritance, composition, data flow)**
> Diagrams are UNAMBIGUOUS (A → B → C is precise)
> Diagrams are TECH-AGNOSTIC (patterns, not implementation)

## Step-by-Step Process

### 1. Locate Diagrams

Search for Mermaid code blocks:
- ````mermaid` markers
- Record line numbers for citation

### 2. Classify Diagram Type

| Type | What It Shows | Requirements to Extract |
|------|---------------|------------------------|
| **Flowchart** | Process flow | Input → Output, branching logic |
| **Class Diagram** | Inheritance | Parent-child relationships, composition |
| **Sequence** | Interactions | Message passing, order of operations |
| **State** | Transitions | Valid state changes, triggers |

### 3. Extract Nodes and Edges

For each diagram:
- List all nodes (entities, states, actions)
- List all edges (relationships, flows, transitions)
- Note any annotations (labels, conditions)

### 4. Derive Requirements

Convert diagram elements to requirements:

**Flowchart Example**:
```mermaid
Input → Validate → Transform → Output
```

Becomes:
- REQ-001: System accepts input
- REQ-002: System validates input (cite validation rules if shown)
- REQ-003: System transforms validated input
- REQ-004: System produces output
- REQ-005: Order is preserved (Input → Validate → Transform → Output)

**Class Diagram Example**:
```mermaid
Animal <|-- Dog
Animal <|-- Cat
```

Becomes:
- REQ-001: Dog inherits from Animal
- REQ-002: Cat inherits from Animal
- REQ-003: Dogs and Cats share Animal interface

### 5. Create Requirement Cards

For each requirement:
```markdown
### REQ-XXX: [Brief Description]

**Source**: [File:LineNumber]
**Diagram Type**: [Flowchart/Class/Sequence/State]
**Derived From**: [Specific nodes/edges]

**Requirement**:
[Clear statement of what must happen]

**Test Criteria**:
[How to verify this requirement]
```

## What NOT to Do

❌ **Don't invent features not shown in diagram**
❌ **Don't add vendor-specific implementation details**
❌ **Don't assume behavior not explicitly shown**
❌ **Don't create requirements from diagram comments alone**

## Examples

See EXAMPLES.md for 10 complete examples showing:
- Processing Pipeline diagram → 6 requirements
- Class Hierarchy diagram → 4 requirements
- State Machine diagram → 8 requirements
```

#### Benefits

1. **Consistency**: Every SPEC LIBRARIAN follows same parsing approach
2. **Quality**: Validated examples prevent common mistakes
3. **Speed**: Helper scripts reduce parsing time
4. **Reusability**: Same skill works across all DeepWiki capabilities
5. **Versioning**: Improve parsing techniques over time

---

## Skill Opportunity 2: Tech-Agnostic Filtering (SPEC REVIEWER)

### Current Challenge

The SPEC REVIEWER must distinguish:

**KEEP (tech-agnostic invariants)**:
- Input/output shapes
- Validation rules
- Ordering guarantees
- Error conditions
- Architectural patterns

**MOVE TO LEGACY_NOTES**:
- Specific URLs: `https://motion-evidence.debater.res.ibm.com`
- Timeouts: `100 seconds`
- Method names: `run_in_batch`
- Error messages: `"empty input argument in pair"`

**Problem**: Inconsistent filtering leads to vendor-specific details leaking into requirements

### Proposed Skill: `tech-agnostic-requirement-filter`

```
tech-agnostic-requirement-filter/
├── SKILL.md                    # Filtering rules and examples
├── REFERENCE.md                # Comprehensive list of patterns
├── scripts/
│   └── pattern_detector.py     # Detect vendor-specific patterns
└── tests/
    └── test_filtering.py       # Validate filtering logic
```

#### SKILL.md Contents

```yaml
---
name: tech-agnostic-requirement-filter
description: Filter technical documentation to separate tech-agnostic behavioral requirements from vendor-specific implementation details
---

# Tech-Agnostic Requirement Filter

## Purpose

Review requirement cards and filter vendor-specific details to `legacy_notes.md` while preserving tech-agnostic behavioral requirements.

## Core Principle

> **INVARIANTS stay → Implementation details go to legacy_notes**

## Decision Framework

For each statement in a requirement, ask:

### Question 1: Is it implementation-specific?

❌ **Move to legacy_notes**:
- Specific URLs/endpoints
- Vendor names (IBM, AWS, etc.)
- Method/function names from vendor API
- Specific timeouts/limits
- Error message text
- Configuration values

✅ **Keep as requirement**:
- "System accepts input"
- "Input must be validated"
- "Empty strings are rejected"
- "Order is preserved"
- "Results are returned as list"

### Question 2: Can multiple implementations satisfy it?

✅ **Keep**: "System validates input format"
  → Can be implemented via regex, JSON schema, custom validator

❌ **Move**: "System uses IBM Watson API endpoint"
  → Only one implementation possible

### Question 3: Is it about WHAT or HOW?

✅ **Keep**: "WHAT must happen" (behavior)
❌ **Move**: "HOW it happens" (implementation)

## Pattern Recognition

### URLs and Endpoints

**Original**:
```
Service endpoint: https://motion-evidence.debater.res.ibm.com/evidence_detection
```

**Filtered**:
```markdown
**REQUIREMENT CARD**:
REQ-001: System provides evidence detection service via HTTP API

**LEGACY_NOTES**:
- IBM implementation uses: https://motion-evidence.debater.res.ibm.com/evidence_detection
```

### Timeouts and Limits

**Original**:
```
Request timeout: 100 seconds
Max batch size: 1000 items
```

**Filtered**:
```markdown
**REQUIREMENT CARD**:
REQ-002: System supports batch processing of multiple items

**LEGACY_NOTES**:
- IBM implementation: timeout=100s, max_batch=1000
```

### Error Messages

**Original**:
```
Returns error: "empty input argument in pair"
```

**Filtered**:
```markdown
**REQUIREMENT CARD**:
REQ-003: System validates that input pairs contain non-empty arguments

**LEGACY_NOTES**:
- IBM error message: "empty input argument in pair"
```

### Method Names

**Original**:
```
Call run_in_batch() to process multiple items
```

**Filtered**:
```markdown
**REQUIREMENT CARD**:
REQ-004: System provides batch processing capability

**LEGACY_NOTES**:
- IBM method name: run_in_batch()
```

## Workflow

### Step 1: Read Requirement Card

Identify all statements that could be vendor-specific

### Step 2: Apply Decision Framework

For each statement, apply 3 questions above

### Step 3: Separate Concerns

- **Keep**: Behavioral requirements (WHAT)
- **legacy_notes.md**: Implementation details (HOW)

### Step 4: Preserve Traceability

Always maintain line number citations in both locations

## Quality Checks

Before completing filtering:

- [ ] All URLs moved to legacy_notes?
- [ ] All vendor names moved?
- [ ] All method names moved?
- [ ] All error message text moved?
- [ ] All timeout/limit values moved?
- [ ] Requirements still testable without legacy_notes?
- [ ] Citations preserved?

## Examples

See REFERENCE.md for 20+ examples across:
- API endpoints
- Authentication methods
- Data formats
- Error handling
- Batch processing
- Rate limiting
```

#### Benefits

1. **Precision**: Clear decision framework prevents ambiguity
2. **Completeness**: Pattern library covers all common cases
3. **Quality**: Quality checklist ensures nothing missed
4. **Teaching**: New reviewers learn from validated examples
5. **Automation**: Scripts can flag potential vendor-specific patterns

---

## Skill Opportunity 3: TDD Workflow (CODING AGENT)

### Current Challenge

The CODING AGENT must:
1. Read **one test** from feature_list.json
2. Implement code to pass that test
3. Run test suite to verify
4. Update feature_list.json to mark test as passing
5. Commit progress to git
6. Repeat until all tests pass
7. Stop early if all tests passing

**Problem**: Agents sometimes:
- Try to implement multiple tests at once
- Forget to update feature_list.json
- Skip git commits
- Don't check for early stopping

### Proposed Skill: `test-driven-development-workflow`

```
test-driven-development-workflow/
├── SKILL.md                    # Step-by-step TDD process
├── COMMIT_TEMPLATES.md         # Git commit message templates
├── scripts/
│   └── progress_tracker.py     # Update feature_list.json automatically
└── checklists/
    └── iteration_checklist.md  # Per-iteration verification
```

#### SKILL.md Contents

```yaml
---
name: test-driven-development-workflow
description: Implement features using test-driven development with one test at a time, progress tracking, and git commits
---

# Test-Driven Development Workflow

## Purpose

Implement features incrementally, one test at a time, with progress tracking and git commits after each passing test.

## Core Principle

> **ONE TEST → Implement → Verify → Commit → REPEAT**

## The Workflow

### Step 0: Orient

```bash
# Check git history
git log --oneline -10

# Check current progress
cat feature_list.json | grep -A5 "passing"
```

### Step 1: Find Next Test

Read `feature_list.json` to find FIRST test where `"passing": false`

```json
{
  "id": "TEST-003",
  "description": "Validate empty string rejection",
  "passing": false
}
```

**IMPORTANT**: Implement **ONLY THIS ONE TEST**

### Step 2: Read Test Code

Locate test in test file:
```bash
grep -n "TEST-003" test_*.py
```

Read test implementation to understand:
- What input it provides
- What output it expects
- What assertions it makes

### Step 3: Implement Minimal Code

Write **ONLY** the code needed to pass this **ONE TEST**

Don't add:
- Features for future tests
- "Nice to have" functionality
- Extra error handling not required by test
- Code for tests not yet implemented

### Step 4: Run Tests

```bash
pytest test_file.py::test_name -v
```

If test fails:
- Read error message
- Fix specific issue
- Re-run test
- Repeat until passing

### Step 5: Update Progress

When test passes, update `feature_list.json`:

```json
{
  "id": "TEST-003",
  "description": "Validate empty string rejection",
  "passing": true  // ← Changed to true
}
```

### Step 6: Commit to Git

```bash
git status
git add *.py *.json
git commit -m "Implement TEST-003: Validate empty string rejection

- Added validation in parse_input()
- Empty strings now raise ValueError
- 3/18 tests now passing

\ud83e\udd16 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Step 7: Check for Completion

Count passing tests:
```bash
grep '"passing": true' feature_list.json | wc -l
grep '"passing": false' feature_list.json | wc -l
```

If all tests passing:
- **STOP IMMEDIATELY**
- Report completion
- Exit early (don't start new tests)

If tests remain:
- Return to Step 1
- Implement next failing test

## Iteration Checklist

After each test:

- [ ] Only ONE test was implemented
- [ ] Test passes when run
- [ ] feature_list.json updated
- [ ] Changes committed to git
- [ ] Commit message follows template
- [ ] Checked if all tests now passing

## Common Mistakes to Avoid

❌ **Implementing multiple tests at once**
  → Implement one test, then loop back

❌ **Forgetting to update feature_list.json**
  → Always update before committing

❌ **Skipping git commits**
  → Commit after each passing test

❌ **Continuing after all tests pass**
  → Check for completion and stop early

❌ **Adding features not required by current test**
  → Minimal implementation only

## Git Commit Message Template

```
Implement TEST-XXX: [Brief description]

- [What code was added/changed]
- [What test now passes]
- [X/Y tests now passing]
- [Any notable decisions or tradeoffs]

\ud83e\udd16 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Progress Tracking

Each run maintains:
- `feature_list.json`: Source of truth for test status
- `claude-progress.txt`: Human-readable notes
- Git history: Complete implementation timeline

## Early Stopping Logic

```python
import json

def check_completion(feature_list_path):
    with open(feature_list_path) as f:
        data = json.load(f)

    tests = data.get('features', [])
    passing = sum(1 for t in tests if t.get('passing'))
    total = len(tests)

    if passing == total:
        print(f"✅ All {total} tests passing - STOPPING EARLY")
        return True
    else:
        print(f"⚙️ Progress: {passing}/{total} tests passing - CONTINUING")
        return False
```

## Examples

See COMMIT_TEMPLATES.md for examples of:
- Good commit messages (clear, specific)
- Bad commit messages (vague, multi-test)
- Progress tracking patterns
- Early stopping scenarios
```

#### Benefits

1. **Discipline**: Enforces one-test-at-a-time approach
2. **Traceability**: Git history shows exactly when each test passed
3. **Efficiency**: Early stopping prevents wasted iterations
4. **Consistency**: All coding agents follow same workflow
5. **Debugging**: Clear commit history makes rollback easy

---

## Skills vs Current Prompts

### Current Approach: Inline Prompts

**Advantages**:
- Simple: Everything in one prompt file
- Transparent: Easy to see all instructions
- Direct: No API calls needed

**Disadvantages**:
- Repetition: Same patterns copied across prompts
- Token cost: Full instructions loaded every time
- No versioning: Hard to track improvements
- No reuse: Can't share patterns across experiments

### Skills Approach

**Advantages**:
- **Reusability**: One skill used by multiple agents/experiments
- **Versioning**: Track improvements to techniques
- **Progressive loading**: Only load when relevant
- **Composition**: Combine multiple skills
- **Testing**: Validate skills in isolation

**Disadvantages**:
- **Complexity**: Requires skill creation/upload
- **API dependency**: Skills hosted on Anthropic side
- **Beta feature**: API may change
- **Learning curve**: Team needs to learn skill creation

---

## Recommendation: Hybrid Approach

### Phase 1: Current State (Working Well)

Keep current inline prompt approach for Experiment 03 completion:
- Prompts are working (40/40 tests passing)
- No need to change mid-experiment
- Finish validating the derivation paradigm

### Phase 2: Extract to Skills (Future Experiments)

After Experiment 03 completes, extract proven patterns to skills:

1. **Create `diagram-requirement-extraction` skill**
   - Base it on successful SPEC LIBRARIAN patterns
   - Test on 5 different capabilities
   - Version 1.0 when stable

2. **Create `tech-agnostic-requirement-filter` skill**
   - Extract from SPEC REVIEWER prompt
   - Add more pattern examples
   - Validate on legacy notes review

3. **Create `test-driven-development-workflow` skill**
   - Base on CODING AGENT prompt
   - Add progress tracking automation
   - Test on new capabilities

### Phase 3: Skill Library (Production)

Build organizational skill library:
```
anthropic-skills/
├── diagram-requirement-extraction/
├── tech-agnostic-requirement-filter/
├── test-driven-development-workflow/
├── deepwiki-navigation/
└── progress-monitoring/
```

---

## Specific Agents That Would Benefit

### 1. SPEC LIBRARIAN → `diagram-requirement-extraction` skill

**Current**: Prompt instructions explain diagram parsing
**With Skill**: Reusable diagram parsing expertise

**Use Case**:
```python
response = client.beta.messages.create(
    container={
        "skills": [
            {"type": "custom", "skill_id": "diagram-extraction", "version": "latest"}
        ]
    },
    messages=[{
        "role": "user",
        "content": f"Extract requirements from {deepwiki_doc} using diagram analysis"
    }]
)
```

**Benefits**:
- Consistent diagram parsing across all capabilities
- Validated examples prevent common mistakes
- Helper scripts speed up parsing
- Easy to improve technique and version

### 2. SPEC REVIEWER → `tech-agnostic-requirement-filter` skill

**Current**: Prompt explains what to filter to legacy_notes
**With Skill**: Precise filtering rules with pattern library

**Use Case**:
```python
response = client.beta.messages.create(
    container={
        "skills": [
            {"type": "custom", "skill_id": "tech-agnostic-filter", "version": "latest"}
        ]
    },
    messages=[{
        "role": "user",
        "content": f"Filter requirement cards in {requirement_cards} to remove vendor details"
    }]
)
```

**Benefits**:
- No vendor-specific details leak into requirements
- Comprehensive pattern library covers edge cases
- Quality checklist ensures completeness
- Can add new patterns as discovered

### 3. CODING AGENT → `test-driven-development-workflow` skill

**Current**: Prompt explains TDD workflow
**With Skill**: Enforced workflow with automation

**Use Case**:
```python
response = client.beta.messages.create(
    container={
        "skills": [
            {"type": "custom", "skill_id": "tdd-workflow", "version": "latest"}
        ]
    },
    messages=[{
        "role": "user",
        "content": f"Implement next failing test in {project_dir} using TDD workflow"
    }]
)
```

**Benefits**:
- Enforces one-test-at-a-time discipline
- Automated progress tracking
- Consistent git commit messages
- Early stopping logic built in

---

## Implementation Priority

### High Priority (After Experiment 03 Completes)

1. **`diagram-requirement-extraction`**
   - Most reusable across capabilities
   - Biggest consistency win
   - Foundation for all experiments

### Medium Priority

2. **`tech-agnostic-requirement-filter`**
   - Prevents vendor lock-in
   - Ensures portable requirements
   - Critical for tech-agnostic goal

### Lower Priority

3. **`test-driven-development-workflow`**
   - Current prompt already working well
   - Less variability between agents
   - Can wait until workflow needs refinement

---

## Validation Plan

Before committing to skills approach:

1. **Complete Experiment 03 with current prompts**
   - Validate derivation paradigm works
   - Document patterns that succeed
   - Identify pain points

2. **Extract patterns to skill prototypes**
   - Create local skill directories
   - Test with simple examples
   - Measure token usage vs inline prompts

3. **Run parallel experiment**
   - Same capability, two approaches:
     - Approach A: Inline prompts (control)
     - Approach B: Custom skills (test)
   - Compare: quality, speed, cost, consistency

4. **Decide based on data**
   - If skills improve outcomes → adopt
   - If no significant benefit → stay with prompts
   - If mixed results → hybrid approach

---

## Cost-Benefit Analysis

### Costs

| Factor | Impact |
|--------|--------|
| **Initial creation** | 2-4 hours per skill |
| **Testing** | 4-8 hours validation |
| **Migration** | Update all experiment prompts |
| **Learning curve** | Team training on skills API |
| **Maintenance** | Version management overhead |

### Benefits

| Factor | Impact |
|--------|--------|
| **Consistency** | All agents use same patterns |
| **Reusability** | One skill → many experiments |
| **Versioning** | Track improvements over time |
| **Composability** | Combine multiple skills |
| **Portability** | Share across projects |

### ROI Calculation

**Break-even point**: After 3-5 experiments using same patterns

**Example**:
- 3 agents × 5 experiments = 15 prompts
- Without skills: 15 × 300 lines = 4,500 lines of repeated instructions
- With skills: 3 skills × 300 lines = 900 lines + 15 × 50 lines (skill invocation) = 1,650 lines
- **Savings**: 2,850 lines of repeated content

---

## Conclusion

Custom skills would provide **significant value** for our experiment infrastructure, but **timing matters**:

✅ **DO NOW**: Complete Experiment 03 with current prompts (working well)

✅ **DO NEXT**: Extract successful patterns to skill prototypes

✅ **DO LATER**: Run validation experiment comparing approaches

✅ **DO EVENTUALLY**: Build organizational skill library if validated

### Key Insight

> **Skills are most valuable when you have proven patterns to codify.**
>
> We're still discovering what works in document-driven derivation.
> After we validate the approach, THEN extract patterns to skills.

---

## Related Documentation

- [Custom Skills Development](/.claude/claude-docs/skills-docs/03_skills_custom_development.ipynb)
- [Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Experiment 03 Strategy](./EXPERIMENT_03_STRATEGY.md)
- [Experiment 03 Manifesto](./EXP_03_MANIFESTO.md)
- [Directory Structure Rationale](./DIRECTORY_STRUCTURE_RATIONALE.md)

---

**Last Updated**: 2026-01-02
**Maintained By**: Experiment Infrastructure Team
