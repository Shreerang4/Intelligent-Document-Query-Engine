# Manual Deployment Guide

Since Railway CLI is not available, here are the steps to deploy your updated application:

## Method 1: Railway Web Interface (Recommended)

1. **Go to Railway Dashboard**
   - Visit: https://railway.app/dashboard
   - Sign in to your account

2. **Find Your Project**
   - Look for project: `bajajhack-production-cf2c`
   - Click on the project

3. **Update Files**
   - Go to the "Settings" tab
   - Look for "Source" or "Repository" section
   - If connected to GitHub, push your changes to the repository
   - If not, you can manually update the files through the Railway interface

4. **Deploy**
   - Railway will automatically detect changes and deploy
   - Or click "Deploy" button if available

## Method 2: Install Railway CLI

1. **Install Node.js**
   - Download from: https://nodejs.org/
   - Install the LTS version

2. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

3. **Login to Railway**
   ```bash
   railway login
   ```

4. **Deploy**
   ```bash
   railway up
   ```

## Method 3: GitHub Integration

If your Railway project is connected to GitHub:

1. **Commit Changes**
   ```bash
   git add .
   git commit -m "Updated to support 10 questions for hackathon"
   git push origin main
   ```

2. **Railway Auto-Deploy**
   - Railway will automatically detect the push and deploy

## Key Changes Made

The main changes that need to be deployed:

1. **main.py**: Updated to support 10 questions instead of 5
2. **test_hackathon.py**: New test file with 10 questions
3. **test_hackathon.ps1**: PowerShell test script
4. **README.md**: Updated documentation

## After Deployment

Once deployed, test the system:

```bash
python test_hackathon.py
```

Or with PowerShell:
```powershell
.\test_hackathon.ps1
```

## Expected Results

After successful deployment, you should see:
- ✅ Health check passes
- ✅ API accepts 10 questions
- ✅ All 10 questions processed successfully
- ✅ Performance metrics displayed

## Troubleshooting

If you encounter issues:

1. **Check Railway Logs**: View deployment logs in Railway dashboard
2. **Verify Changes**: Ensure all updated files are deployed
3. **Test Health Endpoint**: https://bajajhack-production-cf2c.up.railway.app/health
4. **Check API Response**: Look for the new 10-question limit message 