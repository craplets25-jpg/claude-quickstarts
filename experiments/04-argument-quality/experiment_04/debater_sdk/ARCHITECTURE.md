# Debater SDK Architecture Constraint

## ⚠️ CRITICAL WARNING ⚠️

**THIS SCAFFOLD IS NOT THE SPECIFICATION.**

This file defines the ARCHITECTURE PATTERN you must follow.
The actual REQUIREMENTS come from DeepWiki.

**YOU MUST:**
1. Read DeepWiki to derive requirements
2. Follow this architecture pattern when implementing
3. Implement behavior described in DeepWiki, not assumptions from this scaffold

**DO NOT:**
- Use this file as a requirements source
- Assume behavior from scaffold comments
- Skip reading DeepWiki

---

## What You're Building

**We are implementing SERVICE LOGIC, not an API client.**

Reference system: `Client → HTTP → External Service (ML)`
Our system: `Service → LLM (Claude) → Results`

You're recreating what's INSIDE the external service.

---

## Required Architecture Pattern

**You MUST follow this structure (non-negotiable):**

```
DebaterSDK (Factory)
    ↓
BaseService (Abstract)
    ↓
ConcreteServices (ArgumentQuality, Evidence, etc.)
```

### 1. Factory Pattern

Single entry point creates all services:
```python
sdk = DebaterSDK(api_key="...")
service = sdk.get_argument_quality_service()
```

### 2. Abstract Base Class

BaseService provides:
- `run()` - Public API
- `_validate_inputs()` - Input validation
- `_call_llm()` - LLM helper
- Logging/timing

Subclasses implement:
- `_process_batch()` - Core capability logic

### 3. Service Separation

One class per capability in `services/`:
- ArgumentQualityService (P0)
- EvidenceDetectionService (P1)
- ClaimDetectionService (P1)
- ProConService (P1)
- ClusteringService (P2)
- TermWikifierService (P2)

---

## What to Extract from DeepWiki

**Architecture (from diagrams/structure):**
- Class relationships
- Data flow patterns
- Input/output shapes
- Error conditions

**NOT Implementation Details:**
- HTTP endpoints
- Timeouts
- Vendor-specific error text
- Internal method names

---

## Remember

This scaffold = STRUCTURE constraint
DeepWiki = BEHAVIOR requirements

Read DeepWiki. Derive requirements. Then implement.
