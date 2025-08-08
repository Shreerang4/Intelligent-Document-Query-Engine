#!/bin/bash

echo "=== Deploying Updated RAG API to Railway ==="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root."
    exit 1
fi

echo "✅ Found main.py"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

echo "✅ Railway CLI found"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Test the health endpoint: https://bajajhack-production-cf2c.up.railway.app/health"
echo "2. Run the hackathon test: python test_hackathon.py"
echo "3. Or use PowerShell: .\test_hackathon.ps1"
echo ""
echo "🔧 The application now supports up to 10 questions for hackathon requirements." 