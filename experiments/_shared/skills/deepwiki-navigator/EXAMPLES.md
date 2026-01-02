# DeepWiki Navigator - Usage Examples

Complete examples of using the deepwiki-navigator skill in real workflows.

---

## Example 1: Finding and Implementing a New Capability

**Scenario**: User wants to implement next capability after Key Point Analysis

### Without Skill (Traditional Approach)

```markdown
**Agent**: "Let me read the DeepWiki to find next capability"

**Action**: Read entire DeepWiki (5,031 lines)
**Context Used**: ~15,000 tokens
**Time**: 2-3 minutes to scan mentally

**Agent**: *Scrolls through 5000 lines looking for capabilities*
**Agent**: "I found Evidence Detection at line 1234"
**Agent**: *Reads Evidence Detection section*
**Agent**: "Now I'll derive requirements..."

**Total Time**: 5-7 minutes
**Total Context**: 15,000 tokens
```

### With Skill (Optimized Approach)

```markdown
**Agent**: "I'll use deepwiki-navigator skill to scan for capabilities"

**Script Executes**: capability_scanner.py
**Time**: 2 seconds
**Context Used**: ~500 tokens (just the JSON summary)

**Agent Receives**:
{
  "capabilities": [
    {
      "name": "Primary Feature: Key Point Analysis",
      "line_start": 119,
      "line_end": 164,
      "section_size_lines": 45,
      "diagram_count": 1,
      "keywords": ["analysis", "keypoint"]
    },
    {
      "name": "Evidence Detection Service",
      "line_start": 1234,
      "line_end": 2456,
      "section_size_lines": 1222,
      "diagram_count": 7,
      "keywords": ["evidence", "detection"]
    },
    ...
  ],
  "total_capabilities": 13
}

**Agent**: "I see 13 capabilities. Evidence Detection looks good (1222 lines, 7 diagrams)"
**Agent**: "I'll extract that section"

**Script Executes**: section_extractor.py --section "Evidence Detection"
**Time**: 1 second
**Context Used**: ~2,000 tokens (just Evidence Detection section)

**Agent**: "Now I have the section with 7 diagrams parsed. I'll derive requirements..."

**Total Time**: ~30 seconds
**Total Context**: ~2,500 tokens
**Savings**: 83% context, 10x faster
```

---

## Example 2: Verifying a Requirement Citation

**Scenario**: SPEC REVIEWER needs to verify requirement came from correct source

### Without Skill

```markdown
**Reviewer**: "Let me verify this requirement cites correct line numbers"
**Reviewer**: *Reads entire DeepWiki*
**Reviewer**: *Searches for relevant section*
**Reviewer**: *Manually counts lines*
**Reviewer**: "Yes, it's from lines 2345-2367"

**Time**: 3-5 minutes
**Context**: 15,000 tokens
```

### With Skill

```markdown
**Reviewer**: "I'll extract that section to verify"

**Script Executes**: section_extractor.py --lines 2345-2367 --no-content
**Time**: 1 second
**Context**: ~300 tokens (metadata only)

**Agent Receives**:
{
  "line_start": 2345,
  "line_end": 2367,
  "section_title": "Input Validation Rules",
  "has_diagrams": true,
  "diagram_count": 1,
  "content_length": 875
}

**Reviewer**: "Confirmed - requirement correctly cites Input Validation Rules section"

**Time**: 5 seconds
**Context**: 300 tokens
**Savings**: 98% context, 36x faster
```

---

## Example 3: Finding All Sections About a Topic

**Scenario**: Agent needs to find all authentication-related sections

### Without Skill

```markdown
**Agent**: *Reads full DeepWiki*
**Agent**: *Manually searches for "auth"*
**Agent**: *Finds 3 sections scattered across document*
**Agent**: *Reads each section*

**Time**: 5-10 minutes
**Context**: 15,000+ tokens
```

### With Skill

```markdown
**Agent**: "I'll list all sections matching 'authentication'"

**Script Executes**: section_extractor.py --list "authentication"
**Time**: 1 second
**Context**: ~300 tokens

**Agent Receives**:
{
  "keyword": "authentication",
  "matches": [
    {
      "title": "API Authentication Setup",
      "line_start": 323,
      "line_end": 375,
      "size_lines": 52
    },
    {
      "title": "OAuth 2.0 Authentication",
      "line_start": 456,
      "line_end": 494,
      "size_lines": 38
    },
    {
      "title": "Authentication Troubleshooting",
      "line_start": 2890,
      "line_end": 2920,
      "size_lines": 30
    }
  ]
}

**Agent**: "Found 3 auth sections. I'll extract API Authentication Setup"

**Script Executes**: section_extractor.py --section "API Authentication"
**Time**: 1 second
**Context**: ~1,000 tokens

**Agent**: "Got the setup section, now I can proceed"

**Total Time**: 2-3 seconds
**Total Context**: 1,300 tokens
**Savings**: 91% context, 150x faster
```

---

## Example 4: Selecting Best Capability for MVP

**Scenario**: SPEC LIBRARIAN needs to find simplest capability for quick win

### Without Skill

```markdown
**Agent**: *Reads full DeepWiki*
**Agent**: *Mentally compares section sizes*
**Agent**: *Looks for diagrams and examples*
**Agent**: *Makes guess*

**Time**: 10-15 minutes
**Context**: 15,000 tokens
**Quality**: Uncertain (may miss better option)
```

### With Skill

```markdown
**Agent**: "I'll scan capabilities and analyze them"

**Script Executes**: capability_scanner.py
**Time**: 2 seconds
**Context**: 500 tokens

**Agent Receives**:
{
  "capabilities": [
    {
      "name": "Evidence Detection",
      "section_size_lines": 1222,
      "diagram_count": 7,
      "code_example_count": 12,
      "capability_type": "detection"
    },
    {
      "name": "Claim Boundaries",
      "section_size_lines": 89,
      "diagram_count": 2,
      "code_example_count": 3,
      "capability_type": "extraction"
    },
    {
      "name": "Stance Classification",
      "section_size_lines": 156,
      "diagram_count": 3,
      "code_example_count": 5,
      "capability_type": "classification"
    }
  ]
}

**Agent Analysis**:
- Evidence Detection: Too large (1222 lines) for quick MVP
- Claim Boundaries: Small (89 lines), 2 diagrams ✅
- Stance Classification: Medium (156 lines), 3 diagrams ✅

**Agent**: "I'll select Claim Boundaries for quickest MVP"

**Time**: 10 seconds (scan + analysis)
**Context**: 500 tokens
**Quality**: Data-driven decision
**Savings**: 97% context, 90x faster, better quality
```

---

## Example 5: Progressive Section Exploration

**Scenario**: Agent wants to understand capability structure before full extraction

### Without Skill

```markdown
**Agent**: *Must read full section to understand structure*
**Context**: All or nothing approach
```

### With Skill

```markdown
**Agent**: "I'll check metadata first"

**Step 1 - Metadata Only**:
section_extractor.py --section "Key Point Analysis" --no-content

**Agent Receives** (300 tokens):
{
  "section_title": "Primary Feature: Key Point Analysis",
  "line_start": 119,
  "line_end": 164,
  "has_diagrams": true,
  "diagram_count": 1,
  "diagram_types": ["flowchart"],
  "has_code_examples": true,
  "code_example_count": 1,
  "code_languages": ["python"],
  "content_length": 1372
}

**Agent**: "Only 1 diagram, 1 code example, 1372 chars. This is manageable, I'll extract full content"

**Step 2 - Full Extract**:
section_extractor.py --section "Key Point Analysis"

**Agent Receives** (2000 tokens):
{
  "content": "... full section ...",
  "diagrams": [{ parsed Mermaid diagram }],
  "code_blocks": [{ parsed Python example }]
}

**Agent**: "Perfect! Now I'll derive requirements from the flowchart"

**Total Approach**:
- Check metadata first (300 tokens)
- Extract only if worth it (2000 tokens)
- **Total**: 2300 tokens
- **Alternative**: Read full doc (15,000 tokens)
- **Savings**: 85%
```

---

## Example 6: Cross-Referencing Multiple Sections

**Scenario**: Agent needs to understand relationship between two capabilities

### Without Skill

```markdown
**Agent**: *Reads full document*
**Agent**: *Finds both sections*
**Agent**: *Keeps both in memory*
**Agent**: *Compares manually*

**Context**: 15,000+ tokens (full doc + working memory)
```

### With Skill

```markdown
**Agent**: "I'll extract both sections separately"

**Extract 1**:
section_extractor.py --section "Key Point Analysis"
**Returns**: 2000 tokens

**Agent**: *Derives requirements from KPA*

**Extract 2**:
section_extractor.py --section "Evidence Detection"
**Returns**: 3000 tokens

**Agent**: *Compares patterns*

**Agent**: "I see both use similar validation patterns. I'll note the commonality"

**Total Context**: 5000 tokens (sequential, not parallel)
**Savings**: 67% vs full document
**Benefit**: Can process sections sequentially, not all at once
```

---

## Example 7: Finding Diagram-Rich Sections

**Scenario**: Agent wants sections with most diagrams for requirement derivation

### Without Skill

```markdown
**Agent**: *Reads full document*
**Agent**: *Manually counts diagrams per section*
**Agent**: "This is tedious..."

**Time**: 20+ minutes
**Context**: 15,000 tokens
```

### With Skill

```markdown
**Agent**: "I'll scan capabilities and sort by diagram count"

**Script Executes**: capability_scanner.py

**Agent Receives**:
{
  "capabilities": [
    {"name": "Evidence Detection", "diagram_count": 7},
    {"name": "Key Point Analysis", "diagram_count": 5},
    {"name": "Argument Quality", "diagram_count": 4},
    {"name": "Claim Boundaries", "diagram_count": 2}
  ]
}

**Agent**: "Evidence Detection has most diagrams (7). I'll extract that section"

**Time**: 3 seconds
**Context**: 500 tokens + 3000 for extraction = 3500 total
**Savings**: 77% context, 400x faster
```

---

## Context Savings Summary

| Example | Without Skill | With Skill | Savings |
|---------|--------------|------------|---------|
| Find Capability | 15,000 tokens | 2,500 tokens | 83% |
| Verify Citation | 15,000 tokens | 300 tokens | 98% |
| Find Topic Sections | 15,000 tokens | 1,300 tokens | 91% |
| Select MVP | 15,000 tokens | 500 tokens | 97% |
| Progressive Exploration | 15,000 tokens | 2,300 tokens | 85% |
| Cross-Reference | 15,000 tokens | 5,000 tokens | 67% |
| Find Diagram Sections | 15,000 tokens | 3,500 tokens | 77% |
| **AVERAGE** | **15,000 tokens** | **2,200 tokens** | **85%** |

---

## Time Savings Summary

| Example | Without Skill | With Skill | Speedup |
|---------|--------------|------------|---------|
| Find Capability | 5-7 min | 30 sec | 10x |
| Verify Citation | 3-5 min | 5 sec | 36x |
| Find Topic Sections | 5-10 min | 2-3 sec | 150x |
| Select MVP | 10-15 min | 10 sec | 90x |
| Progressive Exploration | N/A | 3 sec | N/A |
| Cross-Reference | 10+ min | 4 sec | 150x |
| Find Diagram Sections | 20+ min | 3 sec | 400x |
| **AVERAGE** | **10 min** | **9 sec** | **67x** |

---

## Key Takeaways

1. **Always scan first** - 500 tokens tells you everything you need to know
2. **Extract only what you need** - One section at a time
3. **Use metadata to guide decisions** - Diagram/code counts indicate quality
4. **Check size before extracting** - Use --no-content to check metadata
5. **Progressive disclosure** - Start small (metadata), expand as needed

---

**Last Updated**: 2026-01-02
