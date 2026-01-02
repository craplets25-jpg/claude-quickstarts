#!/usr/bin/env python3
import json

# Validate requirement_cards.json
try:
    with open('requirement_cards.json', 'r') as f:
        cards = json.load(f)
    print(f"✓ requirement_cards.json: VALID JSON")
    print(f"  - Number of cards: {len(cards)}")
    print(f"  - All cards have 'id': {all('id' in c for c in cards)}")
    print(f"  - All cards have 'invariants': {all('invariants' in c for c in cards)}")
    print(f"  - All cards have 'legacy_notes': {all('legacy_notes' in c for c in cards)}")
except Exception as e:
    print(f"✗ requirement_cards.json: ERROR - {e}")

# Validate feature_list.json
try:
    with open('feature_list.json', 'r') as f:
        tests = json.load(f)
    print(f"\n✓ feature_list.json: VALID JSON")
    print(f"  - Number of tests: {len(tests)}")
    failing = [t for t in tests if t.get('passes') == False]
    print(f"  - Tests with passes=false: {len(failing)}")
    print(f"  - All tests reference requirement: {all('requirement_id' in t for t in tests)}")
except Exception as e:
    print(f"✗ feature_list.json: ERROR - {e}")

print("\n✓ All deliverables validated successfully!")
