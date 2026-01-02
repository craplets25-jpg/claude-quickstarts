#!/usr/bin/env python3
"""
Capability Scanner for DeepWiki

Scans DeepWiki document to find all available NLP capabilities
without loading full document into context.

Returns JSON summary with:
- Capability names
- Line ranges
- Diagram counts
- Code example counts
- Section sizes
- Keywords

Usage:
    python capability_scanner.py <deepwiki_path>
"""

from pathlib import Path
import json
import sys
from typing import List, Dict
from doc_parser import DocumentParser, TocEntry


class CapabilityScanner:
    """Scanner for finding capabilities in DeepWiki"""

    # Keywords that indicate a capability section
    CAPABILITY_KEYWORDS = [
        'analysis', 'detection', 'extraction', 'matching',
        'classification', 'scoring', 'generation', 'identification',
        'claim', 'evidence', 'argument', 'stance', 'topic',
        'keypoint', 'key point', 'quality', 'boundary'
    ]

    # Minimum section size to be considered a capability (lines)
    MIN_SECTION_SIZE = 30  # Reduced from 50 to catch smaller sections

    def __init__(self, deepwiki_path: str):
        """
        Initialize scanner with DeepWiki path.

        Args:
            deepwiki_path: Path to DeepWiki markdown file
        """
        self.parser = DocumentParser(Path(deepwiki_path))
        self.parser.extract_toc()

    def scan_capabilities(self) -> Dict:
        """
        Scan document for all capabilities.

        Returns:
            Dictionary with capability summaries and metadata
        """
        capabilities = []

        for entry in self.parser.toc:
            if self._is_capability_section(entry):
                cap_info = self._analyze_capability(entry)
                capabilities.append(cap_info)

        return {
            'capabilities': capabilities,
            'total_capabilities': len(capabilities),
            'document_stats': self.parser.get_document_stats()
        }

    def _is_capability_section(self, entry: TocEntry) -> bool:
        """
        Determine if TOC entry represents a capability.

        Uses heuristics:
        - Heading level (typically H1, H2, or H3)
        - Title contains capability keywords
        - Section size is substantial
        - Special patterns like "Primary Feature:" or service names
        """
        # Check heading level (H1, H2, or H3 - capabilities can be at various levels)
        if entry.level > 3:
            return False

        # Check section size
        if entry.line_end:
            section_size = entry.line_end - entry.line_start
            if section_size < self.MIN_SECTION_SIZE:
                return False

        # Check for capability keywords in title
        title_lower = entry.title.lower()
        has_keyword = any(
            keyword in title_lower
            for keyword in self.CAPABILITY_KEYWORDS
        )

        # Also check for "Feature:" or "Service:" patterns
        has_feature_pattern = 'feature:' in title_lower or 'service:' in title_lower

        return has_keyword or has_feature_pattern

    def _analyze_capability(self, entry: TocEntry) -> Dict:
        """
        Analyze a capability section in detail.

        Args:
            entry: TocEntry for the capability

        Returns:
            Dictionary with capability metadata
        """
        # Get section content
        content = self.parser.get_section_content(entry)

        # Find diagrams in this section
        diagrams = self.parser.find_diagrams(content)

        # Find code blocks
        code_blocks = self.parser.find_code_blocks(content)

        # Extract keywords from title
        keywords = self._extract_keywords(entry.title)

        # Calculate section size
        section_size = entry.line_end - entry.line_start if entry.line_end else 0

        # Detect capability type from keywords
        capability_type = self._detect_capability_type(entry.title, content)

        return {
            'name': entry.title,
            'line_start': entry.line_start,
            'line_end': entry.line_end,
            'section_size_lines': section_size,
            'heading_level': entry.level,
            'has_diagrams': len(diagrams) > 0,
            'diagram_count': len(diagrams),
            'diagram_types': [d['type'] for d in diagrams],
            'has_code_examples': len(code_blocks) > 0,
            'code_example_count': len(code_blocks),
            'code_languages': list(set(b['language'] for b in code_blocks)),
            'keywords': keywords,
            'capability_type': capability_type
        }

    def _extract_keywords(self, title: str) -> List[str]:
        """
        Extract searchable keywords from title.

        Args:
            title: Section title

        Returns:
            List of keywords
        """
        # Convert to lowercase and split
        words = title.lower().replace('-', ' ').replace('_', ' ').split()

        # Filter out short words and common articles
        stop_words = {'the', 'a', 'an', 'and', 'or', 'for', 'to', 'of', 'in', 'on'}
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]

        return keywords

    def _detect_capability_type(self, title: str, content: str) -> str:
        """
        Detect the type of capability from title and content.

        Returns:
            Capability type string
        """
        title_lower = title.lower()
        content_lower = content[:1000].lower()  # Check first 1000 chars

        type_patterns = {
            'text_analysis': ['analysis', 'analyze', 'detect', 'identify'],
            'classification': ['classif', 'categor'],
            'extraction': ['extract', 'find', 'locate'],
            'matching': ['match', 'align', 'similar'],
            'scoring': ['score', 'quality', 'assess'],
            'generation': ['generat', 'creat', 'produce'],
            'detection': ['detect', 'identif']
        }

        for cap_type, patterns in type_patterns.items():
            if any(pattern in title_lower or pattern in content_lower
                   for pattern in patterns):
                return cap_type

        return 'unknown'


def main():
    """Main entry point for capability scanner"""
    if len(sys.argv) < 2:
        print("Usage: python capability_scanner.py <deepwiki_path>")
        print("\nExample:")
        print("  python capability_scanner.py ../../../deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md")
        sys.exit(1)

    deepwiki_path = sys.argv[1]

    # Verify file exists
    if not Path(deepwiki_path).exists():
        print(f"Error: File not found: {deepwiki_path}")
        sys.exit(1)

    # Scan for capabilities
    scanner = CapabilityScanner(deepwiki_path)
    result = scanner.scan_capabilities()

    # Output JSON
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
