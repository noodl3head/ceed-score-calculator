import re
from pypdf import PdfReader

# Step 1: Verify Official Answer Key against PDF
print("="*80)
print("STEP 1: VERIFYING OFFICIAL ANSWER KEY AGAINST PDF")
print("="*80)

reader = PdfReader("CEED2026_draftAnswerkey.pdf")
pdf_text = reader.pages[0].extract_text()

# Extract answers from PDF
nat_matches = re.findall(r'(\d+)\s+(\d+(?:\.\d+)?(?:\s+to\s+\d+(?:\.\d+)?)?)', pdf_text[:200])
msq_section = re.search(r'SECTION – II \(MSQ\)(.*?)SECTION – III', pdf_text, re.DOTALL)
mcq_section = re.search(r'SECTION – III \(MCQ\)(.*?)$', pdf_text, re.DOTALL)

print("\nNAT Questions (Official PDF):")
for q, ans in nat_matches[:8]:
    print(f"  Q{q}: {ans}")

if msq_section:
    msq_text = msq_section.group(1)
    msq_matches = re.findall(r'(\d+)\s+([A-D,\s]+)', msq_text)
    print("\nMSQ Questions (Official PDF):")
    for q, ans in msq_matches[:10]:
        print(f"  Q{q}: {ans.strip()}")

if mcq_section:
    mcq_text = mcq_section.group(1)
    mcq_matches = re.findall(r'(\d+)\s+([A-D])\s', mcq_text)
    print("\nMCQ Questions (Official PDF - first 10):")
    for q, ans in mcq_matches[:10]:
        print(f"  Q{q}: {ans}")

# Step 2: Test parsing logic with sample questions
print("\n" + "="*80)
print("STEP 2: TESTING PARSING LOGIC")
print("="*80)

with open('response_text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Find specific test cases
test_cases = [
    ("Q.1.*?board game.*?Answer\s*:\s*(\d+(?:\.\d+)?)", "Q1 NAT - board game"),
    ("Q.3.*?square paper.*?Answer\s*:\s*(\d+(?:\.\d+)?)", "Q3 NAT - square paper"),
    ("Q.6.*?symmetrical.*?Chosen Option\s*:\s*([^\n]+)", "Q11 MSQ - symmetrical"),
    ("Q.3.*?resultant.*?image.*?Chosen Option\s*:\s*([^\n]+)", "Q21 MCQ - resultant image"),
]

print("\nSample raw extractions:")
for pattern, desc in test_cases:
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if match:
        raw_value = match.group(1)[:60]
        print(f"  {desc}: '{raw_value}'")
    else:
        print(f"  {desc}: NOT FOUND")

# Step 3: Test cleaning logic
print("\n" + "="*80)
print("STEP 3: TESTING ANSWER CLEANING LOGIC")
print("="*80)

test_answers = [
    "15",
    "31/20/26, 11:24 AM cdn.digialm.com//per/",
    "41/20/26, 11:24 AM cdn...",
    "2,4",
    "1,3,41/20/26",
    "11/20/26, 11:24 AM cdn...",
    "--",
    "https://cdn.digialm.com//per/g01/",
]

print("\nCleaning test:")
for raw in test_answers:
    match = re.match(r'^([\d,\s]+?)(?=\d/\d+/\d+|http|cdn)', raw)
    if match:
        cleaned = match.group(1).strip()
    else:
        cleaned = re.split(r'\n|http|cdn\.digialm', raw)[0].strip()
        cleaned = re.sub(r'\s*\d+/\d+/\d+.*$', '', cleaned)
    
    cleaned = cleaned.rstrip(',').strip()
    
    if not cleaned or cleaned == '--' or cleaned.startswith('--'):
        result = '--'
    elif re.match(r'^[\d,\s]+$', cleaned):
        cleaned = re.sub(r'\s+', '', cleaned)
        result = cleaned
    else:
        result = '--'
    
    print(f"  '{raw[:40]:40}' -> '{result}'")

# Step 4: Test scoring logic
print("\n" + "="*80)
print("STEP 4: TESTING SCORING LOGIC")
print("="*80)

def calculate_nat_score(answer_rule, user_answer):
    if not user_answer or user_answer == "N/A" or user_answer == "--":
        return 0
    try:
        val = float(user_answer)
        if "range" in answer_rule:
            if answer_rule["range"][0] <= val <= answer_rule["range"][1]:
                return 4
        elif "value" in answer_rule:
            if val == answer_rule["value"]:
                return 4
    except:
        pass
    return 0

def calculate_msq_score(correct_keys, chosen_keys, status=""):
    if status == "Not Answered" or not chosen_keys or chosen_keys == "--":
        return 0
    
    chosen_raw = chosen_keys.split(',')
    map_dict = {"1": "A", "2": "B", "3": "C", "4": "D"}
    chosen = {map_dict.get(c.strip(), c.strip()) for c in chosen_raw if c.strip()}
    
    if not chosen: return 0
    correct = set(correct_keys)
    
    if not chosen.issubset(correct): return -1
    if chosen == correct: return 4
    if len(correct) == 4 and len(chosen) == 3: return 3
    if len(correct) >= 3 and len(chosen) == 2: return 2
    if len(correct) >= 2 and len(chosen) == 1: return 1
    return -1

def calculate_mcq_score(correct_key, chosen_option, status=""):
    if status == "Not Answered" or not chosen_option or chosen_option == "--":
        return 0
    
    map_dict = {"1": "A", "2": "B", "3": "C", "4": "D"}
    chosen = map_dict.get(chosen_option.strip(), chosen_option.strip())
    
    if chosen == correct_key: return 3
    else: return -0.5

print("\nNAT Scoring Tests:")
nat_tests = [
    ({"range": [6.0, 6.5]}, "6.2", 4),
    ({"range": [6.0, 6.5]}, "6.6", 0),
    ({"range": [6.0, 6.5]}, "5.9", 0),
    ({"value": 18.0}, "18", 4),
    ({"value": 18.0}, "17", 0),
]
for rule, answer, expected in nat_tests:
    result = calculate_nat_score(rule, answer)
    status = "✓" if result == expected else "✗ ERROR"
    print(f"  {status} Rule={rule}, Answer='{answer}' -> Score={result} (expected {expected})")

print("\nMSQ Scoring Tests:")
msq_tests = [
    (["A", "B", "C"], "1,2,3", 4),  # All correct
    (["A", "B", "C"], "1,2", 2),    # 3 correct, 2 chosen
    (["A", "B", "C", "D"], "1,2,3", 3),  # 4 correct, 3 chosen
    (["A", "D"], "1", 1),           # 2 correct, 1 chosen
    (["A", "B"], "1,3", -1),        # One wrong
    (["A", "B"], "--", 0),          # Not answered
]
for correct, chosen, expected in msq_tests:
    result = calculate_msq_score(correct, chosen)
    status = "✓" if result == expected else "✗ ERROR"
    print(f"  {status} Correct={correct}, Chosen='{chosen}' -> Score={result} (expected {expected})")

print("\nMCQ Scoring Tests:")
mcq_tests = [
    ("A", "1", 3),
    ("A", "2", -0.5),
    ("D", "4", 3),
    ("D", "3", -0.5),
    ("A", "--", 0),
]
for correct, chosen, expected in mcq_tests:
    result = calculate_mcq_score(correct, chosen)
    status = "✓" if result == expected else "✗ ERROR"
    print(f"  {status} Correct={correct}, Chosen='{chosen}' -> Score={result} (expected {expected})")

# Step 5: Manual verification of specific questions
print("\n" + "="*80)
print("STEP 5: MANUAL VERIFICATION OF SAMPLE QUESTIONS")
print("="*80)

print("\nChecking Q1 (NAT - board game):")
q1_match = re.search(r'Q\.1.*?board game.*?Answer\s*:\s*(\d+)', content, re.DOTALL | re.IGNORECASE)
if q1_match:
    answer = q1_match.group(1)
    print(f"  Student answer: {answer}")
    print(f"  Correct answer: 6.0-6.5 or exact value")
    print(f"  Official correct: Range [6.0, 6.5]")
    score = calculate_nat_score({"range": [6.0, 6.5]}, answer)
    print(f"  Calculated score: {score} (should be 4 if 6.0-6.5, else 0)")

print("\nChecking Q12 (MSQ - B,D):")
q12_pattern = r'Q\.7.*?Coloured strips.*?Chosen Option\s*:\s*([^\n]+)'
q12_match = re.search(q12_pattern, content, re.DOTALL | re.IGNORECASE)
if q12_match:
    raw = q12_match.group(1)
    print(f"  Raw chosen: '{raw[:60]}'")
    # Clean it
    match = re.match(r'^([\d,\s]+?)(?=\d/\d+/\d+|http|cdn)', raw)
    if match:
        cleaned = match.group(1).strip().replace(' ', '')
    else:
        cleaned = "--"
    print(f"  Cleaned chosen: '{cleaned}'")
    print(f"  Correct answer: B,D")
    score = calculate_msq_score(["B", "D"], cleaned)
    print(f"  Calculated score: {score}")

print("\nChecking Q21 (MCQ - C):")
q21_pattern = r'Q\.3.*?resultant.*?image.*?Chosen Option\s*:\s*([^\n]+)'
q21_match = re.search(q21_pattern, content, re.DOTALL | re.IGNORECASE)
if q21_match:
    raw = q21_match.group(1)
    print(f"  Raw chosen: '{raw[:60]}'")
    match = re.match(r'^([\d,\s]+?)(?=\d/\d+/\d+|http|cdn)', raw)
    if match:
        cleaned = match.group(1).strip()
    else:
        cleaned = "--"
    print(f"  Cleaned chosen: '{cleaned}'")
    print(f"  Correct answer: C (option 3)")
    score = calculate_mcq_score("C", cleaned)
    print(f"  Calculated score: {score} (should be 3 if chosen=3, -0.5 otherwise)")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80)
