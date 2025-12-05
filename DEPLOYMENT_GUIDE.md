# 🚀 Deployment Guide

This guide will help you deploy the **MedCore Research Platform** to production using **Render** (Backend) and **Vercel** (Frontend).

---

## 1. Prerequisites
- A **GitHub** account.
- A **Render** account (render.com).
- A **Vercel** account (vercel.com).
- Your project pushed to a GitHub repository.

---

## 2. Backend Deployment (Render)

1.  Log in to **Render Dashboard**.
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  **Configuration:**
    *   **Name:** `pharma-ai-backend` (or similar)
    *   **Region:** Oregon (US West) or closest to you.
    *   **Branch:** `main`
    *   **Root Directory:** `.` (Leave empty or dot)
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r backend/requirements.txt`
    *   **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables:**
    Add the following keys (copy from your local `.env` or `config.py`):
    *   `OPENAI_API_KEY`: `sk-...`
    *   `GROQ_API_KEY`: `gsk_...`
    *   `LENS_API_KEY`: `LUzu...`
    *   `COMTRADE_API_KEY`: `d4bc...`
    *   `ENVIRONMENT`: `production`
    *   `DATA_MODE`: `real` (or `mock` if you want to test without API costs)
6.  Click **Create Web Service**.
7.  **Wait for Deployment:** Once live, copy the **Backend URL** (e.g., `https://pharma-ai-backend.onrender.com`).

---

## 3. Frontend Deployment (Vercel)

1.  Log in to **Vercel Dashboard**.
2.  Click **Add New...** -> **Project**.
3.  Import your GitHub repository.
4.  **Framework Preset:** Select **Create React App**.
5.  **Root Directory:** Click `Edit` and select `frontend`.
6.  **Environment Variables:**
    *   `REACT_APP_API_URL`: Paste your **Render Backend URL** (e.g., `https://pharma-ai-backend.onrender.com`).
        *   *Note: Do NOT add a trailing slash `/`.*
7.  Click **Deploy**.

---

## 4. Verification

1.  Open your Vercel URL (e.g., `https://medcore-platform.vercel.app`).
2.  Try a sample query like "Patents for CRISPR".
3.  If it works, congratulations! Your multi-agent platform is live. 🚀

---

## Troubleshooting

*   **Backend 500 Error:** Check Render logs. Ensure all API keys are set correctly.
*   **Frontend Connection Error:** Ensure `REACT_APP_API_URL` in Vercel matches the Render URL exactly (https, no trailing slash).
*   **"ModuleNotFoundError: groq":** Ensure `groq` is in `backend/requirements.txt` (it is).
