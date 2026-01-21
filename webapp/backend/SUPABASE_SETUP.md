# Supabase Setup Instructions

## 1. Create Supabase Project
1. Go to https://supabase.com
2. Sign up or log in
3. Create a new project
4. Note down your project URL and anon/public API key

## 2. Create Database Table

Run this SQL in the Supabase SQL Editor:

```sql
-- Create scores table
CREATE TABLE scores (
    id BIGSERIAL PRIMARY KEY,
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    total_score DECIMAL(5,2) NOT NULL,
    nat_score DECIMAL(5,2) NOT NULL,
    msq_score DECIMAL(5,2) NOT NULL,
    mcq_score DECIMAL(5,2) NOT NULL,
    section_details JSONB,
    question_details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create index on student_id for faster lookups
CREATE INDEX idx_scores_student_id ON scores(student_id);

-- Create index on created_at for sorting
CREATE INDEX idx_scores_created_at ON scores(created_at DESC);

-- Enable Row Level Security
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (you can restrict this later)
CREATE POLICY "Allow all operations" ON scores
    FOR ALL
    USING (true)
    WITH CHECK (true);
```

## 3. Environment Variables

Create a `.env` file in the backend directory with:

```
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here
```

## 4. Table Schema

- `student_id`: Unique identifier extracted from PDF (Application Number/Roll Number)
- `name`: Student's name from PDF
- `total_score`: Overall score out of 150
- `nat_score`: NAT section score
- `msq_score`: MSQ section score  
- `mcq_score`: MCQ section score
- `section_details`: JSON with detailed section breakdown (correct/wrong/unattempted)
- `question_details`: JSON array with all 44 questions and answers
- `created_at`: When record was first created
- `updated_at`: When record was last updated
