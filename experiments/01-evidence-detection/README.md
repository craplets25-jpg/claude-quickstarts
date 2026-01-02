# Experiment 01: Evidence Detection

## Overview

**What**: Implement Evidence Detection capability for IBM Debater service
**Why**: Establish baseline patterns for document-driven derivation with simpler capability
**Status**: ✅ Complete (18/18 tests passing)
**Date**: 2025-12-31

## Structure

```
01-evidence-detection/
├── config/                 # Configuration (prompts, settings)
│   ├── prompts/           # Agent instructions
│   └── requirements.txt   # Python dependencies
├── outputs/               # Generated content (not in git)
│   ├── runs/             # Experiment runs
│   └── reports/          # Analysis reports
└── notes/                # Human documentation
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

- **18/18 tests passing** (100% success rate)
- **Test Coverage**: Input validation, output formats, error handling
- **Implementation Time**: ~2 hours autonomous agent time
- **Code Quality**: Clean separation of concerns, comprehensive error handling

## Capabilities Implemented

### Evidence Detection
- Detect evidence for/against given topics in text
- Support for multiple input formats (text, sentences list)
- Support for multiple topics
- Motion/topic validation
- PRO/CON classification

### Test Coverage
- Input validation (8 tests)
- Output format handling (6 tests)
- Error cases (4 tests)

## Documentation

- **Strategy**: `notes/EXPERIMENT_02_STRATEGY.md` - Experiment design and approach
- **Manifesto**: `notes/EXP_02_MANIFESTO.md` - Core principles and requirements
- **Results**: `outputs/reports/2025-12-31_*` - Analysis and findings

## Dependencies

See `config/requirements.txt` for Python dependencies. Main requirements:
- claude-code-sdk
- pytest (for testing)

## Related Experiments

- **02-key-point-analysis**: Builds on patterns established here, more complex capability

## Notes

This experiment uses **shared infrastructure** from `_shared/infrastructure/`:
- No duplicate code across experiments
- Single source of truth for core functionality
- Consistent patterns and behaviors

This experiment establishes the **baseline patterns** that subsequent experiments build upon:
- Document-driven requirement derivation
- 3-agent pipeline (Librarian → Reviewer → Coder)
- Test-driven development approach
- Isolated git repositories per run

Last Updated: 2026-01-02
