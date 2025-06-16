#!/bin/bash

# GitHub Repository Setup Script for AI Video Generation Platform
# This script initializes a Git repository and pushes to GitHub

echo "🚀 Setting up GitHub repository for AI Video Generation Platform..."

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Add all files to staging
echo "📁 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: AI Video Generation Platform v2.0.0

Features:
- Professional AI video generation with FLUX models
- Advanced visual effects (particles, lighting, cinematic post-processing)
- Viral-ready hooks with content-aware text overlays
- 10-second videos at 1024x1024 resolution
- Real motion sequences with multiple AI frames
- Background music generation
- Flask web interface with galleries
- Complete documentation and setup guides"

# Set up GitHub remote (you'll need to replace with your actual repository URL)
echo "🔗 Setting up GitHub remote..."
echo "Please create a repository on GitHub first, then run:"
echo "git remote add origin https://github.com/yourusername/ai-video-generator.git"
echo "git branch -M main"
echo "git push -u origin main"

echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Copy the repository URL"
echo "3. Run: git remote add origin YOUR_REPO_URL"
echo "4. Run: git branch -M main"
echo "5. Run: git push -u origin main"
echo ""
echo "✨ Repository setup complete!"