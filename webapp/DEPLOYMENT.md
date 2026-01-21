# Deployment Guide

This guide covers deploying the CEED 2026 Score Calculator to production.

## Prerequisites

- Supabase account (free tier available)
- Hosting platform account (Vercel, Netlify, Railway, etc.)
- Domain name (optional)

## 1. Supabase Setup

### Create Project
1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Fill in project details and create

### Run SQL Setup
1. Go to SQL Editor in your Supabase project
2. Copy the SQL from `backend/SUPABASE_SETUP.md`
3. Run the SQL to create the `scores` table

### Get API Credentials
1. Go to Settings → API
2. Copy the following:
   - Project URL (e.g., `https://xxxxx.supabase.co`)
   - `service_role` key (for backend)
   - `anon` key (for frontend if needed)

## 2. Backend Deployment

### Option A: Railway (Recommended)

1. **Create Railway Account**: Go to [railway.app](https://railway.app)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Configure Service**:
   - Root directory: `webapp/backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py`

4. **Set Environment Variables**:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_service_role_key
   FLASK_ENV=production
   PORT=5000
   ```

5. **Deploy**: Railway will automatically deploy your app

6. **Get URL**: Copy the generated URL (e.g., `https://your-app.railway.app`)

### Option B: Heroku

1. **Install Heroku CLI**: Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login**:
   ```bash
   heroku login
   ```

3. **Create App**:
   ```bash
   cd webapp/backend
   heroku create your-app-name
   ```

4. **Add Python Buildpack**:
   ```bash
   heroku buildpacks:set heroku/python
   ```

5. **Set Environment Variables**:
   ```bash
   heroku config:set SUPABASE_URL=https://your-project.supabase.co
   heroku config:set SUPABASE_KEY=your_service_role_key
   heroku config:set FLASK_ENV=production
   ```

6. **Create Procfile**:
   ```bash
   echo "web: python app.py" > Procfile
   ```

7. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy backend"
   git push heroku main
   ```

### Option C: Google Cloud Run

1. **Install gcloud CLI**: Download from [cloud.google.com](https://cloud.google.com/sdk/docs/install)

2. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "app.py"]
   ```

3. **Build and Deploy**:
   ```bash
   gcloud run deploy ceed-calculator \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars SUPABASE_URL=xxx,SUPABASE_KEY=xxx,FLASK_ENV=production
   ```

## 3. Frontend Deployment

### Option A: Vercel (Recommended for React)

**See [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for complete step-by-step guide.**

**Quick Setup:**

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   cd webapp/frontend
   vercel login
   vercel
   ```

3. **Set Environment Variable**:
   ```bash
   vercel env add VITE_API_URL
   # Enter: https://your-backend-url.railway.app
   ```

4. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

**Via Dashboard:**

1. Go to [vercel.com](https://vercel.com)
2. "Add New" → "Project" → Import from GitHub
3. Root Directory: `webapp/frontend`
4. Framework: Vite (auto-detected)
5. Add environment variable: `VITE_API_URL=https://your-backend-url.railway.app`
6. Deploy

Your site will be live at: `https://your-project.vercel.app`

### Option B: Netlify

1. **Create Netlify Account**: Go to [netlify.com](https://netlify.com)

2. **New Site from Git**:
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Select repository

3. **Configure Build**:
   - Base directory: `webapp/frontend`
   - Build command: `npm run build`
   - Publish directory: `webapp/frontend/dist`

4. **Environment Variables**:
   - Go to Site settings → Environment variables
   - Add: `VITE_API_URL=https://your-backend-url.railway.app`

5. **Deploy**: Netlify will auto-deploy

### Option C: Manual Static Hosting

1. **Build Frontend**:
   ```bash
   cd webapp/frontend
   npm install
   npm run build
   ```

2. **Upload `dist/` folder** to any static hosting:
   - GitHub Pages
   - AWS S3 + CloudFront
   - Firebase Hosting
   - Cloudflare Pages

## 4. Post-Deployment Configuration

### Update CORS Settings (Backend)

If frontend and backend are on different domains, update `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-frontend-domain.com",
            "http://localhost:3000"  # for local development
        ]
    }
})
```

### Test the Application

1. Open your frontend URL
2. Upload a test PDF
3. Verify score calculation works
4. Check Supabase database for stored records

### Enable HTTPS

Both Vercel and Railway provide HTTPS automatically. For custom deployments:
- Use Let's Encrypt for free SSL certificates
- Configure reverse proxy (Nginx) with SSL

## 5. Environment Variables Summary

### Backend Environment Variables
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
FLASK_ENV=production
PORT=5000
```

### Frontend Environment Variables
```
VITE_API_URL=https://your-backend-url.railway.app
```

## 6. Monitoring & Maintenance

### Set Up Monitoring
- **Railway**: Built-in logs and metrics
- **Vercel**: Analytics dashboard
- **Supabase**: Database usage dashboard

### Database Backups
1. Go to Supabase Dashboard → Settings → Backups
2. Enable automatic backups (Pro plan)
3. Or manually export data periodically

### Logs
- **Backend**: Check Railway/Heroku logs
- **Frontend**: Check Vercel deployment logs
- **Database**: Check Supabase logs

## 7. Scaling Considerations

### Database
- Free tier: 500 MB database, 50,000 monthly active users
- Upgrade to Pro for more capacity

### Backend
- Railway: Auto-scales based on usage
- Use environment variable to increase workers if needed

### Frontend
- Vercel/Netlify provide global CDN automatically
- No additional configuration needed

## 8. Cost Estimates

### Free Tier (Suitable for Testing)
- Supabase: Free (500 MB)
- Railway: $5/month credit
- Vercel: Free (hobby plan)
- **Total: $0-5/month**

### Production Tier
- Supabase Pro: $25/month
- Railway Pro: $20/month
- Vercel Pro: $20/month
- **Total: ~$65/month**

## 9. Custom Domain Setup

### DNS Configuration
Add the following records to your domain registrar:

For Frontend (example.com):
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
```

For Backend (api.example.com):
```
Type: CNAME
Name: api
Value: your-app.railway.app
```

### Update Environment Variables
```
VITE_API_URL=https://api.example.com
```

## 10. Troubleshooting

### Backend Issues
- **500 Error**: Check Supabase credentials
- **CORS Error**: Verify CORS settings in app.py
- **File Upload Fails**: Check file size limits

### Frontend Issues
- **API Connection Failed**: Verify VITE_API_URL
- **Build Fails**: Check Node.js version (18+)
- **Blank Page**: Check browser console for errors

### Database Issues
- **Connection Failed**: Verify SUPABASE_URL and KEY
- **Insert Failed**: Check table schema and RLS policies

## 11. Security Checklist

- ✅ Use HTTPS for all connections
- ✅ Keep service role key secret (backend only)
- ✅ Enable RLS policies in Supabase
- ✅ Validate file uploads (PDF only, size limits)
- ✅ Rate limit API endpoints
- ✅ Regular security updates

## 12. Continuous Deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: vercel --prod
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
```

## Support

For deployment issues:
1. Check platform documentation
2. Review application logs
3. Contact platform support
4. Open GitHub issue

---

**Deployment Checklist:**
- [ ] Supabase project created and configured
- [ ] Backend deployed and tested
- [ ] Frontend deployed and tested
- [ ] Environment variables set correctly
- [ ] CORS configured properly
- [ ] Database connected successfully
- [ ] File upload working
- [ ] Score calculation verified
- [ ] HTTPS enabled
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Backups enabled
