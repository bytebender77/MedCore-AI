# Frontend Deployment Fix for Render

## Problem
Build command is empty, so the build never runs, and the `build` directory doesn't exist.

## Solution

### Update Render Static Site Settings

Go to your `pharma-ai-frontend` service settings and update:

1. **Root Directory**: `frontend`
   - This tells Render where your frontend code is

2. **Build Command**: 
   ```
   npm install && npm run build
   ```
   - **IMPORTANT**: Make sure this field is NOT empty
   - This installs dependencies and builds the React app

3. **Publish Directory**: `build`
   - Since Root Directory is `frontend`, the build output will be in `frontend/build/`
   - But Publish Directory should be `build` (relative to the root directory `frontend`)

### Step-by-Step Fix

1. Go to your Render dashboard
2. Click on `pharma-ai-frontend` service
3. Click **"Settings"** tab
4. Scroll to **"Build & Deploy"** section
5. Verify/Update:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build` (MUST NOT BE EMPTY)
   - **Publish Directory**: `build`
6. Scroll to **"Environment"** section
7. Verify **Environment Variable**:
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-backend-name.onrender.com` (your actual backend URL)
8. Click **"Save Changes"**
9. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Alternative: If Publish Directory doesn't work

If `build` doesn't work, try:
- **Publish Directory**: `frontend/build` (relative to repo root)

But typically, if Root Directory is `frontend`, then Publish Directory should be `build`.

### Verify Build Command

The build command should:
1. Install all npm packages
2. Run the React build script
3. Create the `build` directory with production files

You can test locally:
```bash
cd frontend
npm install && npm run build
ls build  # Should show built files
```

### Common Issues

**Issue**: "Empty build command"
- **Fix**: Make sure Build Command field has: `npm install && npm run build`

**Issue**: "Publish directory does not exist"
- **Fix**: Make sure Build Command ran successfully first
- Check build logs to see if build completed

**Issue**: Build fails
- Check build logs for specific errors
- Verify `package.json` exists in `frontend/` directory
- Verify Node.js version (should be 18+)

### Expected Build Output

After successful build, you should see in logs:
```
Creating an optimized production build...
Compiled successfully!
```

And the `build` directory should contain:
- `index.html`
- `static/` folder with JS and CSS files
- Other assets

### After Fix

Once the build succeeds:
1. Your frontend will be live at: `https://pharma-ai-frontend.onrender.com`
2. It will connect to your backend using `REACT_APP_API_URL`
3. You can test by visiting the URL

