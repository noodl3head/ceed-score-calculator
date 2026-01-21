# CEED 2026 Score Calculator - Web Application

A production-ready web application for calculating CEED 2026 Part A exam scores from response sheet PDFs.

## Features

- 📤 **PDF Upload**: Drag-and-drop or click to upload response sheets
- 🔢 **Automatic Scoring**: Calculates scores based on official CEED 2026 marking scheme
- 📊 **Detailed Analysis**: Section-wise and question-wise breakdown
- 💾 **Score Storage**: Stores student information and scores in Supabase
- 📱 **Mobile-First Design**: Optimized for mobile devices
- ⚡ **Fast & Secure**: Built with React, Flask, and Supabase

## Scoring Rules

- **NAT (Numerical Answer Type)**: 4 marks (correct) or 0 marks (wrong/unattempted)
- **MSQ (Multiple Select Questions)**: 4, 3, 2, 1, 0, or -1 marks based on correctness
- **MCQ (Multiple Choice Questions)**: 3 marks (correct), -0.5 marks (wrong), 0 marks (unattempted)

## Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- Axios
- Lucide Icons

### Backend
- Python 3.12
- Flask 3.0
- pypdf for PDF processing
- Supabase for database

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.12+
- Supabase account

### Backend Setup

1. Navigate to backend directory:
```bash
cd webapp/backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Supabase:
   - Create a new Supabase project
   - Run the SQL from `SUPABASE_SETUP.md` in the SQL Editor
   - Copy your project URL and service role key

5. Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
FLASK_ENV=development
PORT=5000
```

6. Run the backend:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd webapp/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## API Endpoints

### POST /api/calculate-score
Uploads PDF, extracts student info, calculates score, and stores in database.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (PDF file)

**Response:**
```json
{
  "student_info": {
    "name": "Student Name",
    "student_id": "APPLICATION123"
  },
  "scores": {
    "total_score": 70.0,
    "nat_score": 16,
    "msq_score": 8,
    "mcq_score": 46
  },
  "section_details": {
    "NAT Section": {
      "score": 16,
      "max_score": 40,
      "correct": 4,
      "wrong": 2,
      "unattempted": 4
    },
    ...
  },
  "question_details": {
    "Q1": {
      "type": "NAT",
      "student_answer": "3",
      "correct_answer": "3",
      "score": 4
    },
    ...
  }
}
```

### GET /api/scores/:student_id
Retrieves stored scores for a student.

**Response:**
```json
{
  "student_id": "APPLICATION123",
  "name": "Student Name",
  "total_score": 70.0,
  "nat_score": 16,
  "msq_score": 8,
  "mcq_score": 46,
  "section_details": {...},
  "question_details": {...}
}
```

### GET /api/health
Health check endpoint.

## Project Structure

```
webapp/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── requirements.txt       # Python dependencies
│   ├── SUPABASE_SETUP.md     # Database setup guide
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadPage.jsx    # PDF upload UI
│   │   │   └── ResultsPage.jsx   # Score display UI
│   │   ├── App.jsx               # Main app component
│   │   ├── main.jsx              # Entry point
│   │   └── index.css             # Global styles
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── .env.example
```

## Building for Production

### Frontend (Vercel - Recommended)

**Quick Deploy:**
```bash
cd webapp/frontend
npm install -g vercel
vercel login
vercel
```

Set environment variable:
- `VITE_API_URL`: Your backend URL

See [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for detailed instructions.

**Manual Build:**
```bash
cd webapp/frontend
npm run build
```

The build output will be in `dist/` directory.

### Backend (Railway/Render/Heroku)
The Flask app is production-ready. Deploy to:
- **Railway** (Recommended - easiest setup)
- Render
- Heroku
- Google Cloud Run
- AWS Elastic Beanstalk

See [DEPLOYMENT.md](DEPLOYMENT.md) for backend deployment guides.

## Environment Variables

### Backend (.env)
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase service role key
- `FLASK_ENV`: `development` or `production`
- `PORT`: Port number (default: 5000)

### Frontend (.env)
- `VITE_API_URL`: Backend API URL (default: http://localhost:5000)

## Verification

All scoring logic has been rigorously tested and verified against:
- Official CEED 2026 marking scheme
- CEED2026_draftAnswerkey.pdf
- Multiple test response sheets

See `VERIFICATION_REPORT.txt` for detailed test results.

## License

MIT License

## Support

For issues or questions, please contact the development team.
