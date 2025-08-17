#!/bin/bash

# Grow Plants Game - Cloudflare Workers Deployment Script

echo "🌱 Deploying Grow Plants Game to Cloudflare Workers..."
echo "=================================================="

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI not found!"
    echo "Please install it first: npm install -g wrangler"
    exit 1
fi

# Check if user is logged in
if ! wrangler whoami &> /dev/null; then
    echo "❌ Not logged in to Cloudflare!"
    echo "Please run: wrangler login"
    exit 1
fi

echo "✅ Wrangler CLI found and logged in"
echo "🚀 Starting deployment..."

# Deploy to Cloudflare Workers
if wrangler deploy; then
    echo ""
    echo "🎉 Deployment successful!"
    echo "Your game should now be available at the URL shown above."
    echo ""
    echo "📱 You can now:"
    echo "• Play the game in any web browser"
    echo "• Share the URL with friends and family"
    echo "• Access it from any device with internet"
    echo ""
    echo "🌱 Happy gardening!"
else
    echo ""
    echo "❌ Deployment failed!"
    echo "Please check the error messages above and try again."
    exit 1
fi
