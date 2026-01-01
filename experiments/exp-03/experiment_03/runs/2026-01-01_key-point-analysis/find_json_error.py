#!/usr/bin/env python3
import json

try:
    with open('requirement_cards.json', 'r') as f:
        content = f.read()
        cards = json.loads(content)
    print("✓ requirement_cards.json is valid!")
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")
    print(f"\nShowing context around error position:")
    with open('requirement_cards.json', 'r') as f:
        content = f.read()

    # Show 200 chars before and after error
    start = max(0, e.pos - 200)
    end = min(len(content), e.pos + 200)

    before = content[start:e.pos]
    after = content[e.pos:end]

    print(f"\n...{before}<<<ERROR>>>{after}...")
    print(f"\nError character: '{content[e.pos]}' (ord={ord(content[e.pos])})")
