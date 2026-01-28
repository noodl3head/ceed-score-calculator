#!/usr/bin/env python
"""
Compare current OFFICIAL_ANSWERS with the new answer key PDF
"""

# New answer key from CEED_2026_Answer_Key.pdf
NEW_ANSWER_KEY = {
    # Section I: NAT
    1: {"type": "NAT", "range": [6.0, 6.5]},
    2: {"type": "NAT", "range": [126.0, 128.0]},
    3: {"type": "NAT", "range": [24.0, 25.5]},
    4: {"type": "NAT", "value": 19.0},  # CHANGED from 18.0
    5: {"type": "NAT", "value": 19.0},
    6: {"type": "NAT", "value": 4.0},
    7: {"type": "NAT", "value": 2.0},
    8: {"type": "NAT", "value": 15.0},
    # Section II: MSQ
    9: {"type": "MSQ", "keys": ["A", "B", "C"]},
    10: {"type": "MSQ", "keys": ["C", "D"]},
    11: {"type": "MSQ", "keys": ["A", "D"]},
    12: {"type": "MSQ", "keys": ["B", "D"]},
    13: {"type": "MSQ", "keys": ["A", "C"]},
    14: {"type": "MSQ", "keys": ["A", "B", "C"]},
    15: {"type": "MSQ", "keys": ["A", "B", "C"]},
    16: {"type": "MSQ", "keys": ["A", "B", "C"]},
    17: {"type": "MSQ", "keys": ["D"]},
    18: {"type": "MSQ", "keys": ["B", "D"]},
    # Section III: MCQ
    19: {"type": "MCQ", "key": "A"},
    20: {"type": "MCQ", "key": "B"},
    21: {"type": "MCQ", "key": "C"},
    22: {"type": "MCQ", "key": "D"},
    23: {"type": "MCQ", "key": "C"},
    24: {"type": "MCQ", "key": "D"},
    25: {"type": "MCQ", "key": "D"},
    26: {"type": "MCQ", "key": "C"},
    27: {"type": "MCQ", "key": "D"},
    28: {"type": "MCQ", "key": "D"},
    29: {"type": "MCQ", "key": "B"},
    30: {"type": "MCQ", "key": "D"},
    31: {"type": "MCQ", "key": "A"},
    32: {"type": "MCQ", "key": "B"},
    33: {"type": "MCQ", "key": "D"},
    34: {"type": "MCQ", "key": "B"},
    35: {"type": "MCQ", "key": "B"},
    36: {"type": "MCQ", "key": "B"},
    37: {"type": "MCQ", "key": "D"},
    38: {"type": "MCQ", "key": "D"},
    39: {"type": "MCQ", "key": "B"},
    40: {"type": "MCQ", "key": "A"},
    41: {"type": "MCQ", "key": "C"},
    42: {"type": "MCQ", "key": "B"},  # CHANGED from C
    43: {"type": "MCQ", "key": "B"},
    44: {"type": "MCQ", "key": "B"},
}

# Load old answer key
from calculate_score import OFFICIAL_ANSWERS as OLD_ANSWER_KEY

print("="*80)
print("COMPARING OLD vs NEW ANSWER KEY")
print("="*80)

differences = []
for q_num in range(1, 45):
    old = OLD_ANSWER_KEY.get(q_num)
    new = NEW_ANSWER_KEY.get(q_num)
    
    if old != new:
        differences.append((q_num, old, new))
        print(f"\nQ{q_num} CHANGED:")
        print(f"  OLD: {old}")
        print(f"  NEW: {new}")

print("\n" + "="*80)
if not differences:
    print("✓ No differences found")
else:
    print(f"✗ Found {len(differences)} difference(s)")
    print("\nSummary of changes:")
    for q_num, old, new in differences:
        if old['type'] == 'NAT':
            old_val = old.get('value') or old.get('range')
            new_val = new.get('value') or new.get('range')
            print(f"  Q{q_num} (NAT): {old_val} → {new_val}")
        elif old['type'] == 'MCQ':
            print(f"  Q{q_num} (MCQ): {old['key']} → {new['key']}")
        elif old['type'] == 'MSQ':
            print(f"  Q{q_num} (MSQ): {old['keys']} → {new['keys']}")
print("="*80)
