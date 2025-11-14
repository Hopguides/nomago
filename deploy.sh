#!/bin/bash
# Nomago Monitor - Railway Deployment Helper

set -e

echo "🚲 Nomago Railway Monitor - Deployment Helper"
echo "=============================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found"
    echo "📦 Install: npm install -g @railway/cli"
    echo "🔗 Docs: https://docs.railway.app/develop/cli"
    exit 1
fi

echo "✅ Railway CLI found"
echo ""

# Main menu
echo "Choose an option:"
echo "1. Test locally (JSON fallback)"
echo "2. Test with local PostgreSQL"
echo "3. Deploy to Railway"
echo "4. View Railway logs"
echo "5. Connect to Railway PostgreSQL"
echo "6. Check Railway status"
echo ""
read -p "Enter option (1-6): " option

case $option in
    1)
        echo ""
        echo "🧪 Testing locally with JSON fallback..."
        python3 monitor.py
        echo ""
        echo "📁 Check: nomago_history.json"
        ;;
    2)
        echo ""
        read -p "Enter DATABASE_URL: " db_url
        export DATABASE_URL="$db_url"
        echo "🧪 Testing with PostgreSQL..."
        python3 monitor.py
        ;;
    3)
        echo ""
        echo "🚂 Deploying to Railway..."

        # Check if requirements.txt exists
        if [ ! -f "requirements.txt" ]; then
            echo "❌ requirements.txt not found"
            exit 1
        fi

        # Check if monitor.py exists
        if [ ! -f "monitor.py" ]; then
            echo "❌ monitor.py not found"
            exit 1
        fi

        echo "📦 Files ready:"
        ls -lh monitor.py requirements.txt Procfile railway.json 2>/dev/null
        echo ""

        read -p "Deploy to Railway? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            railway up
            echo ""
            echo "✅ Deployment complete!"
            echo "📊 View logs: railway logs"
            echo "🌐 View dashboard: railway open"
        else
            echo "❌ Deployment cancelled"
        fi
        ;;
    4)
        echo ""
        echo "📊 Viewing Railway logs..."
        railway logs --tail 50
        ;;
    5)
        echo ""
        echo "🔗 Connecting to Railway PostgreSQL..."
        railway connect postgres
        ;;
    6)
        echo ""
        echo "📊 Railway status..."
        railway status
        echo ""
        echo "🔧 Environment variables:"
        railway variables
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"
