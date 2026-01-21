#!/usr/bin/env python
"""
FINAL COMPREHENSIVE VERIFICATION
This script performs rigorous end-to-end validation of all calculations
"""
from calculate_score import *

print("="*80)
print("FINAL COMPREHENSIVE VERIFICATION")
print("="*80)

# Parse and map
sections = parse_response_text('response_text.txt')
all_questions = []
for section in sections:
    all_questions.extend(section)

mapping = {}
for q_num in range(1, 45):
    pattern = QUESTION_PATTERNS[q_num]
    for user_q in all_questions:
        if re.search(pattern, user_q['raw_block'], re.IGNORECASE | re.DOTALL):
            mapping[q_num] = user_q
            break

# Manual calculation
total = 0
details = []

for q_num in range(1, 45):
    official = OFFICIAL_ANSWERS[q_num]
    user_q = mapping.get(q_num)
    
    if not user_q:
        score = 0
        user_ans = 'NOT FOUND'
        status = 'Not Found'
    else:
        status = user_q.get('status', '')
        if official['type'] == 'NAT':
            user_ans = user_q.get('answer', 'N/A')
            score = calculate_nat_score(official, user_ans)
        elif official['type'] == 'MSQ':
            user_ans = user_q.get('chosen_options', '--')
            score = calculate_msq_score(official['keys'], user_ans, status)
        else:
            user_ans = user_q.get('chosen_options', '--')
            score = calculate_mcq_score(official['key'], user_ans, status)
    
    total += score
    details.append({
        'q': q_num,
        'type': official['type'],
        'user': user_ans,
        'score': score
    })

# Verify section totals
nat_total = sum(d['score'] for d in details if 1 <= d['q'] <= 8)
msq_total = sum(d['score'] for d in details if 9 <= d['q'] <= 18)
mcq_total = sum(d['score'] for d in details if 19 <= d['q'] <= 44)

print("\nMANUAL CALCULATION RESULTS:")
print(f"NAT (Q1-8):    {nat_total:6.1f}")
print(f"MSQ (Q9-18):   {msq_total:6.1f}")
print(f"MCQ (Q19-44):  {mcq_total:6.1f}")
print(f"TOTAL:         {total:6.1f}")

# Read the score summary file
with open('score_summary.txt', 'r') as f:
    summary_lines = f.readlines()

# Extract reported totals
reported_nat = None
reported_msq = None
reported_mcq = None
reported_total = None

for line in summary_lines:
    if 'NAT (Max: 32 marks)' in line:
        idx = summary_lines.index(line)
        score_line = summary_lines[idx+1]
        reported_nat = float(score_line.split(':')[1].strip())
    elif 'MSQ (Max: 40 marks)' in line:
        idx = summary_lines.index(line)
        score_line = summary_lines[idx+1]
        reported_msq = float(score_line.split(':')[1].strip())
    elif 'MCQ (Max: 78 marks)' in line:
        idx = summary_lines.index(line)
        score_line = summary_lines[idx+1]
        reported_mcq = float(score_line.split(':')[1].strip())
    elif 'TOTAL PART A SCORE:' in line:
        reported_total = float(line.split(':')[1].strip())

print("\nREPORTED IN score_summary.txt:")
print(f"NAT (Q1-8):    {reported_nat:6.1f}")
print(f"MSQ (Q9-18):   {reported_msq:6.1f}")
print(f"MCQ (Q19-44):  {reported_mcq:6.1f}")
print(f"TOTAL:         {reported_total:6.1f}")

print("\n" + "="*80)
print("VERIFICATION:")
print("="*80)

all_match = True
if abs(nat_total - reported_nat) < 0.01:
    print("✓ NAT scores match")
else:
    print(f"✗ NAT scores DO NOT match: {nat_total} vs {reported_nat}")
    all_match = False

if abs(msq_total - reported_msq) < 0.01:
    print("✓ MSQ scores match")
else:
    print(f"✗ MSQ scores DO NOT match: {msq_total} vs {reported_msq}")
    all_match = False

if abs(mcq_total - reported_mcq) < 0.01:
    print("✓ MCQ scores match")
else:
    print(f"✗ MCQ scores DO NOT match: {mcq_total} vs {reported_mcq}")
    all_match = False

if abs(total - reported_total) < 0.01:
    print("✓ TOTAL scores match")
else:
    print(f"✗ TOTAL scores DO NOT match: {total} vs {reported_total}")
    all_match = False

print("\n" + "="*80)
if all_match:
    print("✓✓✓ ALL CALCULATIONS VERIFIED CORRECT ✓✓✓")
else:
    print("✗✗✗ DISCREPANCIES FOUND - REVIEW NEEDED ✗✗✗")
print("="*80)

# Show some critical questions for spot check
print("\nSPOT CHECK OF CRITICAL QUESTIONS:")
critical = [1, 3, 8, 9, 10, 11, 12, 13, 21, 28, 33, 41]
for q in critical:
    d = next(x for x in details if x['q'] == q)
    print(f"  Q{q:2} ({d['type']:3}): User='{str(d['user']):10}' Score={d['score']:5.1f}")
