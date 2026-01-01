# Prompt Updates for Split Sections
**Date**: 2026-01-01
**Status**: ✅ Complete
**Files Modified**: `prompts/spec_librarian_prompt.md`

---

## Changes Made

### 1. Added "Understanding the canonical artifacts structure" section

**Location**: After "STEP 1 — Establish the universe of truth" header

**What it does**:
- Explicitly tells agents about the split sections directory
- Provides exact paths to all canonical artifacts
- Explains the INDEX.md workflow
- Lists the file structure organization

**New content**:
```markdown
### Understanding the canonical artifacts structure

The canonical artifacts are organized as follows:

**DeepWiki Documentation (SPLIT INTO SECTIONS)**:
- Location: `../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki-sections/`
- **Start here**: Read `INDEX.md` to see all 105 sections with previews
- Each section is a separate file: `001_purpose-and-scope.md`, `055_architecture-overview.md`, etc.
- Section files include metadata comments with source line numbers

**Table of Contents**:
- Location: `../deep-wiki-spec-files/TOC-debater-early-access-program-sdk-H2-H4.md`
- Lists all major sections and subsections

**Reference Implementation**:
- Location: `../reference-files/debater_python_api/`
- Contains: `api/clients/`, `examples/`, and response files
```

### 2. Updated "1A: Find the diagrams first" workflow

**Old approach** (agent had to discover):
- "Search the DeepWiki for Mermaid blocks"
- Agent would use Grep, hit token limits, use offset reads

**New approach** (explicit guidance):
```markdown
**IMPORTANT: DeepWiki has been split into 105 sections for easier reading.**

**Efficient workflow**:
1. Read `../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki-sections/INDEX.md`
2. Identify sections relevant to your capability (grep for keywords)
3. Read complete sections (no token limits!)
4. Extract Mermaid diagrams from relevant sections

**For Evidence Detection**, key sections include:
- Section #55: `055_architecture-overview.md` — Contains all 3 key diagrams:
  - Client Class Hierarchy
  - Service Integration
  - Processing Pipeline
- Section #56: `056_client-classes.md` — Client details
- Section #57: `057_input-and-output-formats.md` — Data formats
```

**Benefits**:
- Agent knows exactly where to find Evidence Detection diagrams
- No searching or grepping needed
- All 3 diagrams in one readable section
- Faster execution

### 3. Updated "1B: Then read supporting text" with explicit paths

**Old**:
```markdown
1) Open the DeepWiki TOC
2) Inspect the debater reference tree (clients + examples + responses)
```

**New**:
```markdown
1) Read the TOC: `../deep-wiki-spec-files/TOC-debater-early-access-program-sdk-H2-H4.md`
2) Inspect the debater reference tree: `../reference-files/debater_python_api/`
   - Check `examples/` for example scripts
   - Check `api/clients/` for client implementations
```

**Benefits**:
- No path discovery needed
- Direct access to files
- Clear structure

### 4. Updated STEP 2 PROOF format to reference sections

**Old format**:
```
- [B] DeepWiki section: ___ (lines ___)
- [C] DIAGRAM: ___ (lines ___) — what it shows
```

**New format**:
```
- [B] DeepWiki section: section #___ `filename.md` (source lines ___ in original)
- [C] DIAGRAMS: section #___ `filename.md` — what they show
  - Diagram 1: ___ (shows ___)
  - Diagram 2: ___ (shows ___)
  - Diagram 3: ___ (shows ___)
```

**Added note**:
```markdown
**Note**: Section files include metadata comments showing original line numbers
from the unsplit file. Use these for traceability.
```

**Benefits**:
- Clear section references
- Multiple diagrams per section supported
- Traceability preserved via metadata

### 5. Updated STEP 3 card format with section references

**Old sources format**:
```json
"sources": {
  "diagram": "Processing Pipeline (lines 2686-2711) — shows...",
  "deepwiki": "section name (lines X-Y)",
  "example": "filename:lines",
  ...
}
```

**New sources format**:
```json
"sources": {
  "diagram": "Section #58: `058_processing-pipeline.md` — shows Input→Validation→Transform→Batch→Results",
  "deepwiki": "Section #55: `055_architecture-overview.md` (original lines 2549-2609)",
  "example": "../reference-files/debater_python_api/examples/evidence_detection_example.py:16",
  "response": "../reference-files/debater_python_api/examples/evidence_detection_response.txt:1-16",
  "client": "../reference-files/debater_python_api/api/clients/claim_and_evidence_detection_client.py:run (lines 32-36)"
}
```

**Benefits**:
- Section number + filename for easy lookup
- Original line numbers preserved for traceability
- Full paths for reference files
- Consistent format

---

## Impact on Agent Behavior

### Before (MVP Run - Session 1)
```
[Tool: Read]
   Input: {'file_path': '../../../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md'}
   [Error] File content (51243 tokens) exceeds maximum allowed tokens (25000)

[Tool: Grep] Pattern: 'mermaid' → Find 71 diagrams

[Tool: Read] offset=2530, limit=300 → Fragment 1
[Tool: Read] offset=2555, limit=100 → Fragment 2
[Tool: Read] offset=2576, limit=100 → Fragment 3

Tool calls: 50+
Time: ~7 minutes
```

### After (Expected - Next Run)
```
[Tool: Read]
   Input: {'file_path': '../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki-sections/INDEX.md'}
   [Done] 105 sections listed

[Tool: Read]
   Input: {'file_path': '../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki-sections/055_architecture-overview.md'}
   [Done] Complete section with all 3 diagrams

Tool calls: ~30 (estimated)
Time: ~3-4 minutes (estimated 40% faster)
```

---

## Validation Checklist

Before next run, verify:
- [x] Split sections exist at correct path
- [x] INDEX.md is complete and readable
- [x] Section #55 contains all Evidence Detection diagrams
- [x] Metadata comments in section files have line numbers
- [x] Prompt references correct paths
- [x] Prompt explains workflow clearly
- [ ] Test with actual agent run (pending)

---

## Key Sections for Evidence Detection

Based on the split, these sections are most relevant for Evidence Detection:

| Section | File | Content | Tokens |
|---------|------|---------|--------|
| #2 | `002_overall-sdk-architecture.md` | SDK architecture overview | ~760 |
| #55 | `055_architecture-overview.md` | **3 key diagrams** | ~596 |
| #56 | `056_client-classes.md` | Client class details | ~429 |
| #57 | `057_input-and-output-formats.md` | Data formats | ~241 |
| #58 | `058_processing-pipeline.md` | Processing flow | ~257 |

**Total tokens if agent reads all 5 sections**: ~2,283 tokens
**vs Original file**: 51,000 tokens (96% reduction in reading load)

---

## Expected Performance Improvement

### Tool Call Reduction
- **Before**: 50+ tool calls (Grep searches, offset reads, path discovery)
- **After**: ~30 tool calls (direct reads, no searching)
- **Improvement**: ~40% fewer tool calls

### Time Savings
- **Before**: ~7 minutes (Session 1 MVP run)
- **After**: ~3-4 minutes (estimated)
- **Improvement**: ~40% faster

### Context Quality
- **Before**: Fragmented understanding (offset reads, partial diagrams)
- **After**: Complete sections (full context, all diagrams together)
- **Improvement**: Better comprehension, fewer errors

### Token Efficiency
- **Before**: Agent had to read 51,000 tokens in fragments
- **After**: Agent reads ~2,300 tokens across 5 sections
- **Improvement**: 96% reduction in token reading

---

## Next Steps

### Immediate
1. [x] Update spec_librarian_prompt.md ✅
2. [ ] Test with new experiment run
3. [ ] Measure actual time savings
4. [ ] Compare tool call counts

### If Successful
1. Document best practices for future experiments
2. Consider splitting other large files (if any)
3. Update other prompts if they reference large files
4. Add split_large_docs.py to standard workflow

### If Issues Found
1. Agent doesn't use INDEX.md → Add more explicit instruction
2. Agent still searches → Strengthen "read sections directly" language
3. Section references confusing → Simplify format
4. Performance not improved → Investigate bottlenecks

---

## Backwards Compatibility

**Does this break existing runs?**
No - this only affects new runs. Existing completed runs (like MVP run) already have their outputs and won't be affected.

**Can we still reference original line numbers?**
Yes - section metadata preserves original line numbers:
```markdown
<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Architecture Overview -->
<!-- Lines: 2549-2609 -->
```

**What if agent ignores new instructions?**
Agent can still discover files the old way - new instructions just make it faster. If agent uses Grep/Read offset, it will still work (just slower).

---

## Files Modified

1. **`prompts/spec_librarian_prompt.md`**
   - Added: "Understanding the canonical artifacts structure" section
   - Updated: "1A: Find the diagrams first" workflow
   - Updated: "1B: Then read supporting text" with explicit paths
   - Updated: STEP 2 PROOF format
   - Updated: STEP 3 card sources format

---

## Summary

✅ **Prompt successfully updated to use split sections**

**Key improvements**:
1. Explicit paths to all canonical artifacts
2. Clear INDEX.md workflow
3. Section-based references (no token limits)
4. Preserved traceability via metadata
5. Evidence Detection sections identified upfront

**Expected benefits**:
- 40% faster sessions
- 40% fewer tool calls
- Better context understanding
- No token limit errors

**Status**: Ready for testing in next experiment run
