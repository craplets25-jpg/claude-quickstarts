# Large File Splitting Solution
**Date**: 2026-01-01
**Status**: ✅ Implemented and Tested
**Script**: `scripts/split_large_docs.py`

---

## Problem Statement

### Issue Identified
During the MVP run (Session 1), the agent encountered a critical problem:

```
[Tool: Read]
   Input: {'file_path': '../../../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md'}
   [Error] File content (51243 tokens) exceeds maximum allowed tokens (25000).
```

**Impact**:
- Agent forced to use Grep for searching (slower, less reliable)
- Agent had to use Read with offset/limit (fragmented understanding)
- Mermaid diagrams harder to find (split across searches)
- Overall slower session execution (~7 minutes vs potential ~3 minutes)

### Root Cause
The DeepWiki documentation file is **188KB** containing **~51,000 tokens**, which exceeds Claude's single read limit of 25,000 tokens.

---

## Solution Implemented

### Script: `split_large_docs.py`

**Purpose**: Automatically split large markdown files into logical sections based on header structure.

**Features**:
1. **Configurable split level**: H2 (##), H3 (###), or H4 (####)
2. **Preserves structure**: Each section includes full content under that header
3. **Metadata tracking**: Source file and line numbers preserved
4. **Index generation**: Creates INDEX.md with section previews and stats
5. **Token estimation**: Estimates token count per section (~4 chars per token)
6. **Slug generation**: Creates URL-safe filenames from headers
7. **Quality checks**: Warns if sections still exceed 25,000 tokens

---

## Results

### DeepWiki Split (H2 Level)

**Before**:
- 1 file: `debater-early-access-program-sdk-Deepwiki.md`
- Size: 188KB
- Tokens: ~51,000 (exceeds limit)
- Agent forced to use Grep/offset reads

**After**:
- 105 sections in `debater-early-access-program-sdk-Deepwiki-sections/`
- Average section: ~443 tokens
- Largest section: ~1,261 tokens
- All sections within 25,000 token limit ✅

### Section Breakdown

**Key Sections Created**:
```
001_purpose-and-scope.md                   ~173 tokens
002_overall-sdk-architecture.md            ~760 tokens
018_kpa-client-architecture.md             ~384 tokens
055_architecture-overview.md               ~596 tokens (Evidence Detection diagrams!)
056_client-classes.md                      ~429 tokens
065_sdk-architecture-overview.md           ~1,261 tokens (largest)
103_release-notes.md                       ~853 tokens
```

**Section #55 (Architecture Overview)** - Most important for Evidence Detection:
- Contains all 3 key Mermaid diagrams:
  - Client Class Hierarchy
  - Service Integration
  - Processing Pipeline
- Only 596 tokens - easily readable in one go
- Preserves line numbers: 2549-2609

---

## Usage

### Basic Usage
```bash
# Split by H2 headers (default)
python scripts/split_large_docs.py ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md

# Output: 105 sections in debater-early-access-program-sdk-Deepwiki-sections/
```

### Advanced Options
```bash
# Split by H3 for even smaller sections
python scripts/split_large_docs.py input.md --level 3

# Custom output directory
python scripts/split_large_docs.py input.md --output-dir my-sections/
```

### Workflow Integration
```bash
# 1. Split before starting experiment
python scripts/split_large_docs.py ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md

# 2. Agent reads INDEX.md to understand structure
cat debater-early-access-program-sdk-Deepwiki-sections/INDEX.md

# 3. Agent reads specific sections directly
cat debater-early-access-program-sdk-Deepwiki-sections/055_architecture-overview.md
```

---

## File Structure

### Output Directory Structure
```
debater-early-access-program-sdk-Deepwiki-sections/
├── INDEX.md                                    # Master index with previews
├── 001_purpose-and-scope.md
├── 002_overall-sdk-architecture.md
├── 003_key-components.md
├── ...
├── 055_architecture-overview.md               # Evidence Detection section!
├── ...
└── 105_version-management.md
```

### Section File Format
Each section file includes:

```markdown
<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Architecture Overview -->
<!-- Lines: 2549-2609 -->

## Architecture Overview

[Full section content with all subsections, diagrams, code, etc.]
```

### INDEX.md Format
```markdown
# Index: debater-early-access-program-sdk-Deepwiki.md

Split on: H2 headers
Total sections: 105

---

## 55. Architecture Overview

**File**: `055_architecture-overview.md`
**Lines**: 2549-2609 (61 lines)
**Est. Tokens**: ~596
**Preview**: The Claim and Evidence Detection system follows the standard client...

---

## Summary

- **Total sections**: 105
- **Total lines**: 3,856
- **Est. total tokens**: ~46,520
- **Avg tokens per section**: ~443
```

---

## Benefits

### For Agents
1. **No token limit errors**: All sections < 25,000 tokens
2. **Faster reads**: Read entire sections at once vs Grep searches
3. **Better context**: Complete sections vs fragmented offset reads
4. **Preserved structure**: Headers, diagrams, code all together
5. **Easy navigation**: INDEX.md provides map of all sections

### For Development
1. **Traceability**: Line numbers preserved in metadata
2. **Reproducibility**: Automated splitting vs manual
3. **Consistency**: Same split every time
4. **Reusability**: Works on any markdown file
5. **Maintainability**: Updates to source can be re-split

### Performance Comparison

**Session 1 (MVP run) - Without split sections**:
- Read attempts: Multiple Grep calls + offset reads
- Time: ~7 minutes
- Tool calls: 50+ (many for searching)

**Estimated with split sections**:
- Read attempts: INDEX.md + specific sections
- Time: ~3-4 minutes (estimated 40% faster)
- Tool calls: ~30 (direct reads, no searching)

---

## Implementation Details

### Algorithm
1. Parse markdown file line by line
2. Detect headers using regex: `^(#{1,6})\s+(.+)$`
3. When split-level header found, start new section
4. Accumulate lines until next split-level header
5. Generate slug from header text
6. Write section with metadata
7. Create INDEX.md with summaries

### Token Estimation
- Uses 4 characters per token heuristic
- Counts all characters in section content
- Provides rough estimate for planning

### Slug Generation
- Remove markdown formatting: `# * ` [ ] ( )`
- Convert to lowercase
- Replace non-alphanumeric with hyphens
- Limit to 80 characters
- Example: "## Architecture Overview" → "architecture-overview"

---

## Testing

### Test Run: DeepWiki Split
```bash
$ python scripts/split_large_docs.py ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md

Reading: ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md
Split level: H2
Output directory: ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki-sections

Parsing document...
Found 105 sections

Writing section files...
[... 105 sections created ...]

======================================================================
SUMMARY
======================================================================
Sections created: 105
Total est. tokens: ~46,520
Average per section: ~443 tokens
Largest section: ~1,261 tokens
Output directory: ../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki-sections

✅ All sections are within the 25,000 token limit
```

**Result**: ✅ Success - All sections readable by agents

---

## Future Enhancements

### Potential Improvements
1. **Auto-detect optimal split level**: Analyze file and suggest H2/H3/H4
2. **Section merging**: Combine very small sections (< 100 tokens)
3. **Cross-references**: Track links between sections
4. **Search index**: Create searchable index of keywords per section
5. **Agent prompt updates**: Automatically reference split sections
6. **Multi-file splitting**: Batch process multiple files
7. **Progress bar**: Show progress during splitting
8. **Validation**: Check all Mermaid diagrams are complete

### Integration Ideas
1. **Pre-experiment hook**: Automatically split large docs before starting
2. **Prompt enhancement**: Teach agents to use INDEX.md effectively
3. **Section caching**: Cache frequently accessed sections
4. **Smart search**: Agent searches INDEX.md then reads relevant sections

---

## Recommendations

### For Next Experiment Run
1. ✅ Use split sections for faster agent reads
2. Update Spec Librarian prompt to reference sections directory
3. Add instruction to read INDEX.md first
4. Track time savings vs MVP run

### Best Practices
1. **Always split large docs** (> 50KB or > 15,000 tokens)
2. **Use H2 split by default** - good balance of granularity
3. **Use H3 if H2 sections still large** (> 5,000 tokens each)
4. **Keep INDEX.md** - agents use it for navigation
5. **Version control splits** - commit sections to git

---

## Files Modified/Created

### Created
- ✅ `scripts/split_large_docs.py` (300 lines)
- ✅ `../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki-sections/` (105 sections + INDEX.md)
- ✅ `scripts/README.md` (updated with split_large_docs.py documentation)

### Modified
- ✅ `scripts/README.md` (added comprehensive documentation)

---

## Conclusion

The large file splitting solution successfully addresses the token limit problem identified in the MVP run. By splitting the 188KB DeepWiki file into 105 manageable sections, agents can now:

- ✅ Read entire sections without token limits
- ✅ Find information faster (INDEX.md navigation)
- ✅ Preserve complete context (full sections vs fragments)
- ✅ Maintain traceability (line numbers preserved)

**Expected Impact**: 40% faster Spec Librarian sessions, fewer tool calls, better context understanding.

**Status**: Ready for integration into next experiment run.

---

## Example: Section 55 (Evidence Detection)

This section was critical for the MVP run and is now easily accessible:

**Before** (MVP run):
```
[Tool: Grep] pattern='Evidence Detection' → Find line numbers
[Tool: Read] offset=2530, limit=300 → Read partial section
[Tool: Grep] pattern='mermaid' → Find diagrams
[Tool: Read] offset=2555, limit=100 → Read diagram 1
[Tool: Read] offset=2576, limit=100 → Read diagram 2
```
**5 tool calls, fragmented understanding**

**After** (with split sections):
```
[Tool: Read] file='055_architecture-overview.md'
```
**1 tool call, complete section with all 3 diagrams**

---

**Total Development Time**: ~30 minutes
**Test Time**: ~2 minutes
**Documentation Time**: ~20 minutes
**Total**: ~52 minutes

**Return on Investment**: Saves ~3-4 minutes per experiment run, better agent understanding, fewer errors
