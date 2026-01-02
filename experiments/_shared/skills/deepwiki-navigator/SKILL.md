---
name: deepwiki-navigator
description: Navigate and extract sections from DeepWiki technical documentation efficiently without loading full document into context. Find capabilities, extract specific sections, and analyze document structure.
---

# DeepWiki Navigator

Efficiently navigate large technical documentation (10,000+ lines) without context overhead.

## Purpose

The DeepWiki Navigator skill provides tools to:
1. **Scan for capabilities** - Find all NLP capabilities in document
2. **Extract sections** - Get specific content by name or line range
3. **Analyze structure** - Understand document organization
4. **Parse diagrams** - Extract and analyze Mermaid diagrams

**Key Benefit**: Scripts execute OUTSIDE context window, so you can process 10,000+ line documents using only ~500 tokens instead of 15,000+.

## When to Use This Skill

Use this skill when working with DeepWiki or similar large technical documentation:

✅ **DO use when**:
- Starting new capability implementation (scan for capabilities)
- Need specific section content (extract by name)
- Looking for diagram/example-rich sections
- Want document statistics without reading everything
- Need to cite line numbers for traceability

❌ **DON'T use when**:
- You already know exact line numbers and section is small (<100 lines)
- You need to read entire document for context
- Working with non-DeepWiki documents (may not work)

## Available Tools

### 1. Capability Scanner

**Purpose**: Find all capabilities in DeepWiki without reading full document

**Command**:
```python
# Run the capability_scanner.py script
# Input: Path to DeepWiki markdown file
# Output: JSON with capability summaries
```

**What You Get Back**:
```json
{
  "capabilities": [
    {
      "name": "Primary Feature: Key Point Analysis",
      "line_start": 119,
      "line_end": 164,
      "section_size_lines": 45,
      "has_diagrams": true,
      "diagram_count": 1,
      "diagram_types": ["flowchart"],
      "has_code_examples": true,
      "code_example_count": 1,
      "keywords": ["analysis", "keypoint", "feature"]
    }
  ],
  "total_capabilities": 13,
  "document_stats": {
    "total_lines": 5031,
    "total_diagrams": 71,
    "total_code_blocks": 119
  }
}
```

**How to Use**:
1. Request capability scan
2. Review summary (NOT full content)
3. Select capability to implement
4. Use section extractor to get full content

### 2. Section Extractor

**Purpose**: Extract specific section content with metadata

**Commands**:

**By Name** (recommended):
```python
# Extract by section name (fuzzy matching)
# Input: DeepWiki path, section name
# Output: Section content + metadata
```

**By Line Range**:
```python
# Extract by exact line numbers
# Input: DeepWiki path, line_start, line_end
# Output: Section content + metadata
```

**List Matching Sections**:
```python
# Find all sections matching keyword
# Input: DeepWiki path, keyword
# Output: List of matching section summaries
```

**What You Get Back**:
```json
{
  "section_title": "Primary Feature: Key Point Analysis",
  "line_start": 119,
  "line_end": 164,
  "content": "... full section content ...",
  "has_diagrams": true,
  "diagrams": [
    {
      "line_start": 5,
      "line_end": 41,
      "content": "... Mermaid diagram content ...",
      "type": "flowchart"
    }
  ],
  "has_code_blocks": true,
  "code_blocks": [...],
  "metadata": {
    "diagram_count": 1,
    "code_block_count": 3,
    "diagram_types": ["flowchart"],
    "code_languages": ["python", "json"]
  }
}
```

## Workflow: From Capability Scan to Implementation

### Step 1: Scan for Capabilities

**Instruction to Agent**: "Use deepwiki-navigator skill to scan DeepWiki for all available capabilities."

**Script Executes**: `capability_scanner.py <deepwiki_path>`

**You Receive**: JSON summary of ~10-15 capabilities with metadata (uses ~500 tokens, not 15,000!)

### Step 2: Select Capability

**Review** the capability summary:
- Check `section_size_lines` (prefer 50-200 lines for MVP)
- Check `diagram_count` (diagrams = better requirements)
- Check `code_example_count` (examples = easier triangulation)
- Review `keywords` to understand topic

**Decision**: Choose capability that matches experiment phase constraints

### Step 3: Extract Section

**Instruction to Agent**: "Use deepwiki-navigator skill to extract section for [capability name]."

**Script Executes**: `section_extractor.py --section "[name]"`

**You Receive**: Full section content with:
- Complete text
- Parsed diagrams (ready for requirement extraction)
- Code examples (ready for triangulation)
- Line numbers (for citations)

### Step 4: Proceed to Requirement Derivation

Now that you have ONLY the relevant section loaded:
- Parse diagrams → derive requirements
- Analyze code examples → triangulate patterns
- Extract API signatures → create requirement cards
- Cite line numbers → maintain traceability

## Example Usage

### Example 1: Starting New Capability

```markdown
**User Request**: "I want to implement Evidence Detection capability"

**Agent**: "I'll use deepwiki-navigator to find this capability"

**Agent Uses Skill**:
1. Scan DeepWiki for capabilities
2. Find "Evidence Detection" in results (lines 1234-2456, 71 diagrams)
3. Extract that section
4. Receive 1,222 lines of relevant content

**Context Used**:
- Scan: 500 tokens (capability summaries)
- Extract: 2,000 tokens (just Evidence Detection section)
- **Total**: 2,500 tokens vs 15,000 for full document!
- **Savings**: 83%
```

### Example 2: Finding Section by Keyword

```markdown
**Agent**: "Need to find all sections related to 'authentication'"

**Agent Uses Skill**:
python section_extractor.py --list "authentication"

**Agent Receives**:
{
  "keyword": "authentication",
  "matches": [
    {"title": "Authentication Setup", "line_start": 323, "size_lines": 52},
    {"title": "API Authentication", "line_start": 456, "size_lines": 38}
  ]
}

**Agent**: "I'll extract the Authentication Setup section"
```

### Example 3: Extracting Just Metadata

```markdown
**Agent**: "I want to know which sections have the most diagrams"

**Agent Uses Skill**:
Scan capabilities → sort by diagram_count → extract top 3

**Result**:
1. "Key Point Analysis" - 5 diagrams
2. "Evidence Detection" - 7 diagrams
3. "Argument Quality" - 4 diagrams

**Agent**: "Evidence Detection has the most diagrams, good for requirements"
```

## Tips for Maximum Efficiency

### DO:
✅ Always scan first before extracting
✅ Use metadata to guide decisions (diagram/code counts)
✅ Extract only what you need (one section at a time)
✅ Cite line numbers from extraction results
✅ Use fuzzy matching for section names (handles variations)

### DON'T:
❌ Extract multiple large sections at once
❌ Re-extract sections you've already seen
❌ Skip capability scan (wastes time searching manually)
❌ Ignore metadata (it guides optimal section selection)

## Integration with Experiment Pipeline

### SPEC LIBRARIAN Phase

**Use deepwiki-navigator to**:
1. Scan DeepWiki → Get all capabilities
2. Filter by phase constraints (size, diagram count)
3. Extract selected capability section
4. Parse diagrams → derive requirements
5. Extract code examples → triangulate

**Context Savings**: 80-90% vs reading full document

### SPEC REVIEWER Phase

**Use deepwiki-navigator to**:
1. Extract specific sections for verification
2. Get line numbers for requirement citations
3. Find examples for validation

**Context Savings**: 60-70% vs re-reading document

### CODING AGENT Phase

**Use deepwiki-navigator to**:
1. Quick reference lookup (extract by name)
2. Find API signatures
3. Check diagram details

**Context Savings**: 50-60% vs searching manually

## Script Reference

### capability_scanner.py

**Input**: Path to DeepWiki markdown file

**Output**: JSON with:
- `capabilities[]` - Array of capability objects
- `total_capabilities` - Count
- `document_stats` - Document metadata

**Command Line**:
```bash
python capability_scanner.py <deepwiki_path>
```

### section_extractor.py

**Input**: DeepWiki path + section identifier

**Output**: JSON with section content and metadata

**Command Line Options**:
```bash
# By section name
python section_extractor.py <deepwiki_path> --section "Key Point Analysis"

# By line range
python section_extractor.py <deepwiki_path> --lines 119-164

# List matching sections
python section_extractor.py <deepwiki_path> --list "analysis"

# Metadata only (no content)
python section_extractor.py <deepwiki_path> --section "..." --no-content
```

## Error Handling

### Common Issues

**"File not found"**:
- Check path to DeepWiki
- Use absolute or correct relative path

**"Section not found"**:
- Try fuzzy matching (automatic)
- List sections with --list to find exact name
- Check capitalization/spelling

**"No capabilities found"**:
- Document may not match expected structure
- Check document_stats to verify it's DeepWiki
- May need to adjust scanner keywords

## Performance Characteristics

| Operation | Time | Context Tokens |
|-----------|------|----------------|
| Capability Scan | ~2 seconds | ~500 |
| Section Extract | ~1 second | ~2,000 |
| List Sections | ~1 second | ~300 |
| Full Document Read | N/A | ~15,000 |

**Typical Workflow**:
1. Scan (2s, 500 tokens)
2. Extract (1s, 2,000 tokens)
**Total**: 3 seconds, 2,500 tokens

**Without Skill**:
1. Read full doc (N/A, 15,000 tokens)
2. Search manually (30-60s)
**Total**: 30+ seconds, 15,000 tokens

**Improvement**: 10x faster, 83% less context

## Related Skills

- **diagram-requirement-extractor**: Parse Mermaid diagrams → requirements
- **example-triangulator**: Analyze multiple examples for patterns
- **vendor-pattern-detector**: Filter tech-specific details

## Troubleshooting

**Q: Why didn't scanner find my capability?**
A: Scanner uses keywords. Try `--list <keyword>` to find section name, then extract manually.

**Q: Extracted section is too large**
A: Use `--no-content` first to check size, or extract subsections individually.

**Q: Need more context around section**
A: Adjust line range: if section is 119-164, try 100-180 for more context.

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-02
**Maintained By**: Experiment Infrastructure Team
