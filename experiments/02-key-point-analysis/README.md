# Experiment 02: Key Point Analysis

## Overview

**What**: Implement Key Point Analysis capability for IBM Debater service
**Why**: Test document-driven derivation on medium-complexity capability with multiple input/output formats
**Status**: ✅ Complete (40/40 tests passing)
**Date**: 2026-01-01

## Structure

```
02-key-point-analysis/
├── config/                 # Configuration (prompts, settings)
│   ├── prompts/           # Agent instructions
│   └── requirements.txt   # Python dependencies
├── outputs/               # Generated content (not in git)
│   ├── runs/             # Experiment runs
│   └── reports/          # Analysis reports
└── notes/                # Human documentation
    ├── EXPERIMENT_03_STRATEGY.md
    ├── EXP_03_MANIFESTO.md
    └── ...
```

## Quick Start

```bash
# From experiment directory
python run_experiment.py --project-dir outputs/runs/my-run

# With custom settings
python run_experiment.py \
    --project-dir outputs/runs/my-run \
    --model claude-sonnet-4-5 \
    --max-iterations 10
```

## Pipeline

**3-Agent Pipeline**: SPEC LIBRARIAN → SPEC REVIEWER → CODING AGENT

1. **SPEC LIBRARIAN**: Derives requirements from canonical artifacts (DeepWiki, examples)
2. **SPEC REVIEWER**: Filters tech-specific details to legacy_notes
3. **CODING AGENT**: Implements behavior-only requirements

## Key Metrics

- **40/40 tests passing** (100% success rate)
- **Test Coverage**: Input validation, output formats, error handling, edge cases
- **Implementation Time**: ~3 hours autonomous agent time
- **Code Quality**: Clean separation of concerns, comprehensive error handling

## Capabilities Implemented

### Key Point Analysis (KPA)
- Analyze text and extract key discussion points
- Support for multiple input formats (text, sentences list)
- Multiple output formats (JSON, sentences list, dict)
- Domain filtering (specific domains only)
- Quality control (min/max matches)

### Test Coverage
- Input validation (18 tests)
- Output format handling (12 tests)
- Domain filtering (6 tests)
- Error cases (4 tests)

## Documentation

- **Strategy**: `notes/EXPERIMENT_03_STRATEGY.md` - Experiment design and approach
- **Manifesto**: `notes/EXP_03_MANIFESTO.md` - Core principles and requirements
- **Results**: `outputs/reports/2026-01-01_*` - Analysis and findings
- **Requirements**: `notes/CRITICAL_REQUIREMENTS.md` - Non-negotiable requirements

## Dependencies

See `config/requirements.txt` for Python dependencies. Main requirements:
- claude-code-sdk
- pytest (for testing)

## Related Experiments

- **01-evidence-detection**: Simpler capability, establishes baseline patterns
- **Future experiments**: Will build on patterns established here

## Notes

This experiment uses **shared infrastructure** from `_shared/infrastructure/`:
- No duplicate code across experiments
- Single source of truth for core functionality
- Consistent patterns and behaviors

Last Updated: 2026-01-02
