#!/usr/bin/env python3
"""
Split Large Documentation Files into Logical Sections
======================================================

This script splits large markdown files into smaller sections based on
header structure, making them easier for agents to read without hitting
token limits.

Usage:
    python scripts/split_large_docs.py <input_file> [options]

Examples:
    # Split by H2 headers (##)
    python scripts/split_large_docs.py deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md

    # Split by H3 headers (###)
    python scripts/split_large_docs.py deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md --level 3

    # Custom output directory
    python scripts/split_large_docs.py deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md --output-dir split-docs/

Features:
- Splits on H2 or H3 headers (configurable)
- Preserves all content under each section
- Creates index file mapping sections
- Generates section summaries
- Handles nested headers properly
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple


class MarkdownSection:
    """Represents a logical section of a markdown document."""

    def __init__(self, header: str, level: int, start_line: int):
        self.header = header
        self.level = level
        self.start_line = start_line
        self.end_line = None
        self.content: List[str] = []
        self.subsections: List['MarkdownSection'] = []

    def add_line(self, line: str):
        """Add a line of content to this section."""
        self.content.append(line)

    def get_slug(self) -> str:
        """Generate a URL-safe slug from the header."""
        # Remove markdown formatting
        slug = re.sub(r'[#*`\[\]()]', '', self.header)
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^a-z0-9]+', '-', slug.lower())
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        # Limit length
        return slug[:80]

    def get_content_preview(self, max_chars: int = 200) -> str:
        """Get a preview of the section content."""
        text = '\n'.join(self.content)
        # Remove extra whitespace
        text = ' '.join(text.split())
        if len(text) > max_chars:
            return text[:max_chars] + '...'
        return text

    def count_lines(self) -> int:
        """Count total lines in this section."""
        return len(self.content)

    def count_tokens_estimate(self) -> int:
        """Estimate token count (rough approximation: ~4 chars per token)."""
        total_chars = sum(len(line) for line in self.content)
        return total_chars // 4


def parse_markdown_file(file_path: Path, split_level: int = 2) -> List[MarkdownSection]:
    """
    Parse a markdown file and split it into logical sections.

    Args:
        file_path: Path to the markdown file
        split_level: Header level to split on (2 for ##, 3 for ###)

    Returns:
        List of MarkdownSection objects
    """
    sections = []
    current_section = None
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, start=1):
        match = header_pattern.match(line.rstrip())

        if match:
            level = len(match.group(1))  # Count # symbols
            header_text = match.group(2)

            # If this is a split-level header, start a new section
            if level == split_level:
                if current_section:
                    current_section.end_line = line_num - 1
                    sections.append(current_section)

                current_section = MarkdownSection(header_text, level, line_num)
                current_section.add_line(line)

            # If we're in a section, add the line
            elif current_section:
                current_section.add_line(line)

            # If no section yet (headers before first split-level), skip or save as preamble
            else:
                # Could handle preamble here if needed
                pass

        else:
            # Regular content line
            if current_section:
                current_section.add_line(line)

    # Don't forget the last section
    if current_section:
        current_section.end_line = len(lines)
        sections.append(current_section)

    return sections


def write_section_file(section: MarkdownSection, output_dir: Path, index: int,
                       source_filename: str) -> Path:
    """
    Write a section to a separate file.

    Args:
        section: The section to write
        output_dir: Directory to write to
        index: Section index (for ordering)
        source_filename: Original filename (for reference)

    Returns:
        Path to the created file
    """
    slug = section.get_slug()
    filename = f"{index:03d}_{slug}.md"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header with metadata
        f.write(f"<!-- Source: {source_filename} -->\n")
        f.write(f"<!-- Section: {section.header} -->\n")
        f.write(f"<!-- Lines: {section.start_line}-{section.end_line} -->\n\n")

        # Write content
        f.write(''.join(section.content))

    return filepath


def create_index_file(sections: List[MarkdownSection], output_dir: Path,
                     source_filename: str, split_level: int) -> Path:
    """
    Create an index file listing all sections.

    Args:
        sections: List of all sections
        output_dir: Directory containing the sections
        source_filename: Original filename
        split_level: Header level that was split on

    Returns:
        Path to the index file
    """
    index_path = output_dir / "INDEX.md"

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f"# Index: {source_filename}\n\n")
        f.write(f"Split on: H{split_level} headers\n")
        f.write(f"Total sections: {len(sections)}\n\n")
        f.write("---\n\n")

        total_lines = 0
        total_tokens = 0

        for i, section in enumerate(sections, start=1):
            slug = section.get_slug()
            filename = f"{i:03d}_{slug}.md"
            lines = section.count_lines()
            tokens = section.count_tokens_estimate()
            preview = section.get_content_preview(150)

            total_lines += lines
            total_tokens += tokens

            f.write(f"## {i}. {section.header}\n\n")
            f.write(f"**File**: `{filename}`  \n")
            f.write(f"**Lines**: {section.start_line}-{section.end_line} ({lines} lines)  \n")
            f.write(f"**Est. Tokens**: ~{tokens:,}  \n")
            f.write(f"**Preview**: {preview}\n\n")
            f.write("---\n\n")

        # Summary at the end
        f.write("\n## Summary\n\n")
        f.write(f"- **Total sections**: {len(sections)}\n")
        f.write(f"- **Total lines**: {total_lines:,}\n")
        f.write(f"- **Est. total tokens**: ~{total_tokens:,}\n")
        f.write(f"- **Avg tokens per section**: ~{total_tokens // len(sections):,}\n")

    return index_path


def split_document(input_file: Path, output_dir: Path, split_level: int = 2) -> Dict:
    """
    Split a large markdown document into logical sections.

    Args:
        input_file: Path to the input markdown file
        output_dir: Directory to write split files to
        split_level: Header level to split on (2 for ##, 3 for ###)

    Returns:
        Dictionary with statistics about the split
    """
    print(f"Reading: {input_file}")
    print(f"Split level: H{split_level}")
    print(f"Output directory: {output_dir}")
    print()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse the document
    print("Parsing document...")
    sections = parse_markdown_file(input_file, split_level)
    print(f"Found {len(sections)} sections")
    print()

    # Write each section
    print("Writing section files...")
    written_files = []
    for i, section in enumerate(sections, start=1):
        filepath = write_section_file(section, output_dir, i, input_file.name)
        written_files.append(filepath)
        tokens = section.count_tokens_estimate()
        print(f"  [{i:03d}] {section.header}")
        print(f"        File: {filepath.name}")
        print(f"        Lines: {section.count_lines()}, Est. tokens: ~{tokens:,}")

    print()

    # Create index
    print("Creating index file...")
    index_path = create_index_file(sections, output_dir, input_file.name, split_level)
    print(f"Index created: {index_path}")
    print()

    # Statistics
    total_tokens = sum(s.count_tokens_estimate() for s in sections)
    avg_tokens = total_tokens // len(sections)
    max_tokens = max(s.count_tokens_estimate() for s in sections)

    stats = {
        'sections': len(sections),
        'total_tokens': total_tokens,
        'avg_tokens': avg_tokens,
        'max_tokens': max_tokens,
        'output_dir': str(output_dir),
        'index_file': str(index_path),
        'files': [str(f) for f in written_files]
    }

    # Print summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Sections created: {len(sections)}")
    print(f"Total est. tokens: ~{total_tokens:,}")
    print(f"Average per section: ~{avg_tokens:,} tokens")
    print(f"Largest section: ~{max_tokens:,} tokens")
    print(f"Output directory: {output_dir}")
    print()

    if max_tokens > 25000:
        print("⚠️  WARNING: Some sections still exceed 25,000 tokens!")
        print("    Consider splitting at a deeper level (H3 instead of H2)")
    else:
        print("✅ All sections are within the 25,000 token limit")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Split large markdown files into logical sections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split DeepWiki by H2 headers
  python scripts/split_large_docs.py deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md

  # Split by H3 headers instead
  python scripts/split_large_docs.py deep-wiki-spec-files/debater-early-access-program-sdk-Deepwiki.md --level 3

  # Custom output directory
  python scripts/split_large_docs.py input.md --output-dir my-split-docs/
        """
    )

    parser.add_argument(
        'input_file',
        type=Path,
        help='Input markdown file to split'
    )

    parser.add_argument(
        '--level',
        type=int,
        default=2,
        choices=[2, 3, 4],
        help='Header level to split on (2=##, 3=###, 4=####). Default: 2'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Output directory (default: <input_file>-sections/)'
    )

    args = parser.parse_args()

    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file not found: {args.input_file}")
        return 1

    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = args.input_file.parent / f"{args.input_file.stem}-sections"

    # Split the document
    try:
        stats = split_document(args.input_file, output_dir, args.level)
        print()
        print(f"✅ Successfully split {args.input_file.name} into {stats['sections']} sections")
        print(f"📁 Output: {output_dir}")
        print(f"📄 Index: {stats['index_file']}")
        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
