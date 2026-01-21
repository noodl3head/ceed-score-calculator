#!/usr/bin/env python
# MSQ edge case verification
def calculate_msq_score(correct_keys, chosen_keys, status=''):
    if status == 'Not Answered' or not chosen_keys or chosen_keys == '--':
        return 0
    
    chosen_raw = chosen_keys.split(',')
    map_dict = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
    chosen = {map_dict.get(c.strip(), c.strip()) for c in chosen_raw if c.strip()}
    
    if not chosen: return 0
    correct = set(correct_keys)
    
    if not chosen.issubset(correct): return -1
    if chosen == correct: return 4
    if len(correct) == 4 and len(chosen) == 3: return 3
    if len(correct) >= 3 and len(chosen) == 2: return 2
    if len(correct) >= 2 and len(chosen) == 1: return 1
    return -1

print('MSQ EDGE CASE VERIFICATION:')
print('='*80)

test_cases = [
    (['A','B','C'], '1,2', 2, 'Q9: 3 correct options, chose 2 correct'),
    (['C','D'], '3,4', 4, 'Q10: All correct'),
    (['A','D'], '1', 1, 'Q11: 2 correct options, chose 1 correct'),
    (['B','D'], '2,4', 4, 'Q12: All correct'),
    (['A','C'], '1,3,4', -1, 'Q13: Chose one wrong option D'),
    (['A','B','C'], '1,3,4', -1, 'Q16: 3 correct, chose 2 correct + 1 wrong'),
    (['D'], '2,3', -1, 'Q17: 1 correct, chose 2 wrong'),
]

all_pass = True
for correct, chosen, expected, desc in test_cases:
    result = calculate_msq_score(correct, chosen)
    status = 'PASS' if result == expected else 'FAIL'
    if result != expected:
        all_pass = False
    print(f'{status}: {desc}')
    print(f'  Correct={correct}, Chosen={chosen} -> Score={result} (expected {expected})')
    print()

if all_pass:
    print('='*80)
    print('ALL MSQ TESTS PASSED!')
    print('='*80)
else:
    print('='*80)
    print('SOME TESTS FAILED - CHECK LOGIC!')
    print('='*80)
