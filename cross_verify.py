#!/usr/bin/env python
# Cross-verification script
import sys
from calculate_score import *

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

# Check specific critical questions
print("="*80)
print("CROSS-VERIFICATION OF CRITICAL QUESTIONS")
print("="*80)

test_qs = [1, 3, 8, 9, 10, 11, 12, 13, 21, 22, 28, 33]
for q_num in test_qs:
    official = OFFICIAL_ANSWERS[q_num]
    user_q = mapping.get(q_num)
    
    if user_q:
        if official['type'] == 'NAT':
            user_ans = user_q['answer']
            correct = official.get('range', official.get('value'))
            score = calculate_nat_score(official, user_ans)
        elif official['type'] == 'MSQ':
            user_ans = user_q['chosen_options']
            correct = ','.join(official['keys'])
            score = calculate_msq_score(official['keys'], user_ans, user_q['status'])
        elif official['type'] == 'MCQ':
            user_ans = user_q['chosen_options']
            correct = official['key']
            score = calculate_mcq_score(official['key'], user_ans, user_q['status'])
        
        print(f"Q{q_num:2} ({official['type']:3}): User='{user_ans:10}' Correct={str(correct):15} Score={score:5}")
    else:
        print(f"Q{q_num:2}: NOT FOUND IN MAPPING")

# Calculate total and verify
print("\n" + "="*80)
print("SECTION TOTALS VERIFICATION")
print("="*80)

nat_score = sum(calculate_nat_score(OFFICIAL_ANSWERS[i], mapping.get(i, {}).get('answer')) 
                for i in range(1, 9) if mapping.get(i))

msq_score = sum(calculate_msq_score(OFFICIAL_ANSWERS[i]['keys'], 
                                     mapping.get(i, {}).get('chosen_options', '--'),
                                     mapping.get(i, {}).get('status', ''))
                for i in range(9, 19) if mapping.get(i))

mcq_score = sum(calculate_mcq_score(OFFICIAL_ANSWERS[i]['key'],
                                     mapping.get(i, {}).get('chosen_options', '--'),
                                     mapping.get(i, {}).get('status', ''))
                for i in range(19, 45) if mapping.get(i))

print(f"NAT (Q1-8):    {nat_score:6.1f} / 32")
print(f"MSQ (Q9-18):   {msq_score:6.1f} / 40")
print(f"MCQ (Q19-44):  {mcq_score:6.1f} / 78")
print(f"TOTAL:         {nat_score + msq_score + mcq_score:6.1f} / 150")

# Detailed breakdown by score type
print("\n" + "="*80)
print("DETAILED BREAKDOWN BY QUESTION")
print("="*80)

for section_name, q_range in [("NAT", range(1,9)), ("MSQ", range(9,19)), ("MCQ", range(19,45))]:
    print(f"\n{section_name} Section:")
    correct = wrong = unattempted = 0
    neg_score = 0
    
    for q_num in q_range:
        user_q = mapping.get(q_num)
        if not user_q:
            unattempted += 1
            continue
            
        official = OFFICIAL_ANSWERS[q_num]
        
        if official['type'] == 'NAT':
            score = calculate_nat_score(official, user_q.get('answer'))
        elif official['type'] == 'MSQ':
            score = calculate_msq_score(official['keys'], user_q.get('chosen_options', '--'), user_q.get('status', ''))
        else:
            score = calculate_mcq_score(official['key'], user_q.get('chosen_options', '--'), user_q.get('status', ''))
        
        if score > 0:
            correct += 1
        elif score < 0:
            wrong += 1
            neg_score += score
        else:
            unattempted += 1
    
    print(f"  Correct: {correct}, Wrong: {wrong}, Unattempted: {unattempted}, Negative: {neg_score}")
