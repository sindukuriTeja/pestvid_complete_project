# 🌐 Complete Hosting & Deployment Guide for PestVid

## Overview
This guide covers deploying your PestVid platform to the cloud for public access.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCTION SETUP                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (Vercel/Netlify)                                  │
│  └─ Static files (HTML, CSS, JS)                           │
│  └─ URL: https://pestivid.vercel.app                       │
│                                                              │
│  Backend API (Vercel/Railway/Render)                        │
│  └─ Node.js + Express                                       │
│  └─ URL: https://pestivid-api.vercel.app                   │
│                                                              │
│  Database (Supabase)                                         │
│  └─ PostgreSQL                                              │
│  └─ Auto-managed, auto-scaled                              │
│                                                              │
│  AI Server (Railway/Render)                                  │
│  └─ Flask + Python                                          │
│  └─ URL: https://pestivid-ai.railway.app                   │
│                                                              │
│  File Storage (Supabase Storage)                            │
│  └─ Videos, images                                          │
│  └─ CDN delivery                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 1: Database (Supabase) ✅

### Already Covered!
Follow `SUPABASE_QUICK_SETUP.md` to set up your database.

**Result:** Database URL ready to use

---

## Part 2: Deploy Backend API

### Option A: Vercel (Recommended - Easiest)

#### Step 1: Prepare Backend
```bash
cd backend
# Create vercel.json
```

Create `backend/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "server-supabase.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server-supabase.js"
    }
  ]
}
```

#### Step 2: Deploy
1. Install Vercel CLI: `npm install -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel`
4. Add environment variables in Vercel dashboard:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `JWT_SECRET`
   - `GROQ_API_KEY`

#### Step 3: Get URL
Your backend will be at: `https://your-project.vercel.app`

---

### Option B: Railway (Good for Python + Node.js)

#### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

#### Step 2: Deploy on Railway
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Add environment variables
6. Deploy!

**Result:** Backend URL like `https://pestivid-production.up.railway.app`

---

### Option C: Render

#### Step 1: Create render.yaml
```yaml
services:
  - type: web
    name: pestivid-backend
    env: node
    buildCommand: npm install
    startCommand: node server-supabase.js
    envVars:
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_SERVICE_KEY
        sync: false
      - key: JWT_SECRET
        sync: false
```

#### Step 2: Deploy
1. Go to https://render.com
2. Connect GitHub
3. Create new Web Service
4. Select repository
5. Add environment variables
6. Deploy!

---

## Part 3: Deploy Flask AI Server

### Option A: Railway (Recommended for Python)

#### Step 1: Create requirements.txt
Already created! Located at `PestVid-main/requirements.txt`

#### Step 2: Create Procfile
Create `Procfile` in root:
```
web: python flask_server_simple.py
```

#### Step 3: Update Flask Server
Update `flask_server_simple.py` last line:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### Step 4: Deploy on Railway
1. Push to GitHub
2. Create new project on Railway
3. Deploy from GitHub
4. Railway auto-detects Python
5. Add environment variables:
   - `GROQ_API_KEY`
   - `COHERE_API_KEY`
   - `PINECONE_API_KEY`

**Result:** AI server at `https://pestivid-ai.up.railway.app`

---

### Option B: Render

Create `render.yaml`:
```yaml
services:
  - type: web
    name: pestivid-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python flask_server_simple.py
    envVars:
      - key: GROQ_API_KEY
        sync: false
```

---

## Part 4: Deploy Frontend

### Option A: Vercel (Recommended)

#### Step 1: Prepare Frontend
Update `public/index.html` - find all API URLs and replace:

```javascript
// OLD
const API_URL = 'http://localhost:3001';
const AI_URL = 'http://localhost:5000';

// NEW
const API_URL = 'https://your-backend.vercel.app';
const AI_URL = 'https://your-ai-server.railway.app';
```

#### Step 2: Deploy
```bash
cd public
vercel
```

Or use Vercel dashboard:
1. Import project
2. Set root directory to `public`
3. Deploy!

**Result:** Frontend at `https://pestivid.vercel.app`

---

### Option B: Netlify

#### Step 1: Create netlify.toml
```toml
[build]
  publish = "public"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Step 2: Deploy
1. Go to https://netlify.com
2. Drag and drop `public` folder
3. Or connect GitHub repo

---

### Option C: GitHub Pages (Free!)

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

#### Step 2: Enable GitHub Pages
1. Go to repository Settings
2. Pages section
3. Source: main branch, /public folder
4. Save

**Result:** `https://yourusername.github.io/pestivid`

---

## Part 5: Update Frontend API URLs

### Method 1: Environment-based Config

Create `public/js/config.js`:
```javascript
const CONFIG = {
    API_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:3001'
        : 'https://your-backend.vercel.app',
    AI_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:5000'
        : 'https://your-ai-server.railway.app'
};
```

Include in `index.html`:
```html
<script src="js/config.js"></script>
```

Use in your code:
```javascript
axios.post(`${CONFIG.API_URL}/api/auth/login`, data)
```

---

### Method 2: Direct Replacement

Search and replace in all files:
- `http://localhost:3001` → `https://your-backend.vercel.app`
- `http://localhost:5000` → `https://your-ai-server.railway.app`

---

## Part 6: Configure CORS

Update backend `server-supabase.js`:

```javascript
const corsOptions = {
  origin: [
    'http://localhost:3000',
    'https://pestivid.vercel.app',
    'https://yourusername.github.io'
  ],
  credentials: true,
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));
```

---

## Part 7: Custom Domain (Optional)

### For Vercel:
1. Go to project settings
2. Domains section
3. Add custom domain
4. Update DNS records

### For Netlify:
1. Domain settings
2. Add custom domain
3. Configure DNS

---

## Deployment Checklist

### Pre-Deployment
- [ ] Supabase database created and configured
- [ ] All environment variables documented
- [ ] API keys secured (not in code)
- [ ] CORS configured for production domains
- [ ] Frontend API URLs updated
- [ ] Test all features locally

### Backend Deployment
- [ ] Backend deployed to Vercel/Railway/Render
- [ ] Environment variables added
- [ ] Health check endpoint working
- [ ] Database connection successful
- [ ] API endpoints responding

### AI Server Deployment
- [ ] Flask server deployed
- [ ] Python dependencies installed
- [ ] API keys configured
- [ ] Endpoints responding
- [ ] CORS configured

### Frontend Deployment
- [ ] Frontend deployed to Vercel/Netlify/GitHub Pages
- [ ] API URLs updated to production
- [ ] All pages loading correctly
- [ ] Authentication working
- [ ] File uploads working (if applicable)

### Post-Deployment
- [ ] Test complete user flow
- [ ] Test on mobile devices
- [ ] Check browser console for errors
- [ ] Monitor error logs
- [ ] Set up analytics (optional)
- [ ] Configure custom domain (optional)

---

## Cost Breakdown

### Free Tier (Perfect for Starting)
- **Supabase:** Free (500MB DB, 1GB storage)
- **Vercel:** Free (100GB bandwidth)
- **Railway:** $5/month credit (enough for small apps)
- **Netlify:** Free (100GB bandwidth)
- **GitHub Pages:** Free (1GB storage)

**Total:** $0-5/month for small to medium traffic

### Paid Tier (For Growth)
- **Supabase Pro:** $25/month (8GB DB, 100GB storage)
- **Vercel Pro:** $20/month (1TB bandwidth)
- **Railway:** Pay as you go (~$10-20/month)

**Total:** ~$55-65/month for serious production use

---

## Monitoring & Maintenance

### Supabase Dashboard
- Monitor database usage
- View query performance
- Check API logs

### Vercel Dashboard
- Monitor deployments
- View function logs
- Check bandwidth usage

### Railway Dashboard
- Monitor resource usage
- View application logs
- Check uptime

---

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Enable HTTPS** - All platforms provide this free
3. **Configure CORS** - Only allow your domains
4. **Use Supabase RLS** - Row Level Security policies
5. **Rate limiting** - Prevent API abuse
6. **Input validation** - Sanitize all user inputs
7. **Regular backups** - Supabase does this automatically

---

## Troubleshooting

### "CORS Error"
- Check CORS configuration in backend
- Verify frontend URL is allowed
- Check browser console for exact error

### "API Not Responding"
- Check backend deployment logs
- Verify environment variables are set
- Test API endpoint directly with curl

### "Database Connection Failed"
- Check Supabase credentials
- Verify project is not paused
- Check connection string format

### "Frontend Not Loading"
- Check deployment logs
- Verify build completed successfully
- Check browser console for errors

---

## Next Steps

1. ✅ Complete Supabase setup
2. ✅ Deploy backend to Vercel/Railway
3. ✅ Deploy AI server to Railway
4. ✅ Deploy frontend to Vercel/Netlify
5. ✅ Test everything end-to-end
6. ✅ Share your live URL!

---

## Your Live URLs

After deployment, you'll have:

```
Frontend:  https://pestivid.vercel.app
Backend:   https://pestivid-api.vercel.app
AI Server: https://pestivid-ai.railway.app
Database:  https://your-project.supabase.co
```

Share the frontend URL with users!

---

## Support

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Supabase Docs: https://supabase.com/docs
- Netlify Docs: https://docs.netlify.com

---

## Congratulations! 🎉

Your PestVid platform is now live and accessible worldwide!
