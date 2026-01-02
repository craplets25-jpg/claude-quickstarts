#!/usr/bin/env python3
"""
Section Extractor for DeepWiki

Extracts specific sections from DeepWiki by line range or section name.
Returns only relevant content with metadata, not entire document.

Usage:
    # Extract by line range:
    python section_extractor.py <deepwiki_path> --lines 119-164

    # Extract by section name:
    python section_extractor.py <deepwiki_path> --section "Key Point Analysis"
"""

from pathlib import Path
import json
import sys
import argparse
from typing import Dict, Optional
from doc_parser import DocumentParser


class SectionExtractor:
    """Extractor for DeepWiki sections"""

    def __init__(self, deepwiki_path: str):
        """
        Initialize extractor with DeepWiki path.

        Args:
            deepwiki_path: Path to DeepWiki markdown file
        """
        self.parser = DocumentParser(Path(deepwiki_path))
        self.parser.extract_toc()

    def extract_by_lines(self, line_start: int, line_end: int) -> Dict:
        """
        Extract section content by line range.

        Args:
            line_start: Starting line (1-indexed)
            line_end: Ending line (1-indexed)

        Returns:
            Dictionary with section content and metadata
        """
        content = self.parser.get_section_by_line_range(line_start, line_end)

        # Analyze content
        diagrams = self.parser.find_diagrams(content)
        code_blocks = self.parser.find_code_blocks(content)

        return {
            'line_start': line_start,
            'line_end': line_end,
            'line_count': line_end - line_start + 1,
            'content': content,
            'has_diagrams': len(diagrams) > 0,
            'diagrams': diagrams,
            'has_code_blocks': len(code_blocks) > 0,
            'code_blocks': code_blocks,
            'metadata': {
                'diagram_count': len(diagrams),
                'code_block_count': len(code_blocks),
                'diagram_types': [d['type'] for d in diagrams],
                'code_languages': list(set(b['language'] for b in code_blocks))
            }
        }

    def extract_by_name(self, section_name: str, fuzzy: bool = True) -> Optional[Dict]:
        """
        Extract section by name.

        Args:
            section_name: Section title to search for
            fuzzy: If True, do fuzzy matching (case-insensitive, partial)

        Returns:
            Dictionary with section content and metadata, or None if not found
        """
        # Search TOC for matching section
        matching_entry = None

        if fuzzy:
            section_lower = section_name.lower()
            for entry in self.parser.toc:
                if section_lower in entry.title.lower():
                    matching_entry = entry
                    break
        else:
            for entry in self.parser.toc:
                if entry.title == section_name:
                    matching_entry = entry
                    break

        if not matching_entry:
            return None

        # Extract content
        content = self.parser.get_section_content(matching_entry)

        # Analyze content
        diagrams = self.parser.find_diagrams(content)
        code_blocks = self.parser.find_code_blocks(content)

        return {
            'section_title': matching_entry.title,
            'heading_level': matching_entry.level,
            'line_start': matching_entry.line_start,
            'line_end': matching_entry.line_end,
            'line_count': matching_entry.line_end - matching_entry.line_start if matching_entry.line_end else 0,
            'content': content,
            'has_diagrams': len(diagrams) > 0,
            'diagrams': diagrams,
            'has_code_blocks': len(code_blocks) > 0,
            'code_blocks': code_blocks,
            'metadata': {
                'diagram_count': len(diagrams),
                'code_block_count': len(code_blocks),
                'diagram_types': [d['type'] for d in diagrams],
                'code_languages': list(set(b['language'] for b in code_blocks))
            }
        }

    def list_sections_matching(self, keyword: str) -> list:
        """
        List all sections matching a keyword.

        Args:
            keyword: Keyword to search for

        Returns:
            List of section summaries
        """
        matches = self.parser.filter_toc_by_keywords([keyword])

        return [
            {
                'title': entry.title,
                'level': entry.level,
                'line_start': entry.line_start,
                'line_end': entry.line_end,
                'size_lines': entry.line_end - entry.line_start if entry.line_end else 0
            }
            for entry in matches
        ]


def main():
    """Main entry point for section extractor"""
    parser = argparse.ArgumentParser(
        description='Extract sections from DeepWiki',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract by line range
  python section_extractor.py deepwiki.md --lines 119-164

  # Extract by section name
  python section_extractor.py deepwiki.md --section "Key Point Analysis"

  # List sections matching keyword
  python section_extractor.py deepwiki.md --list "analysis"
        """
    )

    parser.add_argument('deepwiki_path', help='Path to DeepWiki markdown file')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--lines', help='Line range (e.g., 119-164)')
    group.add_argument('--section', help='Section name to extract')
    group.add_argument('--list', help='List sections matching keyword')

    parser.add_argument('--no-content', action='store_true',
                       help='Return metadata only, not content')

    args = parser.parse_args()

    # Verify file exists
    if not Path(args.deepwiki_path).exists():
        print(f"Error: File not found: {args.deepwiki_path}", file=sys.stderr)
        sys.exit(1)

    # Create extractor
    extractor = SectionExtractor(args.deepwiki_path)

    # Execute command
    result = None

    if args.lines:
        # Parse line range
        try:
            line_start, line_end = map(int, args.lines.split('-'))
        except ValueError:
            print(f"Error: Invalid line range format: {args.lines}", file=sys.stderr)
            print("Use format: START-END (e.g., 119-164)", file=sys.stderr)
            sys.exit(1)

        result = extractor.extract_by_lines(line_start, line_end)

    elif args.section:
        result = extractor.extract_by_name(args.section, fuzzy=True)
        if result is None:
            print(f"Error: Section not found: {args.section}", file=sys.stderr)
            sys.exit(1)

    elif args.list:
        result = {
            'keyword': args.list,
            'matches': extractor.list_sections_matching(args.list)
        }

    # Remove content if requested
    if args.no_content and 'content' in result:
        result['content_length'] = len(result['content'])
        del result['content']

    # Output JSON
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
