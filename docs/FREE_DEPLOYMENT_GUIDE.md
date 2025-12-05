# Free Deployment Guide

This guide covers the best free options to deploy your Pharmaceutical Agentic AI Research Platform.

## 🎯 Recommended Free Deployment Strategy

**Best Combination:**
- **Frontend**: Vercel or Netlify (excellent for React, free SSL, CDN)
- **Backend**: Render or Railway (free tier for Python/FastAPI)
- **Redis**: Upstash Redis (free tier) or Railway (includes Redis)

---

## 🚀 Option 1: Render (Easiest - All-in-One)

**Best for**: Deploying both backend and frontend on one platform

### Free Tier Limits:
- ✅ 750 hours/month (enough for 24/7 operation)
- ✅ Free SSL certificates
- ✅ Automatic deployments from GitHub
- ✅ 512MB RAM per service
- ✅ PostgreSQL database included (free tier)

### Steps:

1. **Sign up**: https://render.com (use GitHub account)

2. **Deploy Backend:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: `pharma-ai-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Root Directory**: `backend`
   - Add Environment Variables:
     ```
     OPENAI_API_KEY=your_key
     GOOGLE_API_KEY=your_key
     REDIS_URL=redis://your-redis-url
     PORT=10000
     ```
   - Click "Create Web Service"

3. **Deploy Frontend:**
   - Click "New +" → "Static Site"
   - Connect your GitHub repository
   - Settings:
     - **Name**: `pharma-ai-frontend`
     - **Build Command**: `cd frontend && npm install && npm run build`
     - **Publish Directory**: `frontend/build`
     - **Root Directory**: `frontend`
   - Add Environment Variable:
     ```
     REACT_APP_API_URL=https://your-backend-url.onrender.com
     ```
   - Click "Create Static Site"

4. **Add Redis (Optional):**
   - Click "New +" → "Redis"
   - Use free tier
   - Copy connection URL to backend environment variables

**Pros**: Simple, all-in-one, free SSL, auto-deployments  
**Cons**: Services spin down after 15 min inactivity (free tier), first request may be slow

---

## 🚀 Option 2: Vercel (Frontend) + Railway (Backend)

**Best for**: Best performance and developer experience

### Vercel (Frontend) - FREE

**Free Tier:**
- ✅ Unlimited deployments
- ✅ Free SSL
- ✅ Global CDN
- ✅ Automatic preview deployments

**Steps:**
1. Sign up: https://vercel.com (use GitHub)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Environment Variables**:
     ```
     REACT_APP_API_URL=https://your-backend-url.railway.app
     ```
5. Click "Deploy"

### Railway (Backend) - FREE with $5 credit/month

**Free Tier:**
- ✅ $5 free credit/month (usually enough for small apps)
- ✅ Free SSL
- ✅ No cold starts
- ✅ Includes Redis

**Steps:**
1. Sign up: https://railway.app (use GitHub)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add service → Select "Backend" directory
5. Configure:
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     OPENAI_API_KEY=your_key
     GOOGLE_API_KEY=your_key
     PORT=8000
     ```
6. Add Redis service (included in free tier)
7. Update `REDIS_URL` environment variable

**Pros**: Fast, no cold starts, great DX  
**Cons**: Limited free credit (may need to pay after $5)

---

## 🚀 Option 3: Netlify (Frontend) + Fly.io (Backend)

### Netlify (Frontend) - FREE

**Free Tier:**
- ✅ 100GB bandwidth/month
- ✅ Free SSL
- ✅ Continuous deployment
- ✅ Form handling

**Steps:**
1. Sign up: https://netlify.com
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub repository
4. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
   - **Environment Variables**:
     ```
     REACT_APP_API_URL=https://your-backend-url.fly.dev
     ```
5. Click "Deploy site"

### Fly.io (Backend) - FREE

**Free Tier:**
- ✅ 3 shared-cpu VMs (256MB RAM each)
- ✅ 3GB persistent volume storage
- ✅ 160GB outbound data transfer

**Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup`
3. In backend directory, create `fly.toml`:
   ```toml
   app = "pharma-ai-backend"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[vm]]
     cpu_kind = "shared"
     cpus = 1
     memory_mb = 256
   ```
4. Deploy: `fly deploy`
5. Set secrets:
   ```bash
   fly secrets set OPENAI_API_KEY=your_key
   fly secrets set GOOGLE_API_KEY=your_key
   ```

**Pros**: Good free tier, fast  
**Cons**: More setup required

---

## 🚀 Option 4: PythonAnywhere (Backend) + GitHub Pages (Frontend)

### PythonAnywhere (Backend) - FREE

**Free Tier:**
- ✅ 1 web app
- ✅ 512MB disk space
- ✅ Limited to 1 CPU
- ✅ External requests allowed

**Steps:**
1. Sign up: https://www.pythonanywhere.com
2. Upload your backend code (or clone from GitHub)
3. Create web app:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → "Python 3.10"
   - Set source code path: `/home/username/pharma-ai/backend`
4. Configure WSGI file:
   ```python
   import sys
   path = '/home/username/pharma-ai/backend'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from app.main import app
   application = app
   ```
5. Set environment variables in "Web" → "Environment variables"
6. Reload web app

### GitHub Pages (Frontend) - FREE

**Steps:**
1. Build frontend: `cd frontend && npm run build`
2. Push `build` folder to `gh-pages` branch
3. Enable GitHub Pages in repository settings
4. Set base URL in `package.json`:
   ```json
   "homepage": "https://yourusername.github.io/repo-name"
   ```

**Pros**: Completely free, reliable  
**Cons**: PythonAnywhere has limitations, GitHub Pages is static only

---

## 🔧 Redis Options (Free)

### Option A: Upstash Redis (Recommended)
- **URL**: https://upstash.com
- **Free Tier**: 10,000 commands/day, 256MB storage
- **Steps**: Sign up → Create database → Copy connection URL

### Option B: Redis Cloud
- **URL**: https://redis.com/try-free/
- **Free Tier**: 30MB storage, 30 connections
- **Steps**: Sign up → Create database → Copy connection URL

### Option C: Railway Redis
- Included when you deploy backend on Railway
- No separate setup needed

---

## 📝 Quick Comparison

| Platform | Backend | Frontend | Free Tier | Ease of Use | Best For |
|----------|---------|----------|-----------|-------------|----------|
| **Render** | ✅ | ✅ | 750 hrs/month | ⭐⭐⭐⭐⭐ | Beginners |
| **Vercel** | ❌ | ✅ | Unlimited | ⭐⭐⭐⭐⭐ | Frontend focus |
| **Railway** | ✅ | ❌ | $5 credit/month | ⭐⭐⭐⭐ | Backend focus |
| **Netlify** | ❌ | ✅ | 100GB bandwidth | ⭐⭐⭐⭐⭐ | Frontend focus |
| **Fly.io** | ✅ | ❌ | 3 VMs | ⭐⭐⭐ | Advanced users |
| **PythonAnywhere** | ✅ | ❌ | 1 web app | ⭐⭐⭐ | Python-only |

---

## 🎯 Recommended Setup for Beginners

**Easiest Path:**
1. **Frontend**: Deploy to Vercel (5 minutes)
2. **Backend**: Deploy to Render (10 minutes)
3. **Redis**: Use Upstash Redis (5 minutes)

**Total Time**: ~20 minutes  
**Cost**: $0/month

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] All API keys are ready (OpenAI, Google AI)
- [ ] `.env` files are NOT committed to Git (add to `.gitignore`)
- [ ] Frontend build works locally: `cd frontend && npm run build`
- [ ] Backend runs locally: `cd backend && uvicorn app.main:app`
- [ ] CORS is configured for your frontend URL
- [ ] Environment variables are set in deployment platform
- [ ] Redis URL is configured (if using Redis)

---

## 🔒 Security Best Practices

1. **Never commit API keys** to Git
2. **Use environment variables** in deployment platforms
3. **Enable HTTPS** (most platforms do this automatically)
4. **Set CORS** to only allow your frontend domain
5. **Use secrets management** features in deployment platforms

---

## 🐛 Common Deployment Issues

### Backend Issues:

**"Module not found" errors:**
- Ensure `requirements.txt` is in the backend directory
- Check build command includes `pip install -r requirements.txt`

**"Port binding" errors:**
- Use `$PORT` environment variable (Render, Railway)
- Or set port to `8000` (Fly.io, PythonAnywhere)

**"API key not found" errors:**
- Verify environment variables are set in deployment platform
- Check variable names match exactly (case-sensitive)

### Frontend Issues:

**"Cannot connect to backend" errors:**
- Verify `REACT_APP_API_URL` is set correctly
- Check backend URL includes `https://`
- Ensure CORS allows your frontend domain

**"Build fails":**
- Check Node.js version (should be 18+)
- Verify all dependencies in `package.json`
- Check build logs for specific errors

---

## 🚀 Quick Start Commands

### Render Deployment:
```bash
# Just connect GitHub repo and configure in dashboard
# No CLI needed!
```

### Vercel Deployment:
```bash
cd frontend
npm i -g vercel
vercel
```

### Railway Deployment:
```bash
cd backend
npm i -g @railway/cli
railway login
railway init
railway up
```

### Fly.io Deployment:
```bash
cd backend
fly launch
fly deploy
```

---

## 💡 Pro Tips

1. **Use GitHub Actions** for automated deployments
2. **Set up monitoring** (many platforms include basic monitoring)
3. **Use custom domains** (free SSL included on most platforms)
4. **Enable auto-deploy** from main branch
5. **Set up staging environment** for testing before production

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Fly.io Documentation](https://fly.io/docs)
- [Netlify Documentation](https://docs.netlify.com)

---

## 🆘 Need Help?

If you encounter issues:
1. Check platform-specific logs
2. Verify environment variables
3. Test locally first
4. Check platform status pages
5. Review platform documentation

**Remember**: Most free tiers have limitations. For production use, consider upgrading to paid tiers for better performance and reliability.

