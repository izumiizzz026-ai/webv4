# QR Attendance System - Unified Deployment Guide

This guide explains how to deploy the QR Attendance system so that **both the web application and desktop EXE share the same backend and database**.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLOUD SERVER                             │
│  ┌─────────────────┐    ┌─────────────────────────────────┐    │
│  │   PostgreSQL    │◄───│   Flask Backend (Gunicorn)      │    │
│  │   Database      │    │   https://your-app.railway.app  │    │
│  └─────────────────┘    └─────────────┬───────────────────┘    │
└───────────────────────────────────────┼─────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
            ┌───────▼───────┐                     ┌─────────▼────────┐
            │  WEB BROWSER  │                     │  DESKTOP APP     │
            │  (Teachers,   │                     │  (QRAttendance   │
            │   Students)   │                     │   .exe)          │
            └───────────────┘                     └──────────────────┘
```

## Deployment Options

### Option A: Railway (Recommended - Free Tier Available)
### Option B: Render
### Option C: Heroku
### Option D: Self-hosted VPS

---

## Step 1: Prepare for Production

### 1.1 Create Production Requirements

The `requirements.txt` already includes production dependencies:
- `gunicorn` - Production WSGI server
- `psycopg2-binary` - PostgreSQL driver

### 1.2 Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `FLASK_SECRET_KEY` | Secure random key (32+ chars) | `your-super-secret-key-here-make-it-long` |
| `FLASK_ENV` | Environment mode | `production` |

---

## Step 2: Deploy to Railway (Recommended)

### 2.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### 2.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Connect your QR Attendance repository

### 2.3 Add PostgreSQL Database
1. In your project, click **"+ New"**
2. Select **"Database" → "PostgreSQL"**
3. Railway auto-sets `DATABASE_URL`

### 2.4 Configure Environment Variables
In Railway dashboard → Variables, add:
```
FLASK_SECRET_KEY=your-secure-random-key-32-chars-minimum
FLASK_ENV=production
```

### 2.5 Configure Start Command
Railway will auto-detect Python. Add a `Procfile`:

---

## Step 3: Production Configuration Files

I'll create these files for you:

1. **Procfile** - Tells cloud platforms how to run the app
2. **runtime.txt** - Specifies Python version  
3. **Updated desktop_config.json** - Points desktop to cloud server

---

## Step 4: Desktop App Configuration

The desktop app can run in two modes:

### Mode 1: Online Mode (Connects to Cloud Server)
Edit `desktop_config.json`:
```json
{
  "server_url": "https://your-app.railway.app",
  "mode": "online"
}
```

### Mode 2: Offline Mode (Local Server + SQLite)
```json
{
  "server_url": "http://localhost:5000",
  "mode": "offline"
}
```

---

## Step 5: Database Migrations

Since both web and desktop share the same cloud database:

1. **Initial Setup**: The first deployment runs `db.create_all()`
2. **Schema Changes**: Use Flask-Migrate for production changes

---

## Quick Deploy Commands

### Railway CLI Deployment
```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Local Testing with Production DB
```powershell
$env:DATABASE_URL = "postgresql://user:pass@host:5432/dbname"
$env:FLASK_SECRET_KEY = "test-key"
python app.py
```

---

## Security Checklist

- [ ] Set strong `FLASK_SECRET_KEY` (32+ random characters)
- [ ] Use HTTPS only in production
- [ ] Change default admin password after first login
- [ ] Enable database connection SSL
- [ ] Set `debug=False` in production

