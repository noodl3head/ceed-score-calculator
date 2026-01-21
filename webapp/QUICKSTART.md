# Quick Start Guide

Get the CEED Score Calculator running locally in 5 minutes.

## Step 1: Supabase Setup (2 minutes)

1. **Create Supabase Account**: Go to [supabase.com](https://supabase.com) and sign up

2. **Create New Project**:
   - Click "New Project"
   - Name: `ceed-calculator`
   - Database Password: (choose a strong password)
   - Region: Choose closest to you
   - Click "Create new project" (takes ~2 minutes)

3. **Create Database Table**:
   - Go to SQL Editor (left sidebar)
   - Click "New Query"
   - Copy and paste this SQL:

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
    section_details JSONB NOT NULL,
    question_details JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster lookups
CREATE INDEX idx_scores_student_id ON scores(student_id);

-- Enable Row Level Security (RLS)
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust for production)
CREATE POLICY "Enable all operations for service role" ON scores
FOR ALL USING (true) WITH CHECK (true);
```

   - Click "Run" to execute

4. **Get API Keys**:
   - Go to Settings → API (left sidebar)
   - Copy these two values:
     - **Project URL**: `https://xxxxx.supabase.co`
     - **service_role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (the long one)

## Step 2: Backend Setup (1 minute)

1. **Open Terminal** in your project root

2. **Navigate to backend**:
```bash
cd webapp\backend
```

3. **Create Virtual Environment**:
```bash
python -m venv venv
```

4. **Activate Virtual Environment**:
```bash
venv\Scripts\activate
```

5. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

6. **Create .env File**:
```bash
copy .env.example .env
```

7. **Edit .env File** (open in notepad):
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_service_role_key_here
FLASK_ENV=development
PORT=5000
```
Replace with your actual Supabase URL and key from Step 1.4

8. **Start Backend**:
```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

✅ Backend is running! Keep this terminal open.

## Step 3: Frontend Setup (2 minutes)

1. **Open NEW Terminal** (keep backend running)

2. **Navigate to frontend**:
```bash
cd webapp\frontend
```

3. **Install Dependencies**:
```bash
npm install
```

This will take ~1-2 minutes.

4. **Start Frontend**:
```bash
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in 500 ms

  ➜  Local:   http://localhost:3000/
```

5. **Open Browser**: Go to http://localhost:3000

## Step 4: Test the Application

1. **Upload a PDF**:
   - Use one of the test PDFs in the root directory
   - Or upload any CEED 2026 response sheet

2. **View Results**:
   - Score calculation happens automatically
   - Results show section-wise and question-wise analysis

3. **Check Database**:
   - Go back to Supabase
   - Click "Table Editor" → "scores"
   - You should see your test record

## Troubleshooting

### Backend Won't Start

**Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Error: No module named 'calculate_score'**
Make sure you're in the correct directory and calculate_score.py exists in the parent directory.

**Error: Supabase connection failed**
- Check your .env file
- Verify SUPABASE_URL and SUPABASE_KEY are correct
- Make sure you used the `service_role` key, not `anon` key

### Frontend Won't Start

**Error: command not found: npm**
Install Node.js from [nodejs.org](https://nodejs.org) (LTS version)

**Error: ECONNREFUSED**
Make sure backend is running on port 5000

**Error: Cannot GET /api/...**
- Backend is not running
- Check if backend is on http://localhost:5000

### PDF Upload Fails

**Error: File too large**
- Default limit is 16 MB
- Compress PDF or use smaller file

**Error: Invalid PDF**
- Make sure file is actually a PDF
- Try re-downloading the response sheet

## Next Steps

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment guide.

### Development
- Backend code: `webapp/backend/app.py`
- Frontend components: `webapp/frontend/src/components/`
- Scoring logic: `calculate_score.py` (root directory)

### Testing
- Test PDFs are in the root directory
- Create test scripts for automated testing

## Commands Reference

### Backend Commands
```bash
# Start backend
cd webapp\backend
venv\Scripts\activate
python app.py

# Install new package
pip install package-name
pip freeze > requirements.txt

# Stop backend
Ctrl + C
```

### Frontend Commands
```bash
# Start frontend
cd webapp\frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new package
npm install package-name

# Stop frontend
Ctrl + C
```

### Database Commands (Supabase)
- View data: Supabase Dashboard → Table Editor
- Query data: SQL Editor
- View logs: Logs section
- Backup: Settings → Backups

## Support

If you encounter issues:
1. Check the error message carefully
2. Search the error online
3. Review README.md and DEPLOYMENT.md
4. Check Supabase and Flask documentation

---

**That's it! You should now have a fully functional local development environment.**

Happy coding! 🚀
