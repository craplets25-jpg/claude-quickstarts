import json

# Validate requirement_cards.json
with open('requirement_cards.json', 'r') as f:
    cards = json.load(f)
    print(f"requirement_cards.json: VALID - {len(cards)} cards")

# Validate feature_list.json
with open('feature_list.json', 'r') as f:
    tests = json.load(f)
    print(f"feature_list.json: VALID - {len(tests)} tests")

print("All JSON files are valid!")
