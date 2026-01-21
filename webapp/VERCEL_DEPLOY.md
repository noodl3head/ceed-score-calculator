# Vercel Frontend Deployment Guide

## Quick Deploy to Vercel

### Option 1: Vercel CLI (Fastest)

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Navigate to frontend**:
```bash
cd webapp\frontend
```

3. **Login to Vercel**:
```bash
vercel login
```

4. **Deploy**:
```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? (your account)
- Link to existing project? **N**
- Project name? **ceed-calculator** (or your choice)
- Directory? **.** (current directory)
- Override settings? **N**

5. **Set Environment Variable**:
```bash
vercel env add VITE_API_URL
```
Enter your backend URL: `https://your-backend.railway.app`

6. **Deploy to Production**:
```bash
vercel --prod
```

✅ Done! Your frontend is live.

---

### Option 2: Vercel Dashboard (No CLI)

1. **Push to GitHub**:
```bash
git add .
git commit -m "Add frontend"
git push
```

2. **Go to Vercel Dashboard**:
- Visit [vercel.com](https://vercel.com)
- Click "Add New" → "Project"

3. **Import Repository**:
- Connect your GitHub account
- Select your repository
- Click "Import"

4. **Configure Project**:
- **Framework Preset**: Vite
- **Root Directory**: `webapp/frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

5. **Add Environment Variable**:
- Click "Environment Variables"
- Name: `VITE_API_URL`
- Value: `https://your-backend.railway.app` (your backend URL)
- Environment: Production, Preview, Development (select all)

6. **Deploy**:
- Click "Deploy"
- Wait ~2 minutes
- Your site will be live at `https://your-project.vercel.app`

---

## Update Backend URL After Deployment

### If you deployed backend first:

```bash
vercel env add VITE_API_URL production
# Enter: https://your-backend.railway.app

# Redeploy to apply changes
vercel --prod
```

### If you need to update it:

1. Go to Vercel Dashboard
2. Select your project
3. Settings → Environment Variables
4. Edit `VITE_API_URL`
5. Redeploy (Deployments → click ⋯ → Redeploy)

---

## Custom Domain (Optional)

### Add Custom Domain:

1. Vercel Dashboard → Your Project → Settings → Domains
2. Enter your domain: `ceed-calculator.com`
3. Add DNS records at your domain registrar:

```
Type: CNAME
Name: @
Value: cname.vercel-dns.com

Type: CNAME  
Name: www
Value: cname.vercel-dns.com
```

4. Wait for DNS propagation (~5-60 minutes)
5. SSL certificate auto-generated

---

## Automatic Deployments

Vercel automatically deploys when you push to GitHub:

- **Production**: Push to `main` branch
- **Preview**: Push to any other branch or open PR

### Disable Auto-Deploy (if needed):
1. Settings → Git
2. Uncheck "Production Branch"

---

## Backend Deployment Options

Deploy your backend to one of these platforms:

### Railway (Recommended - Easy + Free Tier)

1. Go to [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Select repository
4. Root directory: `webapp/backend`
5. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `FLASK_ENV=production`
   - `PORT=5000`
6. Deploy
7. Copy the generated URL (e.g., `https://your-app.up.railway.app`)
8. Update Vercel env variable `VITE_API_URL` with this URL

### Render

1. Go to [render.com](https://render.com)
2. "New" → "Web Service"
3. Connect repository
4. Root directory: `webapp/backend`
5. Build command: `pip install -r requirements.txt`
6. Start command: `python app.py`
7. Add environment variables
8. Deploy

### Heroku

1. Install Heroku CLI
2. Create `Procfile` in `webapp/backend`:
   ```
   web: python app.py
   ```
3. Deploy:
   ```bash
   cd webapp/backend
   heroku create your-app-name
   heroku config:set SUPABASE_URL=xxx SUPABASE_KEY=xxx FLASK_ENV=production
   git subtree push --prefix webapp/backend heroku main
   ```

---

## CORS Configuration

Make sure your backend allows requests from Vercel:

In `webapp/backend/app.py`, update CORS:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-project.vercel.app",
            "https://your-custom-domain.com",
            "http://localhost:3000"  # for local dev
        ]
    }
})
```

Or allow all origins (less secure):
```python
CORS(app)  # Already configured this way
```

---

## Testing Deployment

1. **Frontend URL**: `https://your-project.vercel.app`
2. **Upload a test PDF**
3. **Check browser console** (F12) for any errors
4. **Verify API calls** go to correct backend URL

---

## Monitoring

### Vercel Dashboard:
- **Analytics**: Usage stats
- **Speed Insights**: Performance metrics
- **Logs**: Real-time function logs
- **Deployments**: History of all deploys

### Common Issues:

**API calls fail (CORS error)**:
- Update backend CORS configuration
- Verify `VITE_API_URL` is correct

**Environment variable not working**:
- Make sure it starts with `VITE_`
- Redeploy after adding variables

**Build fails**:
- Check build logs in Vercel dashboard
- Verify `package.json` is correct
- Ensure all dependencies are listed

**404 on refresh**:
- Add `vercel.json` with SPA routing (already created)

---

## Cost

**Vercel Free Tier (Hobby)**:
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- Custom domains
- Perfect for this project

**Vercel Pro** ($20/month):
- Only needed for commercial use or high traffic
- More bandwidth and features

---

## Rollback

If something breaks:

1. Vercel Dashboard → Deployments
2. Find last working deployment
3. Click ⋯ → "Promote to Production"

---

## Environment Variables Summary

Frontend (Vercel):
```
VITE_API_URL=https://your-backend-url.railway.app
```

Backend (Railway/Render/Heroku):
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_service_role_key
FLASK_ENV=production
PORT=5000
```

---

## Complete Deployment Checklist

- [ ] Backend deployed (Railway/Render/Heroku)
- [ ] Backend URL obtained
- [ ] Frontend pushed to GitHub
- [ ] Vercel project created
- [ ] `VITE_API_URL` environment variable set
- [ ] Frontend deployed successfully
- [ ] Test upload works
- [ ] Scores display correctly
- [ ] Database records created
- [ ] Custom domain configured (optional)
- [ ] CORS configured properly
- [ ] HTTPS working

---

**Your app will be live at**: `https://your-project.vercel.app`

**Deployment time**: ~5 minutes total (2 min frontend + 3 min backend)
