# Skills Implementation Plan - Script-Powered Workflows

**Purpose**: Detailed plan for using custom skills with embedded scripts to optimize the 3-agent pipeline

**Key Insight**: Scripts in skills execute OUTSIDE the context window, enabling complex processing without token costs

**Date**: 2026-01-02

---

## Executive Summary

Custom skills with embedded Python scripts can dramatically improve our pipeline by:
1. **Processing large documents** without consuming context (DeepWiki is 10,000+ lines)
2. **Automating structure extraction** (Mermaid diagrams, TOC, examples)
3. **Enabling consistent validation** (pattern detection, requirement format checks)
4. **Reducing agent workload** (focus on semantic reasoning, not syntax parsing)

---

## Critical Insight: We Already Have the Code!

Our codebase includes `doc_parser.py` which could be packaged into skills:

```python
from doc_parser import DocumentParser

parser = DocumentParser('deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md')
parser.extract_toc()

# Find sections by keyword
entries = parser.filter_toc_by_keywords(['Evidence Detection'])

# Get content without reading full doc
content = parser.get_section_content(entries[0])
```

**This is PERFECT for skills!** Package these utilities so agents can call them without implementing parsing logic.

---

## Skill 1: DeepWiki Navigator (SPEC LIBRARIAN)

### Current Pain Points

❌ **Must read entire DeepWiki** (10,000+ lines) → massive context usage
❌ **Manual section navigation** → error-prone, time-consuming
❌ **Repeated parsing** → every agent reinvents TOC extraction
❌ **Can't quickly scan capabilities** → must read sequentially

### Skill Solution: `deepwiki-navigator`

**Structure:**
```
deepwiki-navigator/
├── SKILL.md                    # Instructions for navigation
├── scripts/
│   ├── doc_parser.py           # Copy from our codebase!
│   ├── capability_scanner.py   # Find all capabilities
│   └── section_extractor.py    # Extract specific sections
└── EXAMPLES.md                 # Usage examples
```

### Key Scripts

#### 1. `capability_scanner.py`

**Purpose**: Scan DeepWiki and return list of capabilities WITHOUT loading full doc into context

```python
#!/usr/bin/env python3
"""
Scan DeepWiki to find all available capabilities.
Returns JSON list of capabilities with metadata.
"""

from pathlib import Path
from doc_parser import DocumentParser
import json

def scan_capabilities(deepwiki_path: str) -> dict:
    """
    Scan DeepWiki for all capabilities.

    Returns:
        {
            "capabilities": [
                {
                    "name": "Evidence Detection",
                    "line_start": 1234,
                    "line_end": 2456,
                    "has_diagrams": true,
                    "diagram_count": 3,
                    "has_examples": true,
                    "section_size_lines": 1222,
                    "keywords": ["evidence", "detection", "text", "analysis"]
                },
                ...
            ],
            "total_capabilities": 13,
            "document_size_lines": 10234
        }
    """
    parser = DocumentParser(Path(deepwiki_path))
    parser.extract_toc()

    capabilities = []

    # Identify capability sections (typically H2 or H3)
    for entry in parser.toc:
        if is_capability_section(entry):
            section_content = parser.get_section_content(entry)

            capabilities.append({
                "name": entry.title,
                "line_start": entry.line_start,
                "line_end": entry.line_end,
                "has_diagrams": "```mermaid" in section_content,
                "diagram_count": section_content.count("```mermaid"),
                "has_examples": "example" in section_content.lower(),
                "section_size_lines": entry.line_end - entry.line_start,
                "keywords": extract_keywords(entry.title)
            })

    return {
        "capabilities": capabilities,
        "total_capabilities": len(capabilities),
        "document_size_lines": len(parser.lines)
    }

def is_capability_section(entry) -> bool:
    """Determine if TOC entry represents a capability"""
    # Heuristics: specific heading levels, naming patterns
    capability_keywords = [
        'detection', 'analysis', 'extraction', 'matching',
        'classification', 'scoring', 'generation'
    ]

    title_lower = entry.title.lower()
    return any(keyword in title_lower for keyword in capability_keywords)

def extract_keywords(title: str) -> list:
    """Extract searchable keywords from title"""
    words = title.lower().replace('-', ' ').split()
    return [w for w in words if len(w) > 3]

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: capability_scanner.py <deepwiki_path>")
        sys.exit(1)

    result = scan_capabilities(sys.argv[1])
    print(json.dumps(result, indent=2))
```

#### 2. `section_extractor.py`

**Purpose**: Extract specific section content by line numbers

```python
#!/usr/bin/env python3
"""
Extract specific sections from DeepWiki by line numbers.
Returns only relevant content, not entire document.
"""

from pathlib import Path
import json

def extract_section(deepwiki_path: str, line_start: int, line_end: int) -> dict:
    """
    Extract section content by line range.

    Returns:
        {
            "content": "...",
            "line_count": 500,
            "has_diagrams": true,
            "diagrams": [...],
            "has_code_blocks": true,
            "code_blocks": [...]
        }
    """
    with open(deepwiki_path, 'r') as f:
        lines = f.readlines()

    section_lines = lines[line_start-1:line_end]
    content = ''.join(section_lines)

    return {
        "content": content,
        "line_count": len(section_lines),
        "has_diagrams": "```mermaid" in content,
        "diagrams": extract_diagrams(section_lines, line_start),
        "has_code_blocks": "```python" in content or "```json" in content,
        "code_blocks": extract_code_blocks(section_lines, line_start)
    }

def extract_diagrams(lines: list, offset: int) -> list:
    """Extract all Mermaid diagrams with line numbers"""
    diagrams = []
    in_diagram = False
    diagram_start = None
    diagram_lines = []

    for i, line in enumerate(lines):
        line_num = offset + i

        if '```mermaid' in line:
            in_diagram = True
            diagram_start = line_num
            diagram_lines = []
        elif in_diagram and '```' in line:
            diagrams.append({
                "line_start": diagram_start,
                "line_end": line_num,
                "content": '\n'.join(diagram_lines),
                "type": detect_diagram_type(diagram_lines)
            })
            in_diagram = False
        elif in_diagram:
            diagram_lines.append(line.rstrip())

    return diagrams

def detect_diagram_type(lines: list) -> str:
    """Detect diagram type from first line"""
    if not lines:
        return "unknown"

    first_line = lines[0].lower()

    if "flowchart" in first_line or "graph" in first_line:
        return "flowchart"
    elif "classDiagram" in first_line:
        return "class"
    elif "sequenceDiagram" in first_line:
        return "sequence"
    elif "stateDiagram" in first_line:
        return "state"
    else:
        return "unknown"

def extract_code_blocks(lines: list, offset: int) -> list:
    """Extract code examples with line numbers"""
    # Similar to extract_diagrams but for code blocks
    pass

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: section_extractor.py <deepwiki_path> <line_start> <line_end>")
        sys.exit(1)

    result = extract_section(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    print(json.dumps(result, indent=2))
```

### Agent Workflow with Skill

**Before (current)**:
```
1. Agent: "Read entire DeepWiki" → 10,000 lines loaded into context
2. Agent: Manually search for capability sections
3. Agent: Extract relevant parts from memory
4. Agent: Parse Mermaid diagrams character by character
```
**Token cost**: ~15,000 tokens just for document loading

**After (with skill)**:
```
1. Agent: "Use deepwiki-navigator skill to scan capabilities"
2. Skill script runs: capability_scanner.py
3. Returns JSON: List of 13 capabilities with metadata
4. Agent: Reviews list, selects "Key Point Analysis"
5. Agent: "Extract section for Key Point Analysis"
6. Skill script runs: section_extractor.py --lines 4500-6200
7. Returns: Only relevant section (1700 lines) with parsed diagrams
```
**Token cost**: ~2,500 tokens for relevant content only

**Savings**: ~80% reduction in context usage!

---

## Skill 2: Diagram Requirement Extractor (SPEC LIBRARIAN)

### Current Pain Points

❌ **Manual Mermaid parsing** → error-prone, syntax issues
❌ **Inconsistent node extraction** → missed relationships
❌ **No validation** → can't verify diagram syntax
❌ **Repeated parsing** → every diagram parsed from scratch

### Skill Solution: `diagram-requirement-extractor`

**Structure:**
```
diagram-requirement-extractor/
├── SKILL.md                        # Derivation rules
├── EXAMPLES.md                     # 10 example diagram → requirements
├── scripts/
│   ├── mermaid_parser.py           # Parse Mermaid syntax
│   ├── node_extractor.py           # Extract nodes/edges
│   ├── relationship_analyzer.py    # Analyze relationships
│   └── requirement_generator.py    # Generate requirement cards
└── templates/
    └── requirement_card_template.md
```

### Key Scripts

#### `mermaid_parser.py`

```python
#!/usr/bin/env python3
"""
Parse Mermaid diagram syntax and extract structure.
Returns nodes, edges, and relationships as JSON.
"""

import re
import json

def parse_mermaid_diagram(diagram_content: str, line_start: int) -> dict:
    """
    Parse Mermaid diagram and extract structure.

    Returns:
        {
            "type": "flowchart",
            "nodes": [
                {"id": "A", "label": "Start", "shape": "rounded"},
                {"id": "B", "label": "Process", "shape": "rectangle"}
            ],
            "edges": [
                {"from": "A", "to": "B", "label": "next", "line_num": 2345}
            ],
            "line_start": 2340,
            "line_end": 2360
        }
    """
    lines = diagram_content.strip().split('\n')

    # Detect diagram type
    diagram_type = detect_type(lines[0])

    nodes = []
    edges = []

    for i, line in enumerate(lines[1:], start=1):
        line_num = line_start + i

        # Parse node definitions
        node_match = re.match(r'\s*(\w+)\[(.+?)\]', line)
        if node_match:
            nodes.append({
                "id": node_match.group(1),
                "label": node_match.group(2),
                "shape": detect_shape(line),
                "line_num": line_num
            })

        # Parse edge definitions
        edge_match = re.search(r'(\w+)\s*--?>?\|?(.+?)?\|?\s*(\w+)', line)
        if edge_match:
            edges.append({
                "from": edge_match.group(1),
                "to": edge_match.group(3),
                "label": edge_match.group(2).strip() if edge_match.group(2) else "",
                "line_num": line_num
            })

    return {
        "type": diagram_type,
        "nodes": nodes,
        "edges": edges,
        "line_start": line_start,
        "line_end": line_start + len(lines)
    }

def detect_type(first_line: str) -> str:
    """Detect diagram type from first line"""
    first_line_lower = first_line.lower()

    if "flowchart" in first_line_lower or "graph" in first_line_lower:
        return "flowchart"
    elif "classdiagram" in first_line_lower:
        return "class"
    elif "sequencediagram" in first_line_lower:
        return "sequence"
    elif "statediagram" in first_line_lower:
        return "state"
    else:
        return "unknown"

def detect_shape(line: str) -> str:
    """Detect node shape from syntax"""
    if '[[' in line and ']]' in line:
        return "subroutine"
    elif '(' in line and ')' in line:
        return "rounded"
    elif '[' in line and ']' in line:
        return "rectangle"
    elif '{' in line and '}' in line:
        return "diamond"
    else:
        return "default"

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: mermaid_parser.py <diagram_content> <line_start>")
        sys.exit(1)

    diagram = sys.argv[1]
    line_start = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    result = parse_mermaid_diagram(diagram, line_start)
    print(json.dumps(result, indent=2))
```

#### `requirement_generator.py`

```python
#!/usr/bin/env python3
"""
Generate requirement cards from parsed diagram structure.
Applies derivation rules to convert structure to requirements.
"""

import json

def generate_requirements(parsed_diagram: dict) -> list:
    """
    Generate requirement cards from parsed diagram.

    Returns list of requirement dictionaries.
    """
    requirements = []

    diagram_type = parsed_diagram['type']
    nodes = parsed_diagram['nodes']
    edges = parsed_diagram['edges']

    if diagram_type == "flowchart":
        requirements.extend(generate_flowchart_requirements(nodes, edges))
    elif diagram_type == "class":
        requirements.extend(generate_class_requirements(nodes, edges))
    elif diagram_type == "sequence":
        requirements.extend(generate_sequence_requirements(nodes, edges))

    return requirements

def generate_flowchart_requirements(nodes: list, edges: list) -> list:
    """Generate requirements from flowchart structure"""
    requirements = []

    # Input node (first node)
    if nodes:
        requirements.append({
            "type": "input",
            "description": f"System accepts {nodes[0]['label']}",
            "source_line": nodes[0]['line_num'],
            "diagram_element": f"Node: {nodes[0]['id']}"
        })

    # Processing nodes (middle nodes)
    for node in nodes[1:-1]:
        if node['shape'] == 'rectangle':
            requirements.append({
                "type": "processing",
                "description": f"System performs {node['label']}",
                "source_line": node['line_num'],
                "diagram_element": f"Node: {node['id']}"
            })
        elif node['shape'] == 'diamond':
            requirements.append({
                "type": "decision",
                "description": f"System evaluates {node['label']}",
                "source_line": node['line_num'],
                "diagram_element": f"Node: {node['id']}"
            })

    # Output node (last node)
    if len(nodes) > 1:
        requirements.append({
            "type": "output",
            "description": f"System produces {nodes[-1]['label']}",
            "source_line": nodes[-1]['line_num'],
            "diagram_element": f"Node: {nodes[-1]['id']}"
        })

    # Order preservation (from edges)
    if len(edges) > 1:
        requirements.append({
            "type": "ordering",
            "description": "System preserves processing order",
            "source_line": edges[0]['line_num'],
            "diagram_element": "Edge sequence",
            "details": " → ".join([e['from'] for e in edges] + [edges[-1]['to']])
        })

    return requirements

def generate_class_requirements(nodes: list, edges: list) -> list:
    """Generate requirements from class diagram"""
    requirements = []

    # Inheritance relationships
    for edge in edges:
        if '<|--' in str(edge.get('label', '')):
            requirements.append({
                "type": "inheritance",
                "description": f"{edge['to']} inherits from {edge['from']}",
                "source_line": edge['line_num'],
                "diagram_element": f"Edge: {edge['from']} <|-- {edge['to']}"
            })

    # Composition relationships
    for edge in edges:
        if '*--' in str(edge.get('label', '')):
            requirements.append({
                "type": "composition",
                "description": f"{edge['from']} contains {edge['to']}",
                "source_line": edge['line_num'],
                "diagram_element": f"Edge: {edge['from']} *-- {edge['to']}"
            })

    return requirements

def generate_sequence_requirements(nodes: list, edges: list) -> list:
    """Generate requirements from sequence diagram"""
    requirements = []

    # Message passing
    for edge in edges:
        requirements.append({
            "type": "interaction",
            "description": f"{edge['from']} sends '{edge['label']}' to {edge['to']}",
            "source_line": edge['line_num'],
            "diagram_element": f"Message: {edge['from']} -> {edge['to']}"
        })

    return requirements

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: requirement_generator.py <parsed_diagram_json>")
        sys.exit(1)

    parsed = json.loads(sys.argv[1])
    requirements = generate_requirements(parsed)
    print(json.dumps(requirements, indent=2))
```

### Agent Workflow with Skill

**Before**:
```
Agent: "Parse this Mermaid diagram:
flowchart LR
    A[Input] --> B[Validate]
    B --> C[Transform]
    C --> D[Output]

...now extract requirements"
```
Agent must manually:
- Identify node syntax patterns
- Extract labels
- Detect edge types
- Derive requirements from structure
- Generate requirement cards

**After**:
```
Agent: "Use diagram-requirement-extractor skill on this diagram"

Skill executes:
1. mermaid_parser.py → Extracts nodes/edges JSON
2. requirement_generator.py → Generates requirements

Returns:
{
  "requirements": [
    {"type": "input", "description": "System accepts Input", "line": 2345},
    {"type": "processing", "description": "System performs Validate", "line": 2346},
    {"type": "processing", "description": "System performs Transform", "line": 2347},
    {"type": "output", "description": "System produces Output", "line": 2348},
    {"type": "ordering", "description": "System preserves order: A → B → C → D", "line": 2345}
  ]
}

Agent: Reviews requirements, refines descriptions, creates final cards
```

**Benefit**: Agent focuses on semantic understanding, scripts handle syntax

---

## Skill 3: Vendor Pattern Detector (SPEC REVIEWER)

### Current Pain Points

❌ **Manual pattern detection** → miss vendor-specific details
❌ **Inconsistent filtering** → some URLs slip through
❌ **No validation** → can't verify all patterns caught
❌ **Time-consuming** → must review every line

### Skill Solution: `vendor-pattern-detector`

**Structure:**
```
vendor-pattern-detector/
├── SKILL.md                    # Filtering rules
├── PATTERNS.md                 # Comprehensive pattern library
├── scripts/
│   ├── url_detector.py         # Find URLs and endpoints
│   ├── method_extractor.py     # Find vendor method names
│   ├── timeout_finder.py       # Find timeouts and limits
│   ├── error_message_parser.py # Find error message strings
│   └── pattern_validator.py    # Validate filtering complete
└── tests/
    └── test_patterns.py        # Validate pattern detection
```

### Key Script

#### `pattern_validator.py`

```python
#!/usr/bin/env python3
"""
Comprehensive vendor-specific pattern detector.
Scans requirement cards and flags all vendor-specific content.
"""

import json
import re

def detect_vendor_patterns(requirement_cards: list) -> dict:
    """
    Scan requirement cards for vendor-specific patterns.

    Returns:
        {
            "flagged_items": [
                {
                    "card_id": "KPA-012",
                    "pattern_type": "url",
                    "content": "https://motion-evidence.debater.res.ibm.com/...",
                    "line": "...",
                    "suggestion": "Move to legacy_notes.md"
                }
            ],
            "summary": {
                "urls": 5,
                "method_names": 12,
                "timeouts": 3,
                "error_messages": 8,
                "total_flagged": 28
            }
        }
    """
    flagged = []

    patterns = {
        "url": r'https?://[^\s]+',
        "method_name": r'(?:def |\.)(run_in_batch|evidence_detection|kp_analysis)\(',
        "timeout": r'\d+\s*(seconds?|minutes?|ms)\b',
        "error_message": r'"([^"]+)"',  # Quoted strings
        "vendor_name": r'\b(IBM|Watson|AWS|Azure|Google|Debater)\b',
        "config_value": r'(?:timeout|limit|max|min)\s*[=:]\s*\d+',
    }

    for card in requirement_cards:
        card_id = card.get('id', 'UNKNOWN')
        content = json.dumps(card)  # Search entire card as string

        for pattern_type, pattern in patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)

            for match in matches:
                flagged.append({
                    "card_id": card_id,
                    "pattern_type": pattern_type,
                    "content": match.group(0),
                    "context": get_context(content, match.start(), 50),
                    "suggestion": generate_suggestion(pattern_type)
                })

    # Generate summary
    summary = {}
    for pattern_type in patterns.keys():
        summary[pattern_type] = sum(1 for f in flagged if f['pattern_type'] == pattern_type)
    summary['total_flagged'] = len(flagged)

    return {
        "flagged_items": flagged,
        "summary": summary,
        "scan_complete": True
    }

def get_context(text: str, pos: int, length: int) -> str:
    """Extract surrounding context for a match"""
    start = max(0, pos - length)
    end = min(len(text), pos + length)
    return text[start:end]

def generate_suggestion(pattern_type: str) -> str:
    """Generate action suggestion based on pattern type"""
    suggestions = {
        "url": "Move URL to legacy_notes.md - keep only 'API endpoint' in requirement",
        "method_name": "Move method name to legacy_notes.md - keep only 'batch processing' in requirement",
        "timeout": "Move specific timeout to legacy_notes.md - keep only 'timeout support' in requirement",
        "error_message": "Move error text to legacy_notes.md - keep only 'error validation' in requirement",
        "vendor_name": "Remove vendor name - rephrase as 'system' or 'service'",
        "config_value": "Move specific value to legacy_notes.md - keep only capability in requirement"
    }
    return suggestions.get(pattern_type, "Review for vendor-specificity")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: pattern_validator.py <requirement_cards.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        cards = json.load(f)

    result = detect_vendor_patterns(cards)
    print(json.dumps(result, indent=2))
```

### Agent Workflow with Skill

**Before**:
```
Agent: Reads 40 requirement cards (60KB JSON)
Agent: Manually scans each card for vendor patterns
Agent: Decides what to move to legacy_notes
Agent: Rewrites cards manually
```
**Time**: 30-45 minutes per capability

**After**:
```
Agent: "Use vendor-pattern-detector skill on requirement_cards.json"

Skill executes pattern_validator.py:
Returns:
{
  "flagged_items": [
    {
      "card_id": "KPA-012",
      "pattern_type": "url",
      "content": "https://motion-evidence.debater.res.ibm.com/...",
      "suggestion": "Move URL to legacy_notes.md"
    },
    {
      "card_id": "KPA-015",
      "pattern_type": "method_name",
      "content": "run_in_batch()",
      "suggestion": "Move method name to legacy_notes.md"
    }
  ],
  "summary": {
    "urls": 5,
    "method_names": 12,
    "timeouts": 3,
    "error_messages": 8,
    "total_flagged": 28
  }
}

Agent: Reviews flagged items, makes semantic decisions, applies filtering
```
**Time**: 10-15 minutes per capability

**Benefit**: 60% faster, 100% coverage of patterns

---

## Skill 4: TDD Progress Tracker (CODING AGENT)

### Current Pain Points

❌ **Manual JSON parsing** → error-prone reading of feature_list.json
❌ **Manual progress updates** → forget to update "passing" field
❌ **No automatic early stopping** → continue when all tests pass
❌ **Inconsistent commit messages** → varies by agent

### Skill Solution: `tdd-progress-tracker`

**Structure:**
```
tdd-progress-tracker/
├── SKILL.md                        # TDD workflow
├── COMMIT_TEMPLATES.md             # Standard commit messages
├── scripts/
│   ├── next_test_finder.py         # Find next failing test
│   ├── progress_updater.py         # Update feature_list.json
│   ├── test_counter.py             # Count passing tests
│   ├── early_stop_checker.py       # Check if all tests pass
│   └── commit_message_generator.py # Generate commit messages
└── checklists/
    └── iteration_checklist.md      # Per-iteration checklist
```

### Key Scripts

#### `next_test_finder.py`

```python
#!/usr/bin/env python3
"""
Find the next failing test from feature_list.json.
Returns test details without loading JSON into context.
"""

import json

def find_next_test(feature_list_path: str) -> dict:
    """
    Find first test where "passing": false

    Returns:
        {
            "found": true,
            "test_id": "TEST-015",
            "description": "Validates empty string rejection",
            "requirement_id": "KPA-005",
            "test_type": "unit",
            "test_index": 14,
            "total_tests": 40,
            "passing_count": 14,
            "remaining_count": 26
        }
    """
    with open(feature_list_path, 'r') as f:
        features = json.load(f)

    total = len(features)
    passing = sum(1 for f in features if f.get('passing', False))

    for idx, test in enumerate(features):
        if not test.get('passing', False):
            return {
                "found": True,
                "test_id": test['id'],
                "description": test['description'],
                "requirement_id": test.get('requirement_id', 'UNKNOWN'),
                "test_type": test.get('test_type', 'unknown'),
                "test_index": idx,
                "total_tests": total,
                "passing_count": passing,
                "remaining_count": total - passing
            }

    # All tests passing
    return {
        "found": False,
        "message": "All tests passing!",
        "total_tests": total,
        "passing_count": total,
        "remaining_count": 0
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: next_test_finder.py <feature_list.json>")
        sys.exit(1)

    result = find_next_test(sys.argv[1])
    print(json.dumps(result, indent=2))
```

#### `progress_updater.py`

```python
#!/usr/bin/env python3
"""
Update feature_list.json to mark test as passing.
Handles JSON editing automatically.
"""

import json

def mark_test_passing(feature_list_path: str, test_id: str) -> dict:
    """
    Mark specific test as passing in feature_list.json

    Returns:
        {
            "success": true,
            "test_id": "TEST-015",
            "previous_status": false,
            "new_status": true,
            "passing_count": 15,
            "total_tests": 40
        }
    """
    with open(feature_list_path, 'r') as f:
        features = json.load(f)

    found = False
    previous_status = None

    for test in features:
        if test['id'] == test_id:
            previous_status = test.get('passing', False)
            test['passing'] = True
            found = True
            break

    if not found:
        return {
            "success": False,
            "error": f"Test {test_id} not found",
            "test_id": test_id
        }

    # Write back
    with open(feature_list_path, 'w') as f:
        json.dump(features, f, indent=2)

    passing = sum(1 for f in features if f.get('passing', False))

    return {
        "success": True,
        "test_id": test_id,
        "previous_status": previous_status,
        "new_status": True,
        "passing_count": passing,
        "total_tests": len(features)
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: progress_updater.py <feature_list.json> <test_id>")
        sys.exit(1)

    result = mark_test_passing(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
```

#### `commit_message_generator.py`

```python
#!/usr/bin/env python3
"""
Generate standardized commit message for test implementation.
"""

import json

def generate_commit_message(test_info: dict, passing_count: int, total_tests: int) -> str:
    """
    Generate commit message following standard template.

    Args:
        test_info: Dict with test_id, description, requirement_id
        passing_count: Number of tests now passing
        total_tests: Total number of tests

    Returns:
        Formatted commit message string
    """
    template = """Implement {test_id}: {description}

- Implemented {requirement_id} requirement
- Test now passing
- {passing_count}/{total_tests} tests now passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"""

    return template.format(
        test_id=test_info['test_id'],
        description=test_info['description'],
        requirement_id=test_info.get('requirement_id', 'UNKNOWN'),
        passing_count=passing_count,
        total_tests=total_tests
    )

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 4:
        print("Usage: commit_message_generator.py <test_info_json> <passing_count> <total_tests>")
        sys.exit(1)

    test_info = json.loads(sys.argv[1])
    message = generate_commit_message(test_info, int(sys.argv[2]), int(sys.argv[3]))
    print(message)
```

### Agent Workflow with Skill

**Before**:
```
Agent: Read feature_list.json (23KB)
Agent: Parse JSON mentally
Agent: Find first "passing": false
Agent: Remember test details
Agent: Implement test
Agent: Run pytest
Agent: Read feature_list.json again
Agent: Edit JSON to set "passing": true
Agent: Write commit message manually
Agent: Commit
```

**After**:
```
Agent: "Use tdd-progress-tracker skill to find next test"
Skill: next_test_finder.py → Returns TEST-015 details

Agent: Implement code for TEST-015
Agent: Run pytest → PASSED

Agent: "Use tdd-progress-tracker skill to mark TEST-015 passing"
Skill: progress_updater.py → Updates feature_list.json automatically

Agent: "Use tdd-progress-tracker skill to generate commit message"
Skill: commit_message_generator.py → Returns formatted message

Agent: git commit -m "<generated message>"

Agent: "Use tdd-progress-tracker skill to check if complete"
Skill: early_stop_checker.py → Returns {"all_passing": false, "remaining": 25}

Agent: Continue to next test
```

**Benefits**:
- No manual JSON parsing/editing
- Automatic progress tracking
- Consistent commit messages
- Built-in early stopping check
- Faster iteration (less time on bookkeeping)

---

## Skill 5: Example Triangulator (SPEC LIBRARIAN)

### Current Pain Points

❌ **Reading multiple example files** → each file consumes context
❌ **Manual pattern extraction** → compare inputs/outputs mentally
❌ **Inconsistent triangulation** → might miss commonalities
❌ **Time-consuming** → read 3-5 examples sequentially

### Skill Solution: `example-triangulator`

**Structure:**
```
example-triangulator/
├── SKILL.md                    # Triangulation methodology
├── PATTERNS.md                 # Common pattern types
├── scripts/
│   ├── example_parser.py       # Parse JSON/Python examples
│   ├── shape_extractor.py      # Extract input/output shapes
│   ├── pattern_finder.py       # Find common patterns
│   └── triangulation_report.py # Generate triangulation report
└── EXAMPLES.md                 # Example triangulation
```

### Key Script

#### `triangulation_report.py`

```python
#!/usr/bin/env python3
"""
Triangulate multiple example files to find common patterns.
Returns invariant patterns across all examples.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

def triangulate_examples(example_paths: List[str]) -> dict:
    """
    Analyze multiple examples and find common patterns.

    Returns:
        {
            "input_shape": {
                "type": "list",
                "element_type": "string",
                "constraints": ["non-empty", "max_length: 10000"]
            },
            "output_shape": {
                "type": "dict",
                "required_keys": ["keypoint_matchings"],
                "keypoint_matchings": {
                    "type": "list",
                    "element_shape": {...}
                }
            },
            "validation_rules": [
                "Empty strings rejected",
                "ID uniqueness enforced",
                "List length must match"
            ],
            "examples_analyzed": 5,
            "confidence": "high"  # high if all examples agree
        }
    """
    examples = []

    for path in example_paths:
        with open(path, 'r') as f:
            if path.endswith('.json'):
                examples.append(json.load(f))
            elif path.endswith('.py'):
                # Extract from Python code
                examples.append(extract_from_python(f.read()))

    # Extract patterns
    input_shapes = [extract_input_shape(ex) for ex in examples]
    output_shapes = [extract_output_shape(ex) for ex in examples]
    validations = [extract_validations(ex) for ex in examples]

    # Find commonalities
    common_input = find_common_shape(input_shapes)
    common_output = find_common_shape(output_shapes)
    invariant_validations = find_invariant_validations(validations)

    # Calculate confidence
    confidence = "high" if all_examples_agree(examples) else "medium"

    return {
        "input_shape": common_input,
        "output_shape": common_output,
        "validation_rules": invariant_validations,
        "examples_analyzed": len(examples),
        "confidence": confidence,
        "divergences": find_divergences(examples) if confidence != "high" else []
    }

def extract_input_shape(example: dict) -> dict:
    """Extract input data shape from example"""
    # Implementation would analyze the example structure
    pass

def extract_output_shape(example: dict) -> dict:
    """Extract output data shape from example"""
    pass

def extract_validations(example: dict) -> list:
    """Extract validation rules from example"""
    pass

def find_common_shape(shapes: list) -> dict:
    """Find common structure across all shapes"""
    pass

def find_invariant_validations(validations: list) -> list:
    """Find validation rules present in all examples"""
    pass

def all_examples_agree(examples: list) -> bool:
    """Check if all examples show consistent patterns"""
    pass

def find_divergences(examples: list) -> list:
    """Identify where examples differ"""
    pass

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: triangulation_report.py <example1.json> <example2.json> ...")
        sys.exit(1)

    result = triangulate_examples(sys.argv[1:])
    print(json.dumps(result, indent=2))
```

### Agent Workflow with Skill

**Before**:
```
Agent: Read example1.json (5KB)
Agent: Read example2.json (8KB)
Agent: Read example3.json (6KB)
Agent: Compare mentally to find patterns
Agent: Extract common input shape
Agent: Extract common output shape
Agent: Identify validation rules
```
**Context**: 19KB loaded, manual comparison

**After**:
```
Agent: "Use example-triangulator skill on example1.json, example2.json, example3.json"

Skill: triangulation_report.py → Processes all examples

Returns:
{
  "input_shape": {
    "type": "list",
    "element_type": "string",
    "constraints": ["non-empty", "max: 10000"]
  },
  "output_shape": {
    "type": "dict",
    "required_keys": ["keypoint_matchings"],
    ...
  },
  "validation_rules": [
    "Empty strings rejected",
    "ID uniqueness enforced"
  ],
  "confidence": "high"
}

Agent: Reviews patterns, derives requirements
```
**Context**: Minimal (just the summary), no example files loaded

---

## Summary: Script Execution Benefits

### Context Window Savings

| Workflow | Before (tokens) | After (tokens) | Savings |
|----------|----------------|----------------|---------|
| **Capability Selection** | 15,000 | 2,500 | 83% |
| **Diagram Parsing** | 5,000 | 500 | 90% |
| **Vendor Pattern Detection** | 8,000 | 1,000 | 88% |
| **Progress Tracking** | 3,000 | 200 | 93% |
| **Example Triangulation** | 19,000 | 1,500 | 92% |
| **TOTAL** | **50,000** | **5,700** | **89%** |

### Speed Improvements

| Task | Before (minutes) | After (minutes) | Speedup |
|------|------------------|-----------------|---------|
| Capability selection | 15 | 2 | 7.5x |
| Diagram analysis | 10 | 3 | 3.3x |
| Vendor filtering | 30 | 10 | 3x |
| Test implementation | 90 | 60 | 1.5x |
| **TOTAL PER CAPABILITY** | **145** | **75** | **1.9x** |

### Quality Improvements

✅ **Consistency**: Scripts ensure identical processing every time
✅ **Completeness**: Pattern detection catches 100% of known patterns
✅ **Validation**: Built-in checks prevent missing requirements
✅ **Traceability**: Automatic line number tracking
✅ **Reproducibility**: Same inputs → same outputs always

---

## Implementation Priority

### Phase 1: Immediate Value (Week 1)

1. **`deepwiki-navigator`** - Biggest context savings (83%)
   - Package existing doc_parser.py
   - Add capability_scanner.py
   - Test on Experiment 03

2. **`tdd-progress-tracker`** - Fastest to implement
   - Extract existing logic from prompts
   - Add automation scripts
   - Test on next coding session

### Phase 2: High Value (Week 2)

3. **`diagram-requirement-extractor`** - Complex but high ROI
   - Implement Mermaid parser
   - Add requirement generator
   - Validate on 10 diagrams

4. **`vendor-pattern-detector`** - Quality improvement
   - Build pattern library
   - Implement validators
   - Test on existing requirement cards

### Phase 3: Advanced (Week 3)

5. **`example-triangulator`** - Sophisticated analysis
   - Implement shape extractors
   - Add pattern finders
   - Test on multiple examples

---

## Success Metrics

### Measure These Before/After Skills

1. **Context Usage**: Total tokens per capability
2. **Time to Complete**: Minutes from start to all tests passing
3. **Error Rate**: Number of missed patterns/requirements
4. **Consistency**: Variance between runs on same capability
5. **Agent Satisfaction**: Subjective "ease of use" rating

### Target Goals

- ✅ 80%+ reduction in context usage
- ✅ 2x speedup in implementation
- ✅ 95%+ pattern detection accuracy
- ✅ Zero missed requirements
- ✅ 100% consistent processing

---

## Next Steps

### Immediate (This Week)

1. **Extract `doc_parser.py`** from existing codebase
2. **Create `deepwiki-navigator` skill** as proof of concept
3. **Test on a new capability** (e.g., Claim Detection)
4. **Measure context savings** and speed improvement

### Short Term (Next 2 Weeks)

5. Package remaining 4 skills
6. Run parallel experiment (with/without skills)
7. Document results and ROI
8. Refine based on findings

### Long Term (Next Month)

9. Build organizational skill library
10. Share skills across team
11. Version and maintain skills
12. Create new skills as patterns emerge

---

## Related Documentation

- [Custom Skills Analysis](./CUSTOM_SKILLS_ANALYSIS.md)
- [Experiment 03 Strategy](./EXPERIMENT_03_STRATEGY.md)
- [Custom Skills Development](/.claude/claude-docs/skills-docs/03_skills_custom_development.ipynb)
- [Directory Structure Rationale](./DIRECTORY_STRUCTURE_RATIONALE.md)

---

**Last Updated**: 2026-01-02
**Maintained By**: Experiment Infrastructure Team
