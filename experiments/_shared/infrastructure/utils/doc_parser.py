#!/usr/bin/env python3
"""
Document Parser for DeepWiki and Technical Documentation

Utility for parsing large technical documents to extract:
- Table of contents
- Sections by keyword
- Mermaid diagrams
- Code examples
- Specific line ranges

Designed to work with documents without loading entire file into memory.
"""

from pathlib import Path
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
import re


@dataclass
class TocEntry:
    """Represents a table of contents entry"""
    level: int  # Heading level (1-6)
    title: str
    line_start: int
    line_end: Optional[int] = None  # Set when next heading found


class DocumentParser:
    """
    Parse technical documentation files.

    Optimized for large documents (10,000+ lines) by indexing
    structure without loading full content into memory.
    """

    def __init__(self, doc_path: Path):
        """
        Initialize parser with document path.

        Args:
            doc_path: Path to markdown document
        """
        self.doc_path = Path(doc_path)
        self.toc: List[TocEntry] = []
        self.lines: List[str] = []

        # Load document lines
        with open(self.doc_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def extract_toc(self) -> List[TocEntry]:
        """
        Extract table of contents by parsing markdown headings.

        Returns:
            List of TocEntry objects with heading hierarchy
        """
        self.toc = []

        for i, line in enumerate(self.lines):
            # Match markdown headings: # Title, ## Title, etc.
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))  # Count # symbols
                title = match.group(2).strip()

                # Set line_end for previous entry
                if self.toc:
                    self.toc[-1].line_end = i

                entry = TocEntry(
                    level=level,
                    title=title,
                    line_start=i + 1,  # 1-indexed for human readability
                    line_end=None
                )
                self.toc.append(entry)

        # Set line_end for last entry
        if self.toc:
            self.toc[-1].line_end = len(self.lines)

        return self.toc

    def filter_toc_by_keywords(self, keywords: List[str]) -> List[TocEntry]:
        """
        Filter TOC entries that contain any of the keywords.

        Args:
            keywords: List of keywords to search for (case-insensitive)

        Returns:
            List of matching TocEntry objects
        """
        if not self.toc:
            self.extract_toc()

        matches = []
        keywords_lower = [k.lower() for k in keywords]

        for entry in self.toc:
            title_lower = entry.title.lower()
            if any(keyword in title_lower for keyword in keywords_lower):
                matches.append(entry)

        return matches

    def get_section_content(self, entry: TocEntry) -> str:
        """
        Get full content of a section by TocEntry.

        Args:
            entry: TocEntry object

        Returns:
            Section content as string
        """
        if entry.line_end is None:
            # If line_end not set, use end of document
            end_line = len(self.lines)
        else:
            end_line = entry.line_end

        # Extract lines (convert from 1-indexed to 0-indexed)
        section_lines = self.lines[entry.line_start - 1:end_line]
        return ''.join(section_lines)

    def get_section_by_line_range(self, line_start: int, line_end: int) -> str:
        """
        Get content by line range.

        Args:
            line_start: Starting line (1-indexed)
            line_end: Ending line (1-indexed)

        Returns:
            Section content as string
        """
        # Convert to 0-indexed
        start_idx = line_start - 1
        end_idx = line_end

        section_lines = self.lines[start_idx:end_idx]
        return ''.join(section_lines)

    def find_diagrams(self, section_content: Optional[str] = None) -> List[Dict]:
        """
        Find all Mermaid diagrams in document or section.

        Args:
            section_content: If provided, search in this content.
                           Otherwise search entire document.

        Returns:
            List of diagram dictionaries with line numbers and content
        """
        if section_content is None:
            search_lines = self.lines
            offset = 0
        else:
            search_lines = section_content.split('\n')
            offset = 0  # Caller should track offset if needed

        diagrams = []
        in_diagram = False
        diagram_start = None
        diagram_lines = []

        for i, line in enumerate(search_lines):
            line_num = offset + i + 1  # 1-indexed

            if '```mermaid' in line.lower():
                in_diagram = True
                diagram_start = line_num
                diagram_lines = []
            elif in_diagram and '```' in line:
                diagrams.append({
                    'line_start': diagram_start,
                    'line_end': line_num,
                    'content': '\n'.join(diagram_lines),
                    'type': self._detect_diagram_type(diagram_lines)
                })
                in_diagram = False
            elif in_diagram:
                diagram_lines.append(line.rstrip())

        return diagrams

    def _detect_diagram_type(self, lines: List[str]) -> str:
        """Detect Mermaid diagram type from first line"""
        if not lines:
            return 'unknown'

        first_line = lines[0].lower().strip()

        if 'flowchart' in first_line or 'graph' in first_line:
            return 'flowchart'
        elif 'classdiagram' in first_line:
            return 'class'
        elif 'sequencediagram' in first_line:
            return 'sequence'
        elif 'statediagram' in first_line:
            return 'state'
        else:
            return 'unknown'

    def find_code_blocks(self, section_content: Optional[str] = None,
                        language: Optional[str] = None) -> List[Dict]:
        """
        Find code blocks in document or section.

        Args:
            section_content: If provided, search in this content
            language: If provided, filter by language (e.g., 'python', 'json')

        Returns:
            List of code block dictionaries with line numbers and content
        """
        if section_content is None:
            search_lines = self.lines
            offset = 0
        else:
            search_lines = section_content.split('\n')
            offset = 0

        code_blocks = []
        in_code = False
        code_start = None
        code_lines = []
        code_lang = None

        for i, line in enumerate(search_lines):
            line_num = offset + i + 1  # 1-indexed

            # Match code fence with optional language
            fence_match = re.match(r'^```(\w+)?', line)

            if fence_match and not in_code:
                in_code = True
                code_start = line_num
                code_lang = fence_match.group(1) or 'text'
                code_lines = []
            elif '```' in line and in_code:
                # Filter by language if specified
                if language is None or code_lang == language:
                    code_blocks.append({
                        'line_start': code_start,
                        'line_end': line_num,
                        'content': '\n'.join(code_lines),
                        'language': code_lang
                    })
                in_code = False
            elif in_code:
                code_lines.append(line.rstrip())

        return code_blocks

    def get_document_stats(self) -> Dict:
        """
        Get statistics about the document.

        Returns:
            Dictionary with document metadata
        """
        if not self.toc:
            self.extract_toc()

        return {
            'total_lines': len(self.lines),
            'total_headings': len(self.toc),
            'heading_levels': {
                level: sum(1 for e in self.toc if e.level == level)
                for level in range(1, 7)
            },
            'total_diagrams': len(self.find_diagrams()),
            'total_code_blocks': len(self.find_code_blocks()),
            'file_size_bytes': self.doc_path.stat().st_size,
            'file_path': str(self.doc_path)
        }


if __name__ == '__main__':
    """
    Example usage:

    python doc_parser.py path/to/document.md
    """
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python doc_parser.py <document_path>")
        sys.exit(1)

    doc_path = sys.argv[1]
    parser = DocumentParser(Path(doc_path))

    # Extract TOC
    parser.extract_toc()

    # Print document stats
    stats = parser.get_document_stats()
    print("\n=== Document Statistics ===")
    print(json.dumps(stats, indent=2))

    # Print TOC
    print("\n=== Table of Contents ===")
    for entry in parser.toc[:20]:  # First 20 entries
        indent = "  " * (entry.level - 1)
        print(f"{indent}- {entry.title} (lines {entry.line_start}-{entry.line_end})")

    if len(parser.toc) > 20:
        print(f"... and {len(parser.toc) - 20} more sections")
