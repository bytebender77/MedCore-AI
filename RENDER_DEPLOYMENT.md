# Render Deployment Guide

This guide will walk you through deploying your Pharmaceutical Agentic AI Research Platform to Render.

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- OpenAI API Key
- Google AI API Key

## Quick Deploy (Using render.yaml)

### Step 1: Push to GitHub

1. Make sure your code is pushed to a GitHub repository
2. Ensure all changes are committed:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

1. **Sign in to Render**: https://dashboard.render.com
2. **Click "New +"** → **"Blueprint"**
3. **Connect your GitHub repository**
4. **Select the repository** containing this project
5. **Render will automatically detect `render.yaml`**
6. **Click "Apply"** to create all services

This will create:
- ✅ Backend web service
- ✅ Frontend static site
- ✅ Redis instance (optional)

### Step 3: Configure Environment Variables

After deployment starts, configure your API keys:

1. Go to your **Backend service** dashboard
2. Navigate to **"Environment"** tab
3. Add the following environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```
4. Click **"Save Changes"** - this will trigger a redeploy

### Step 4: Update Frontend API URL

1. Go to your **Frontend service** dashboard
2. Navigate to **"Environment"** tab
3. Verify `REACT_APP_API_URL` is set (should be auto-configured)
4. If not, set it to your backend URL: `https://your-backend-name.onrender.com`

### Step 5: Wait for Deployment

- Backend typically takes 5-10 minutes for first deployment
- Frontend typically takes 3-5 minutes
- You'll see build logs in real-time

### Step 6: Verify Deployment

1. **Backend Health Check**: Visit `https://your-backend-name.onrender.com/health`
2. **API Docs**: Visit `https://your-backend-name.onrender.com/docs`
3. **Frontend**: Visit your frontend URL (shown in dashboard)

---

## Manual Deployment (Alternative Method)

If you prefer to set up services manually:

### Deploy Backend

1. **Click "New +"** → **"Web Service"**
2. **Connect GitHub** and select your repository
3. **Configure**:
   - **Name**: `pharma-ai-backend`
   - **Environment**: `Python 3`
   - **Region**: `Oregon` (or closest to you)
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables**:
   ```
   OPENAI_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   REDIS_URL=redis://your-redis-url (if using Redis)
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   PORT=10000
   ```
5. **Click "Create Web Service"**

### Deploy Frontend

1. **Click "New +"** → **"Static Site"**
2. **Connect GitHub** and select your repository
3. **Configure**:
   - **Name**: `pharma-ai-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
4. **Add Environment Variable**:
   ```
   REACT_APP_API_URL=https://your-backend-name.onrender.com
   ```
5. **Click "Create Static Site"**

### Deploy Redis (Optional)

1. **Click "New +"** → **"Redis"**
2. **Configure**:
   - **Name**: `pharma-ai-redis`
   - **Plan**: `Free`
3. **Copy the connection URL** and add it to your backend's `REDIS_URL` environment variable

---

## Important Notes

### Free Tier Limitations

- **Backend**: Services spin down after 15 minutes of inactivity
- **First request** after spin-down may take 30-60 seconds (cold start)
- **750 hours/month** total across all services
- **512MB RAM** per service

### Performance Tips

1. **Keep services warm**: Use a monitoring service (like UptimeRobot) to ping `/health` every 10 minutes
2. **Use external Redis**: Consider Upstash Redis for better performance
3. **Optimize builds**: Frontend builds are cached, but first build takes longer

### Environment Variables Reference

#### Backend Required:
```
OPENAI_API_KEY          # Your OpenAI API key
GOOGLE_API_KEY          # Your Google AI API key
```

#### Backend Optional:
```
REDIS_URL               # Redis connection string (default: localhost)
ENVIRONMENT             # production/development (default: production)
LOG_LEVEL               # DEBUG/INFO/WARNING/ERROR (default: INFO)
PORT                    # Server port (default: 8000, Render uses $PORT)
MAX_CONCURRENT_AGENTS   # Max parallel agents (default: 5)
```

#### Frontend Required:
```
REACT_APP_API_URL       # Backend API URL (e.g., https://backend.onrender.com)
```

---

## Troubleshooting

### Backend Issues

**Build fails with "Module not found":**
- Verify `requirements.txt` exists in `backend/` directory
- Check build logs for specific missing packages
- Ensure Python 3.8+ is being used

**Service won't start:**
- Check start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Verify `PORT` environment variable is set
- Check logs for specific error messages

**API keys not working:**
- Verify environment variables are set correctly
- Check for extra spaces or quotes in API keys
- Ensure variables are saved and service is redeployed

**CORS errors:**
- Backend already allows all origins (`allow_origins=["*"]`)
- If issues persist, verify frontend URL is correct

### Frontend Issues

**Build fails:**
- Check Node.js version (should be 18+)
- Verify all dependencies in `package.json`
- Check build logs for specific errors

**Cannot connect to backend:**
- Verify `REACT_APP_API_URL` is set correctly
- Ensure backend URL uses `https://` (not `http://`)
- Check backend is running and accessible

**Blank page after deployment:**
- Check browser console for errors
- Verify `REACT_APP_API_URL` is set
- Check build completed successfully

### General Issues

**Services keep spinning down:**
- This is normal for free tier
- First request after spin-down will be slow
- Consider using a keep-alive service

**Slow response times:**
- Free tier has limited resources
- Consider upgrading to paid tier for better performance
- Optimize your code and reduce dependencies

---

## Post-Deployment Checklist

- [ ] Backend health check returns `200 OK`
- [ ] Frontend loads without errors
- [ ] API calls from frontend work correctly
- [ ] Environment variables are set
- [ ] SSL certificates are active (automatic on Render)
- [ ] Custom domain configured (optional)
- [ ] Monitoring/keep-alive set up (optional)

---

## Updating Your Deployment

### Automatic Updates

Render automatically deploys when you push to your connected branch (usually `main`).

### Manual Updates

1. Go to your service dashboard
2. Click **"Manual Deploy"**
3. Select branch and click **"Deploy latest commit"**

### Rollback

1. Go to your service dashboard
2. Click **"Events"** tab
3. Find previous successful deployment
4. Click **"Redeploy"**

---

## Custom Domain Setup

1. Go to your service dashboard
2. Click **"Settings"** tab
3. Scroll to **"Custom Domains"**
4. Click **"Add Custom Domain"**
5. Follow DNS configuration instructions
6. SSL certificate is automatically provisioned

---

## Monitoring & Logs

### View Logs

1. Go to your service dashboard
2. Click **"Logs"** tab
3. View real-time and historical logs

### Health Checks

Render automatically checks `/health` endpoint. Ensure it returns:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "usage_stats": {...}
}
```

---

## Cost Estimation

### Free Tier (Current)
- **Backend**: Free (750 hours/month)
- **Frontend**: Free (unlimited)
- **Redis**: Free (25MB)
- **Total**: $0/month

### Paid Tier (If Needed)
- **Backend Starter**: $7/month (always on, 512MB RAM)
- **Frontend**: Still free
- **Redis**: $10/month (100MB)
- **Total**: ~$17/month

---

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Render Status**: https://status.render.com

---

## Next Steps

After successful deployment:

1. ✅ Test all features
2. ✅ Set up monitoring/keep-alive
3. ✅ Configure custom domain (optional)
4. ✅ Set up CI/CD (already automatic with Render)
5. ✅ Review and optimize performance

Your application is now live! 🚀

