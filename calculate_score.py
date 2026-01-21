import re

# Official Answer Key
OFFICIAL_ANSWERS = {
    # Section I: NAT
    1: {"type": "NAT", "range": [6.0, 6.5]},
    2: {"type": "NAT", "range": [126.0, 128.0]},
    3: {"type": "NAT", "range": [24.0, 25.5]},
    4: {"type": "NAT", "value": 18.0},
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
    42: {"type": "MCQ", "key": "C"},
    43: {"type": "MCQ", "key": "B"},
    44: {"type": "MCQ", "key": "B"},
}

# Unique patterns for each official question
QUESTION_PATTERNS = {
    # NAT
    1: r"geometric\s+blocks\s+with\s+their\s+dimensions",
    2: r"ice-cream\s+cone\s+completely\s+filled",
    3: r"square\s+paper\s+of\s+side\s+10\s+cm",
    4: r"unique\s+patterns\s+are\s+there\s+in\s+the\s+image",
    5: r"spheres\s+are\s+rotating",
    6: r"Nine\s+tiles\s+containing\s+parts\s+of\s+English",
    7: r"plane\s+passes\s+through\s+three\s+vertices",
    8: r"board\s+game\s*,\s+and\s+two\s+views",
    
    # MSQ
    9: r"octahedron\s+as\s+shown\s+on\s+the\s+left",
    10: r"NOT\s+a\s+part\s+of\s+the\s+image\s+on\s+the\s+left",
    11: r"symmetrical\s+along\s+vertical\s+planes",
    12: r"Coloured\s+strips\s+are\s+printed\s+on\s+a\s+transparent",
    13: r"table\s+made\s+out\s+of\s+cardboard",
    14: r"plant\s+pruner\s+\(cutter\)\s+with\s+two\s+studs",
    15: r"triangular\s+groove\s+is\s+shown\s+on\s+the\s+left",
    16: r"planets\s+orbiting\s+around\s+the\s+sun",
    17: r"views\s+of\s+a\s+3D\s+object\s+are\s+shown",
    18: r"Six\s+different\s+shapes\s+are\s+cut\s+from\s+a\s+square",
    
    # MCQ
    19: r"stack\s+of\s+sugar\s+cubes",
    20: r"rubber\s+roller\s+is\s+cut\s+with\s+a",
    21: r"resultant\s+image\?", 
    22: r"options\s+belong\s+to\s+the\s+same\s+font\?",
    23: r"Which\s+spanner\s+from\s+the\s+options",
    24: r"perspective\s+drawing\s+of\s+the\s+object",
    25: r"red\s+dot\s+is\s+connected\s+with\s+two",
    26: r"replace\s+the\s+question\s+mark\?\s+Options\s+1\.\s+A", # Distinguish from Q33
    27: r"grid\s+PQRS\s+is\s+distorted",
    28: r"Sets\s+of\s+T\s*oys\s+and\s+Furniture",
    29: r"art\s+movements\s+sequentially",
    30: r"image\s+on\s+the\s+left\s+to\s+form\s+a\s+word",
    31: r"OPEN\s+HEART",
    32: r"magnetic\s+and\s+non-magnetic\s+bars",
    33: r"replace\s+the\s+question\s+mark\?\s+Options\s+1\.", # Catching differently
    34: r"fan\s+is\s+also\s+required\s+to\s+spin",
    35: r"reciprocating\s+movement\s+is\s+shown",
    36: r"monuments\s+in\s+India\s+from\s+North\s+to\s+South",
    37: r"application\s+screen\s+are\s+shown\s+below",
    38: r"wooden\s+artifact\s+made\s+using\s+traditional",
    39: r"seat\s+is\s+to\s+be\s+designed\s+for\s+a\s+public\s+bus",
    40: r"identical\s+hollow\s+cylinders\s+is\s+shown",
    41: r"solid\s+copper\s+object\s+is\s+shown",
    42: r"lit\s+by\s+sunlight\s+at\s+45\s+degrees",
    43: r"toy\s+set",
    44: r"gestalt\s+principles\s+associated",
}

def parse_response_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    # DON'T remove footer noise yet - it removes actual answers like "31/20/26"
    # We'll clean it during answer extraction instead
    
    # Split into logical sections based on Q.1 restarts
    # We find all Q.X markers
    matches = list(re.finditer(r'Q\.\d+', content))
    sections = []
    current_section = []
    last_num = -1
    
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        q_block = content[start:end]
        
        m = re.match(r'Q\.(\d+)', q_block)
        curr_num = int(m.group(1))
        
        if curr_num < last_num:
            # Numbering reset! New section.
            sections.append(current_section)
            current_section = []
        
        # Extract fields from q_block
        q_text_match = re.search(r'Q\.\d+\s*(.*?)(?=Given|Options|Question ID|Status)', q_block, re.DOTALL)
        q_text = q_text_match.group(1).strip() if q_text_match else ""
        
        answer_match = re.search(r'Answer\s*:(.*?)(?=\s*Question ID|Status|$)', q_block, re.DOTALL)
        chosen_option_match = re.search(r'Chosen Option\s*:([^\n]*)', q_block)
        status_match = re.search(r'Status\s*:(.*?)(?=\s*Given|Options|Question ID|Answer|Chosen Option|$)', q_block, re.DOTALL)
        
        q_info = {
            "text": q_text,
            "raw_block": q_block,
            "status": status_match.group(1).strip() if status_match else "",
            "answer": answer_match.group(1).strip() if answer_match else None,
            "chosen_options": chosen_option_match.group(1).strip() if chosen_option_match else None
        }
        
        # Clean chosen_options - handle timestamp and URL contamination
        if q_info["chosen_options"]:
            raw = q_info["chosen_options"].strip()
            
            # First, remove any trailing date/timestamp patterns and URLs
            cleaned = re.sub(r'\s*\d{1,2}/\d{1,2}/\d{2,4}.*$', '', raw)
            cleaned = re.sub(r'\s*http.*$', '', cleaned)
            cleaned = re.sub(r'\s*cdn\..*$', '', cleaned)
            
            # Remove any text after the first valid answer pattern
            # Valid patterns: digits with optional commas/spaces (1,3 or 13 or 4,2 or 42), or --
            match = re.match(r'^([\d,\s]+|--|\d+)(?:\s|$)', cleaned)
            if match:
                cleaned = match.group(1)
            
            # Remove all whitespace
            cleaned = re.sub(r'\s+', '', cleaned)
            cleaned = cleaned.rstrip(',').strip()
            
            # Check if it's a valid answer format
            if not cleaned or cleaned == '--' or cleaned.startswith('--'):
                q_info["chosen_options"] = "--"
            # Accept any combination of digits 1-4 (with or without commas)
            # This includes: 1, 1,3, 13, 42, 123, 1,2,3 etc.
            elif re.match(r'^[1-4,]+$', cleaned) and re.search(r'[1-4]', cleaned):
                q_info["chosen_options"] = cleaned
            else:
                # Invalid format, treat as unanswered
                q_info["chosen_options"] = "--"
                
        current_section.append(q_info)
        last_num = curr_num
    
    sections.append(current_section)
    return sections

def calculate_msq_score(correct_keys, chosen_keys, status=""):
    if status == "Not Answered" or not chosen_keys or chosen_keys == "--":
        return 0
    
    # Handle both comma-separated (1,3) and consecutive digits (13 or 42)
    if ',' in chosen_keys:
        chosen_raw = chosen_keys.split(',')
    else:
        # Split consecutive digits: "42" -> ["4", "2"], "123" -> ["1", "2", "3"]
        chosen_raw = list(chosen_keys)
    
    map_dict = {"1": "A", "2": "B", "3": "C", "4": "D"}
    chosen = {map_dict.get(c.strip(), c.strip()) for c in chosen_raw if c.strip() and c.strip() in map_dict}
    
    if not chosen: return 0
    correct = set(correct_keys)
    
    # If any incorrect option is chosen, return -1
    if not chosen.issubset(correct): return -1
    
    # Full marks: All correct options chosen
    if chosen == correct: return 4
    
    # Partial marks based on official rules:
    # +3: All 4 options are correct but ONLY 3 chosen
    if len(correct) == 4 and len(chosen) == 3: return 3
    
    # +2: Three or more options are correct but ONLY 2 chosen (both correct)
    if len(correct) >= 3 and len(chosen) == 2: return 2
    
    # +1: Two or more options are correct but ONLY 1 chosen (correct)
    if len(correct) >= 2 and len(chosen) == 1: return 1
    
    # All other cases (shouldn't reach here if logic is correct)
    return -1

def calculate_mcq_score(correct_key, chosen_option, status=""):
    if status == "Not Answered" or not chosen_option or chosen_option == "--":
        return 0
    
    # MCQ should only have ONE option - reject multi-digit or comma-separated answers
    # Valid: "1", "2", "3", "4"
    # Invalid: "42", "12", "1,2", etc.
    if len(chosen_option) > 1 or ',' in chosen_option:
        # Multi-digit or multiple options for MCQ = wrong answer
        return -0.5
    
    map_dict = {"1": "A", "2": "B", "3": "C", "4": "D"}
    chosen = map_dict.get(chosen_option.strip(), chosen_option.strip())
    
    if chosen == correct_key: return 3
    else: return -0.5

def calculate_nat_score(answer_rule, user_answer):
    if not user_answer or user_answer == "N/A": return 0
    try:
        val = float(user_answer)
        if "range" in answer_rule:
            if answer_rule["range"][0] <= val <= answer_rule["range"][1]: return 4
        elif "value" in answer_rule:
            if val == answer_rule["value"]: return 4
    except: pass
    return 0

def main():
    sections = parse_response_text("response_text.txt")
    
    # Flatten all questions from all sections into one list
    all_questions = []
    for section in sections:
        all_questions.extend(section)
    
    mapping = {} # official_num -> user_q_info
    
    # Map all questions by searching across all responses
    # This handles cases where questions are scattered across sections
    for q_num in range(1, 45):
        pattern = QUESTION_PATTERNS[q_num]
        for user_q in all_questions:
            # Search in raw_block as well in case question text extraction was clipped
            if re.search(pattern, user_q["raw_block"], re.IGNORECASE | re.DOTALL):
                mapping[q_num] = user_q
                break

    # Track scores by section
    section_scores = {
        "NAT": {"total": 0, "negative": 0, "correct": 0, "wrong": 0, "unattempted": 0},
        "MSQ": {"total": 0, "negative": 0, "correct": 0, "wrong": 0, "unattempted": 0},
        "MCQ": {"total": 0, "negative": 0, "correct": 0, "wrong": 0, "unattempted": 0}
    }
    
    results = []
    
    for q_num in range(1, 45):
        official = OFFICIAL_ANSWERS[q_num]
        user_q = mapping.get(q_num)
        
        score = 0
        user_display = "N/A"
        correct_display = ""
        status = "Not Found"
        
        if user_q:
            status = user_q["status"]
            if official["type"] == "NAT":
                user_display = user_q["answer"] if user_q["answer"] else "N/A"
                correct_display = f"{official.get('value', official.get('range'))}"
                score = calculate_nat_score(official, user_q["answer"])
            elif official["type"] == "MSQ":
                user_display = user_q["chosen_options"] if user_q["chosen_options"] else "N/A"
                correct_display = ",".join(official["keys"])
                score = calculate_msq_score(official["keys"], user_q["chosen_options"], status)
            elif official["type"] == "MCQ":
                user_display = user_q["chosen_options"] if user_q["chosen_options"] else "N/A"
                correct_display = official["key"]
                score = calculate_mcq_score(official["key"], user_q["chosen_options"], status)
        else:
            if official["type"] == "NAT": correct_display = f"{official.get('value', official.get('range'))}"
            elif official["type"] == "MSQ": correct_display = ",".join(official["keys"])
            elif official["type"] == "MCQ": correct_display = official["key"]
        
        # Update section statistics
        section_type = official["type"]
        section_scores[section_type]["total"] += score
        if score > 0:
            section_scores[section_type]["correct"] += 1
        elif score < 0:
            section_scores[section_type]["negative"] += score
            section_scores[section_type]["wrong"] += 1
        else:
            # Score is 0 - check if it's actually unattempted or wrong attempt
            is_unattempted = False
            if user_q and user_display:
                # Check if answer was provided
                if official["type"] == "NAT":
                    # For NAT, if answer exists and isn't N/A or --, it was attempted but wrong
                    if user_display not in ["N/A", "--", None, ""]:
                        section_scores[section_type]["wrong"] += 1
                    else:
                        section_scores[section_type]["unattempted"] += 1
                        is_unattempted = True
                else:
                    # For MSQ/MCQ, if chosen_options is -- or N/A, it's unattempted
                    if user_display in ["N/A", "--", None, ""]:
                        section_scores[section_type]["unattempted"] += 1
                        is_unattempted = True
                    else:
                        # This shouldn't happen for MSQ/MCQ (would be negative or positive)
                        section_scores[section_type]["unattempted"] += 1
                        is_unattempted = True
            else:
                section_scores[section_type]["unattempted"] += 1
                is_unattempted = True
            
        results.append({
            "q_num": q_num,
            "type": official["type"],
            "status": status,
            "user_ans": user_display,
            "correct_ans": correct_display,
            "score": score
        })
    
    # Generate report
    total_score = sum(section_scores[s]["total"] for s in section_scores)
    total_negative = sum(section_scores[s]["negative"] for s in section_scores)
    
    # Find section with most negative score
    worst_section = min(section_scores.keys(), key=lambda s: section_scores[s]["negative"])
    
    # Write to file
    with open("score_summary.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("CEED 2026 - PART A SCORE REPORT\n")
        f.write("="*80 + "\n\n")
        
        # Summary
        f.write("OVERALL SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Score:           {total_score:.1f} / 150\n")
        f.write(f"Total Negative Score:  {total_negative:.1f}\n")
        f.write(f"Section with Most Negative Score: {worst_section} ({section_scores[worst_section]['negative']:.1f} marks)\n")
        f.write("\n")
        
        # Section-wise breakdown
        f.write("SECTION-WISE BREAKDOWN\n")
        f.write("-"*80 + "\n")
        for section in ["NAT", "MSQ", "MCQ"]:
            stats = section_scores[section]
            max_score = 32 if section == "NAT" else (40 if section == "MSQ" else 78)
            f.write(f"\n{section} (Max: {max_score} marks)\n")
            f.write(f"  Score:            {stats['total']:.1f}\n")
            f.write(f"  Negative Score:   {stats['negative']:.1f}\n")
            f.write(f"  Correct:          {stats['correct']}\n")
            f.write(f"  Wrong:            {stats['wrong']}\n")
            f.write(f"  Unattempted:      {stats['unattempted']}\n")
        
        f.write("\n\n")
        f.write("DETAILED QUESTION-WISE REPORT\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Q.No':<6} {'Type':<6} {'Status':<16} {'User Ans':<12} {'Correct':<12} {'Score':<6}\n")
        f.write("-"*80 + "\n")
        
        for r in results:
            # Clean user answer for display (remove URL fragments)
            user_ans = str(r["user_ans"])
            if "http" in user_ans or len(user_ans) > 15:
                user_ans = user_ans.split("http")[0].split("1/20/26")[0].strip()
                if user_ans.endswith(","):
                    user_ans = user_ans[:-1]
            
            status = r["status"].split("1/20/26")[0].strip()
            
            f.write(f"{r['q_num']:<6} {r['type']:<6} {status:<16} {user_ans:<12} {str(r['correct_ans']):<12} {r['score']:<6.1f}\n")
        
        f.write("-"*80 + "\n")
        f.write(f"TOTAL PART A SCORE: {total_score:.1f}\n")
        f.write("="*80 + "\n")
    
    print(f"Score report generated: score_summary.txt")
    print(f"\nTotal Score: {total_score:.1f} / 150")
    print(f"Total Negative: {total_negative:.1f}")
    print(f"Worst Section: {worst_section} ({section_scores[worst_section]['negative']:.1f} marks)")

if __name__ == "__main__":
    main()
