# Debater SDK - Architecture Scaffold

## ⚠️ THIS IS NOT THE SPECIFICATION ⚠️

**This scaffold defines STRUCTURE only.**
**Requirements come from DeepWiki.**

Read ARCHITECTURE.md, then read DeepWiki.

## What's Here

- `ARCHITECTURE.md` - Architecture pattern (MUST follow)
- `base.py` - Abstract base (DO NOT modify)
- `sdk.py` - Factory (DO NOT modify)
- `services/*.py` - Stubs (IMPLEMENT based on DeepWiki)

## Implementation Priorities

- **P0:** ArgumentQualityService
- **P1:** EvidenceDetection, ClaimDetection, ProCon
- **P2:** Clustering, TermWikifier

## Critical Rule

Scaffold = architecture constraint
DeepWiki = requirements source

DO NOT implement based on scaffold comments.
DO read DeepWiki and derive requirements.
