# Experiment NN: [Capability Name]

## Overview

**What**: [Brief description of what capability is being implemented]
**Why**: [Why this experiment matters - what question it answers]
**Status**: 🔄 In Progress / ✅ Complete / ❌ Failed
**Date**: YYYY-MM-DD

## Structure

```
NN-capability-name/
├── config/                 # Configuration (prompts, settings)
│   ├── prompts/           # Agent instructions
│   └── requirements.txt   # Python dependencies
├── outputs/               # Generated content
│   ├── runs/             # Experiment runs
│   └── reports/          # Analysis reports
└── notes/                # Human documentation
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

- **Tests**: X/Y passing (Z% success rate)
- **Test Coverage**: [Describe what's covered]
- **Implementation Time**: [Estimate or actual]
- **Code Quality**: [Assessment]

## Capabilities Implemented

### [Capability Name]
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Test Coverage
- [Test category 1] (N tests)
- [Test category 2] (N tests)
- [Test category 3] (N tests)

## Documentation

- **Strategy**: `notes/EXPERIMENT_STRATEGY.md` - Experiment design and approach
- **Results**: `outputs/reports/YYYY-MM-DD_*` - Analysis and findings
- **Requirements**: `notes/CRITICAL_REQUIREMENTS.md` - Non-negotiable requirements (if any)

## Dependencies

See `config/requirements.txt` for Python dependencies. Main requirements:
- claude-code-sdk
- pytest (for testing)
- [Other dependencies]

## Related Experiments

- **Previous**: [Link to related prior experiment]
- **Next**: [Link to planned follow-up]

## Notes

This experiment uses **shared infrastructure** from `_shared/infrastructure/`:
- No duplicate code across experiments
- Single source of truth for core functionality
- Consistent patterns and behaviors

[Any experiment-specific notes or lessons learned]

Last Updated: YYYY-MM-DD
