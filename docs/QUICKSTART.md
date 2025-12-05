# Quick Start Guide

This guide will help you get the Pharmaceutical Agentic AI Research Platform up and running quickly.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (check with `python3 --version`)
- **Node.js 18+** and **npm** (check with `node --version` and `npm --version`)
- **OpenAI API Key** (get one at https://platform.openai.com/api-keys)
- **Google AI API Key** (get one at https://makersuite.google.com/app/apikey)

## Step 1: Environment Setup

### Backend Environment Variables

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file:
   ```bash
   touch .env
   ```

3. Add your API keys to the `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Optional: Configure other settings
   REDIS_URL=redis://localhost:6379
   ENVIRONMENT=development
   LOG_LEVEL=INFO
   MAX_CONCURRENT_AGENTS=5
   DEFAULT_OPENAI_MODEL=gpt-4o-mini
   DEFAULT_GEMINI_MODEL=gemini-2.5-flash
   ```

### Frontend Environment Variables (Optional)

The frontend will work with default settings, but you can customize:

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create a `.env` file (optional):
   ```bash
   touch .env
   ```

3. Add configuration if needed:
   ```env
   REACT_APP_API_URL=http://localhost:8000
   PORT=3000
   ```

## Step 2: Install Dependencies

### Backend Dependencies

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

   Or if you prefer using a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Frontend Dependencies

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Step 3: Run the Application

### Option A: Run Both Services (Recommended)

Open **two separate terminal windows/tabs**:

#### Terminal 1 - Backend:
```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm start
```

The frontend will automatically open in your browser at `http://localhost:3000`.

### Option B: Run in Background (Alternative)

You can also run both services in the background:

```bash
# Backend
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

# Frontend
cd frontend
npm start &
```

## Step 4: Verify Installation

### Check Backend

1. Open your browser and visit: `http://localhost:8000/health`
   - You should see a JSON response with `"status": "healthy"`

2. Visit the API documentation: `http://localhost:8000/docs`
   - This is the interactive Swagger UI for testing the API

### Check Frontend

1. The frontend should automatically open at: `http://localhost:3000`
   - If not, manually navigate to this URL

2. You should see the Pharmaceutical Agentic AI interface

## Step 5: Test the Application

1. **Test Backend API:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test from Frontend:**
   - Enter a query in the frontend interface
   - Select your preferred AI provider (OpenAI or Gemini)
   - Submit the query and wait for results

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Module not found errors:**
```bash
# Make sure you're in the backend directory and dependencies are installed
cd backend
pip3 install -r requirements.txt
```

**API Key errors:**
- Verify your `.env` file exists in the `backend` directory
- Check that API keys are correctly formatted (no quotes, no extra spaces)
- Ensure API keys are valid and have sufficient credits

### Frontend Issues

**Port 3000 already in use:**
```bash
# The frontend will prompt you to use a different port
# Or set PORT in .env file
PORT=3001 npm start
```

**Cannot connect to backend:**
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` in frontend `.env` file
- Ensure CORS is enabled (it should be by default)

**Node modules errors:**
```bash
# Delete node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### General Issues

**Both services won't start:**
- Check if Python 3.8+ and Node.js 18+ are installed
- Verify you're in the correct directories
- Check terminal output for specific error messages

**API calls failing:**
- Verify API keys are set correctly in `backend/.env`
- Check API key quotas and billing status
- Review backend logs for detailed error messages

## Stopping the Services

### To stop the services:

1. **If running in foreground:**
   - Press `Ctrl+C` in each terminal window

2. **If running in background:**
   ```bash
   # Find and kill backend process
   lsof -ti:8000 | xargs kill -9
   
   # Find and kill frontend process
   lsof -ti:3000 | xargs kill -9
   ```

## Deployment

### Deploy to Render (Recommended - Free)

This project is ready to deploy to Render with one click!

1. **Push your code to GitHub**
2. **Sign up at [Render.com](https://render.com)**
3. **Click "New +" → "Blueprint"**
4. **Connect your GitHub repository**
5. **Render will auto-detect `render.yaml` and deploy everything**

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.

### Other Deployment Options

See [FREE_DEPLOYMENT_GUIDE.md](FREE_DEPLOYMENT_GUIDE.md) for other free hosting options.

## Next Steps

- Read the [User Guide](docs/USER_GUIDE.md) for detailed usage instructions
- Check the [Architecture Documentation](docs/ARCHITECTURE.md) to understand the system design
- Review the [API Documentation](docs/API.md) for API endpoints
- Deploy to production using [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

## Quick Reference

| Service | Port | URL | Command |
|---------|------|-----|---------|
| Backend API | 8000 | http://localhost:8000 | `python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` |
| API Docs | 8000 | http://localhost:8000/docs | (Auto-generated) |
| Frontend | 3000 | http://localhost:3000 | `npm start` |

## Need Help?

- Check the logs in `backend/logs/` for backend errors
- Review browser console (F12) for frontend errors
- Ensure all prerequisites are installed correctly
- Verify environment variables are set properly

