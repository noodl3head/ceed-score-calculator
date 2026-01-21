import re

# Simplified version of parse_response_text
with open('response_text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove footer noise
content = re.sub(r'\d+/\d+/\d+,\s+\d+:\d+\s+[AP]M.*', '', content)

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
    q_text = q_text_match.group(1).strip() if q_text_match else ''
    
    chosen_option_match = re.search(r'Chosen Option\s*:(.*?)(?=\s*Q\.\d+|$)', q_block, re.DOTALL)
    raw_chosen = chosen_option_match.group(1).strip() if chosen_option_match else None
    
    if raw_chosen:
        match_test = re.match(r'^([\d,\s]+?)(?=\d/\d+/\d+|http|cdn)', raw_chosen)
        if match_test:
            cleaned = match_test.group(1).strip()
        else:
            cleaned = re.split(r'\n|http|cdn\.digialm', raw_chosen)[0].strip()
            cleaned = re.sub(r'\s*\d+/\d+/\d+.*$', '', cleaned)
        
        cleaned = cleaned.rstrip(',').strip()
    else:
        cleaned = None
    
    current_section.append({
        'q_num': curr_num, 
        'text': q_text[:50], 
        'raw_chosen': raw_chosen[:40] if raw_chosen else None, 
        'cleaned': cleaned
    })
    last_num = curr_num

sections.append(current_section)

# Find Q.3 in section 3 (MCQ) - should be Q21
print(f'Total sections: {len(sections)}')
if len(sections) >= 3:
    print(f'\nSection 3 (MCQ) - first 10 questions:')
    for q in sections[2][:10]:
        raw_display = f"'{q['raw_chosen']}'" if q['raw_chosen'] else 'None'
        print(f"  Q.{q['q_num']}: Raw={raw_display:50} | Cleaned={q['cleaned']}")
