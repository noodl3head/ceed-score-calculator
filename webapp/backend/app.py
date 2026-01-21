from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
import re
import os
from datetime import datetime
from supabase import create_client, Client
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
except Exception as e:
    print(f"Warning: Could not initialize Supabase client: {e}")
    supabase = None

# Import scoring logic from root directory (two levels up)
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from calculate_score import (
    OFFICIAL_ANSWERS, 
    QUESTION_PATTERNS,
    calculate_nat_score,
    calculate_msq_score,
    calculate_mcq_score,
    parse_response_text
)

def extract_student_info(pdf_path):
    """Extract student name and ID from PDF"""
    reader = PdfReader(pdf_path)
    full_text = ""
    # Read first 2 pages to find info
    for i in range(min(2, len(reader.pages))):
        full_text += reader.pages[i].extract_text()
    
    # Try multiple patterns for name extraction
    name = "Unknown"
    name_patterns = [
        r'Participant Name\s+([A-Z\s]+?)(?=\n|Test Center|Test Date)',
        r'Candidate Name\s*:?\s*([^\n]+)',
        r'Name\s*:?\s*([A-Z][A-Za-z\s]+?)(?=\n|Application|\d{10})',
        r'Student Name\s*:?\s*([^\n]+)',
    ]
    
    for pattern in name_patterns:
        name_match = re.search(pattern, full_text, re.IGNORECASE)
        if name_match:
            extracted = name_match.group(1).strip()
            # Clean up common contamination
            extracted = re.split(r'\d{2}/\d{2}/\d{2,4}|\d{10,}|Application|Test Center', extracted)[0].strip()
            if extracted and len(extracted) > 2 and not extracted.isdigit():
                name = extracted
                break
    
    # Extract Application Number or ID
    student_id = None
    id_patterns = [
        r'Participant ID\s+(\d+)',
        r'Application Number\s*:?\s*(\d+)',
        r'Roll Number\s*:?\s*(\d+)',
        r'ID\s*:?\s*(\d+)',
        r'\b(\d{10,})\b'  # Any 10+ digit number as fallback
    ]
    
    for pattern in id_patterns:
        id_match = re.search(pattern, full_text, re.IGNORECASE)
        if id_match:
            student_id = id_match.group(1).strip()
            break
    
    student_id = id_match.group(1).strip() if id_match else None
    
    return name, student_id

def calculate_score_from_pdf(pdf_path):
    """Calculate score from PDF and return detailed results"""
    # Extract text from PDF
    reader = PdfReader(pdf_path)
    content = ""
    for i, page in enumerate(reader.pages):
        content += f"--- Page {i+1} ---\n"
        content += page.extract_text()
        content += "\n\n"
    
    # Parse using existing logic
    sections = parse_response_with_content(content)
    all_questions = []
    for section in sections:
        all_questions.extend(section)
    
    # Map questions
    mapping = {}
    for q_num in range(1, 45):
        pattern = QUESTION_PATTERNS[q_num]
        for user_q in all_questions:
            if re.search(pattern, user_q["raw_block"], re.IGNORECASE | re.DOTALL):
                mapping[q_num] = user_q
                break
    
    # Calculate scores
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
            if official["type"] == "NAT": 
                correct_display = f"{official.get('value', official.get('range'))}"
            elif official["type"] == "MSQ": 
                correct_display = ",".join(official["keys"])
            elif official["type"] == "MCQ": 
                correct_display = official["key"]
        
        # Update section statistics
        section_type = official["type"]
        section_scores[section_type]["total"] += score
        
        if score > 0:
            section_scores[section_type]["correct"] += 1
        elif score < 0:
            section_scores[section_type]["negative"] += score
            section_scores[section_type]["wrong"] += 1
        else:
            if user_q and user_display:
                if official["type"] == "NAT":
                    if user_display not in ["N/A", "--", None, ""]:
                        section_scores[section_type]["wrong"] += 1
                    else:
                        section_scores[section_type]["unattempted"] += 1
                else:
                    if user_display in ["N/A", "--", None, ""]:
                        section_scores[section_type]["unattempted"] += 1
                    else:
                        section_scores[section_type]["unattempted"] += 1
            else:
                section_scores[section_type]["unattempted"] += 1
        
        results.append({
            "q_num": q_num,
            "type": official["type"],
            "status": status,
            "user_ans": user_display,
            "correct_ans": correct_display,
            "score": score
        })
    
    total_score = sum(section_scores[s]["total"] for s in section_scores)
    total_negative = sum(section_scores[s]["negative"] for s in section_scores)
    worst_section = min(section_scores.keys(), key=lambda s: section_scores[s]["negative"])
    
    return {
        "total_score": total_score,
        "total_negative": total_negative,
        "worst_section": worst_section,
        "section_scores": section_scores,
        "results": results
    }

def parse_response_with_content(content):
    """Parse response text content (from calculate_score.py logic)"""
    # Split into logical sections based on Q.1 restarts
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
            sections.append(current_section)
            current_section = []
        
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
        
        # Clean chosen_options
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

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "supabase_connected": supabase is not None})

@app.route('/api/calculate-score', methods=['POST'])
def calculate_score_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        # Extract student info
        name, student_id = extract_student_info(tmp_path)
        
        if not student_id:
            return jsonify({"error": "Could not extract student ID from PDF"}), 400
        
        # Calculate score
        score_data = calculate_score_from_pdf(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Format section details for frontend
        section_details_formatted = {
            "NAT Section": {
                "score": score_data["section_scores"]["NAT"]["total"],
                "max_score": 32,
                "correct": score_data["section_scores"]["NAT"]["correct"],
                "wrong": score_data["section_scores"]["NAT"]["wrong"],
                "unattempted": score_data["section_scores"]["NAT"]["unattempted"]
            },
            "MSQ Section": {
                "score": score_data["section_scores"]["MSQ"]["total"],
                "max_score": 40,
                "correct": score_data["section_scores"]["MSQ"]["correct"],
                "wrong": score_data["section_scores"]["MSQ"]["wrong"],
                "unattempted": score_data["section_scores"]["MSQ"]["unattempted"]
            },
            "MCQ Section": {
                "score": score_data["section_scores"]["MCQ"]["total"],
                "max_score": 78,
                "correct": score_data["section_scores"]["MCQ"]["correct"],
                "wrong": score_data["section_scores"]["MCQ"]["wrong"],
                "unattempted": score_data["section_scores"]["MCQ"]["unattempted"]
            }
        }
        
        # Format question details for frontend
        question_details_formatted = {}
        for q in score_data["results"]:
            q_key = f"Q{q['q_num']}"
            question_details_formatted[q_key] = {
                "type": q["type"],
                "student_answer": q["user_ans"],
                "correct_answer": q["correct_ans"],
                "score": q["score"]
            }
        
        # Prepare response for frontend
        result = {
            "student_info": {
                "name": name,
                "student_id": student_id
            },
            "scores": {
                "total_score": score_data["total_score"],
                "nat_score": score_data["section_scores"]["NAT"]["total"],
                "msq_score": score_data["section_scores"]["MSQ"]["total"],
                "mcq_score": score_data["section_scores"]["MCQ"]["total"]
            },
            "section_details": section_details_formatted,
            "question_details": question_details_formatted
        }
        
        # Store in Supabase if configured
        if supabase:
            try:
                # Check if student already exists
                existing = supabase.table('scores').select('*').eq('student_id', student_id).execute()
                
                if existing.data:
                    # Update existing record
                    supabase.table('scores').update({
                        "name": name,
                        "total_score": score_data["total_score"],
                        "nat_score": result["scores"]["nat_score"],
                        "msq_score": result["scores"]["msq_score"],
                        "mcq_score": result["scores"]["mcq_score"],
                        "section_details": section_details_formatted,
                        "question_details": question_details_formatted,
                        "updated_at": datetime.utcnow().isoformat()
                    }).eq('student_id', student_id).execute()
                else:
                    # Insert new record
                    supabase.table('scores').insert({
                        "student_id": student_id,
                        "name": name,
                        "total_score": score_data["total_score"],
                        "nat_score": result["scores"]["nat_score"],
                        "msq_score": result["scores"]["msq_score"],
                        "mcq_score": result["scores"]["mcq_score"],
                        "section_details": section_details_formatted,
                        "question_details": question_details_formatted,
                        "created_at": datetime.utcnow().isoformat()
                    }).execute()
            except Exception as e:
                print(f"Supabase error: {e}")
                # Continue even if Supabase fails
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scores/<student_id>', methods=['GET'])
def get_score(student_id):
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    
    try:
        result = supabase.table('scores').select('*').eq('student_id', student_id).execute()
        if result.data:
            return jsonify(result.data[0]), 200
        else:
            return jsonify({"error": "Score not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
