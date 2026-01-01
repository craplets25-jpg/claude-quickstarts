# Prompt Fixes Applied - 2026-01-01

## Summary

Applied comprehensive fixes to address issues identified in test-run-03 and EXPERIMENT_02_STRATEGY.md.

---

## 1. Critical Fix: Update ALL Passing Tests

**File**: `prompts/coding_prompt.md`
**Section**: Step 6

**Problem**: Agent only marked 1 test as passing despite 12 tests actually passing.

**Fix Applied**:
```markdown
### Step 6 — Update ALL Passing Tests in feature_list.json

**CRITICAL: You MUST update ALL passing tests, not just the target test.**

1. **Identify all tests with "passes": true in test results**
2. **Update feature_list.json for EVERY passing test:**
   - Change "passes": false → "passes": true
   - This is REQUIRED, not optional
3. **Count and verify:**
   - Count how many tests you updated
   - Verify count matches your test results from Step 5

**Verification Checklist:**
- [ ] Ran full test suite (not just target test)
- [ ] Identified ALL passing tests
- [ ] Updated ALL passing tests in feature_list.json
- [ ] Verified count: X tests updated
```

**Expected Impact**: No more duplicate work implementing already-passing tests.

---

## 2. Critical Fix: Continue to Next Test

**File**: `prompts/coding_prompt.md`
**Section**: New Step 8

**Problem**: Agent stopped after implementing ONE test, even when more work could be done.

**Fix Applied**:
```markdown
### Step 8 — Check If More Work Remains

**IMPORTANT: Do not stop after just one test.**

1. **Count remaining tests** with "passes": false
2. **Evaluate if you should continue:**

**CONTINUE to next test if ALL of these are true:**
- [ ] At least one test still has "passes": false
- [ ] Session has been running < 25 minutes
- [ ] Next test is structural/behavioral (not semantic)
- [ ] Next test doesn't require major refactoring
- [ ] No blocking errors encountered

**If you CONTINUE:**
- Return to Step 2
- Select the NEXT failing test
- Repeat the implementation loop
```

**Expected Impact**: 3-5 tests implemented per coding session instead of just 1.

---

## 3. Fix: Add Progress Tracking

**File**: `prompts/coding_prompt.md`
**Section**: Step 5 and Step 7

**Problem**: No visibility into how many tests pass after each implementation.

**Fix Applied**:

**Step 5 - Track progress during verification:**
```markdown
1. **Run the ENTIRE test suite** (not just the target test)
2. **Count ALL passing tests**
3. **Log progress metrics:**
   - Tests passing: X/Y (Z%)
   - Tests implemented this session: N
   - Estimated time elapsed: ~M minutes
```

**Step 7 - Structured summary:**
```markdown
**STRUCTURED SUMMARY (at top):**
PROGRESS SUMMARY
================
Session: [N]
Agent: Coding Agent
Date: [YYYY-MM-DD]

Metrics:
- Tests passing: X/Y (Z%)
- Tests implemented this session: N
- Tests passing due to side effects: M
- Time: ~T minutes
- Status: [In progress / Complete]
```

**Expected Impact**: Better visibility into progress, easier to track velocity.

---

## 4. Fix: Test Selection Strategy

**File**: `prompts/coding_prompt.md`
**Section**: Step 2

**Problem**: Agent might implement semantic tests early, which require complex scoring logic.

**Fix Applied**:
```markdown
**Test Selection Strategy:**

Prefer tests in this order:
1. **Structural tests** (input/output shape, validation, API boundaries)
2. **Behavioral tests** (order preservation, batching, error handling)
3. **Integration tests** (multiple components working together)
4. **Semantic tests** (require ML models or complex scoring logic) ← DEFER TO END

If you encounter a semantic test early (e.g., TEST-015 "High scores indicate strong evidence"):
- Document: "This test requires semantic scoring logic - deferring to end"
- Skip to next structural/behavioral test
- Return to semantic tests after all other tests pass
```

**Expected Impact**: Agent implements easier tests first, saves semantic tests for end when architecture is stable.

---

## 5. Fix: Standardize JSON Output Format

**File**: `prompts/spec_librarian_prompt.md`
**Sections**: Step 3 and Step 4

**Problem**: feature_list.json was sometimes wrapped in object, sometimes bare array.

**Fix Applied**:

**For requirement_cards.json:**
```markdown
The output MUST be a JSON array at the root level:
[
  {
    "id": "ED-001",
    "title": "...",
    ...
  }
]

Do NOT wrap in an object like {"cards": [...]}.
```

**For feature_list.json:**
```markdown
The output MUST be a JSON array at the root level:
[
  {
    "id": "TEST-001",
    "requirement_id": "ED-001",
    "description": "...",
    "passes": false,
    ...
  }
]

Do NOT wrap in an object like {"tests": [...]} or {"capability": "...", "tests": [...]}.
```

**Expected Impact**: Consistent JSON format, no more AttributeError on parsing.

---

## 6. Fix: Path Discovery Issue

**Files**:
- `prompts/spec_librarian_prompt.md`
- `prompts/spec_reviewer_prompt.md`
- `prompts/coding_prompt.md`

**Problem**: Agents search parent directories repeatedly instead of using local files.

**Fix Applied**:

Added to ALL three prompts:
```markdown
**IMPORTANT: All required files are in your current working directory.**
Do not search parent directories. Look locally first.
```

**Expected Impact**: Agents look in current directory first, reducing file search overhead.

---

## Summary of Expected Improvements

| Metric | Before | After (Expected) |
|--------|--------|------------------|
| Tests per coding session | 1 | 3-5 |
| Tests marked as passing | 1 (actual: 12) | 12 (all) |
| JSON format variance | Yes | No (standardized) |
| Path searches | Multiple parent dirs | Local first |
| Progress visibility | Limited | Comprehensive |
| Test selection | Sequential | Smart (defer semantic) |

---

## Testing Plan

### Phase 1: Small Verification Run (2 iterations)

```bash
python autonomous_agent_demo.py \
  --project-dir ./generations/test-fix-verify \
  --max-iterations 2
```

**Success Criteria**:
- [ ] Session 1 (Spec Librarian): Creates bare array JSON files
- [ ] Session 2 (Spec Reviewer): Reads local files without searching parent dirs
- [ ] Session 3 (Coding Agent): Updates ALL passing tests in feature_list.json
- [ ] Session 3 (Coding Agent): Continues to next test before stopping

### Phase 2: Full MVP Run (20 iterations, 5 capabilities)

Only proceed if Phase 1 succeeds.

```bash
python autonomous_agent_demo.py \
  --project-dir ./generations/mvp-01 \
  --max-iterations 20
```

**Expected Timeline**:
- Iteration 1: Spec Librarian (50-80 cards, 50-80 tests)
- Iteration 2: Spec Reviewer (filter tech details)
- Iterations 3-20: Coding Agent (15-25 tests per iteration)

**Success Criteria**:
- [ ] All 5 capabilities implemented (Evidence, Claim, ArgQuality, ProCon, Boundaries)
- [ ] 80%+ tests passing
- [ ] No invented features
- [ ] Clean, maintainable code

---

## Rollback Plan

If fixes cause issues:

1. Revert prompts:
   ```bash
   git checkout HEAD -- prompts/
   ```

2. Restore from backup (if needed)

3. Analyze logs to identify which fix caused the issue

4. Apply fixes incrementally

---

## Monitoring Commands

**Full view with decisions**:
```bash
python monitor.py generations/mvp-01
```

**Focus on decisions only**:
```bash
python monitor.py generations/mvp-01 --mode decisions
```

**Live activity log**:
```bash
python monitor.py generations/mvp-01 --mode live
```

**Or tail the log directly**:
```bash
tail -f generations/mvp-01/logs/live.log
```

---

## Notes

- All fixes address real issues observed in test-run-03
- Fixes are conservative and well-documented
- Each fix has clear success criteria
- Logging system will make debugging much easier
- Ready for verification run
