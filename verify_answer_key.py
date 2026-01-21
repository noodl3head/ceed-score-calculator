#!/usr/bin/env python
"""
Verify answer key in code matches official PDF exactly
"""
from pypdf import PdfReader
import re

print("="*80)
print("VERIFYING ANSWER KEY AGAINST OFFICIAL PDF")
print("="*80)

# Read official answer key PDF
reader = PdfReader("CEED2026_draftAnswerkey.pdf")
pdf_text = reader.pages[0].extract_text()

# Parse official answers
official_pdf = {}

# NAT section
nat_section = re.search(r'SECTION – I \(NAT\)(.*?)SECTION – II', pdf_text, re.DOTALL)
if nat_section:
    lines = nat_section.group(1).strip().split('\n')
    for line in lines:
        matches = re.findall(r'(\d+)\s+([\d.]+(?:\s+to\s+[\d.]+)?)', line)
        for q, ans in matches:
            if 'to' in ans:
                parts = ans.split(' to ')
                official_pdf[int(q)] = ('NAT', 'range', [float(parts[0]), float(parts[1])])
            else:
                official_pdf[int(q)] = ('NAT', 'value', float(ans))

# MSQ section
msq_section = re.search(r'SECTION – II \(MSQ\)(.*?)SECTION – III', pdf_text, re.DOTALL)
if msq_section:
    text = msq_section.group(1)
    matches = re.findall(r'(\d+)\s+([A-D,\s]+?)(?=\d+\s+[A-D]|\Z)', text)
    for q, ans in matches:
        q_num = int(q)
        keys = [x.strip() for x in ans.replace(',', ' ').split() if x.strip() in ['A','B','C','D']]
        official_pdf[q_num] = ('MSQ', 'keys', keys)

# MCQ section
mcq_section = re.search(r'SECTION – III \(MCQ\)(.*?)$', pdf_text, re.DOTALL)
if mcq_section:
    text = mcq_section.group(1)
    matches = re.findall(r'(\d+)\s+([A-D])\s', text)
    for q, ans in matches:
        official_pdf[int(q)] = ('MCQ', 'key', ans)

# Load our answer key
from calculate_score import OFFICIAL_ANSWERS

# Compare
print("\nCOMPARING ANSWER KEYS:")
print("-"*80)

all_match = True
for q_num in range(1, 45):
    code_ans = OFFICIAL_ANSWERS[q_num]
    pdf_ans = official_pdf.get(q_num)
    
    if not pdf_ans:
        print(f"Q{q_num}: PDF answer not found!")
        all_match = False
        continue
    
    # Check type
    if code_ans['type'] != pdf_ans[0]:
        print(f"Q{q_num}: Type mismatch - Code:{code_ans['type']} vs PDF:{pdf_ans[0]}")
        all_match = False
        continue
    
    # Check answer
    if code_ans['type'] == 'NAT':
        if 'range' in code_ans:
            if pdf_ans[1] != 'range' or code_ans['range'] != pdf_ans[2]:
                print(f"Q{q_num}: NAT range mismatch - Code:{code_ans['range']} vs PDF:{pdf_ans[2]}")
                all_match = False
        else:
            if pdf_ans[1] != 'value' or code_ans['value'] != pdf_ans[2]:
                print(f"Q{q_num}: NAT value mismatch - Code:{code_ans['value']} vs PDF:{pdf_ans[2]}")
                all_match = False
    elif code_ans['type'] == 'MSQ':
        if set(code_ans['keys']) != set(pdf_ans[2]):
            print(f"Q{q_num}: MSQ keys mismatch - Code:{code_ans['keys']} vs PDF:{pdf_ans[2]}")
            all_match = False
    else:  # MCQ
        if code_ans['key'] != pdf_ans[2]:
            print(f"Q{q_num}: MCQ key mismatch - Code:{code_ans['key']} vs PDF:{pdf_ans[2]}")
            all_match = False

if all_match:
    print("✓ ALL 44 ANSWERS MATCH OFFICIAL PDF EXACTLY")
else:
    print("✗ MISMATCHES FOUND!")

print("-"*80)
print(f"\nTotal questions verified: {len(official_pdf)}")
print("="*80)
