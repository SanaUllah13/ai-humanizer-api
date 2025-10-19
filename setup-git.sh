#!/bin/bash

# AI Humanizer - GitHub Setup Helper Script
# This script helps you push your code to GitHub

echo "🚀 AI Humanizer - GitHub Setup"
echo "================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    echo "Visit: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ GitHub username cannot be empty"
    exit 1
fi

# Get repository name (default: ai-humanizer-api)
read -p "Enter repository name (press Enter for 'ai-humanizer-api'): " repo_name
repo_name=${repo_name:-ai-humanizer-api}

echo ""
echo "📝 Summary:"
echo "  GitHub Username: $github_username"
echo "  Repository Name: $repo_name"
echo "  Repository URL: https://github.com/$github_username/$repo_name"
echo ""

read -p "Is this correct? (y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Setup cancelled"
    exit 1
fi

echo ""
echo "🔧 Setting up Git repository..."
echo ""

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized"
fi

# Create .gitignore
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.DS_Store
*.log
.env
*.egg-info
dist/
build/
EOF
echo "✅ .gitignore created"

# Add all files
git add .
echo "✅ Files staged"

# Commit
git commit -m "Initial commit - AI Text Humanizer"
echo "✅ Initial commit created"

# Add remote
git remote remove origin 2>/dev/null  # Remove if exists
git remote add origin "https://github.com/$github_username/$repo_name.git"
echo "✅ Remote repository added"

# Set branch name to main
git branch -M main
echo "✅ Branch renamed to main"

echo ""
echo "📤 Ready to push to GitHub!"
echo ""
echo "⚠️  IMPORTANT: Before running the next command:"
echo "   1. Go to https://github.com/new"
echo "   2. Create a repository named: $repo_name"
echo "   3. Leave it EMPTY (don't add README or .gitignore)"
echo "   4. Press Enter here when done"
echo ""
read -p "Press Enter when you've created the GitHub repository..."

echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ✅ ✅ SUCCESS! ✅ ✅ ✅"
    echo ""
    echo "Your code is now on GitHub:"
    echo "https://github.com/$github_username/$repo_name"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Go to https://render.com and sign up"
    echo "  2. Click 'New +' → 'Web Service'"
    echo "  3. Connect your GitHub repository: $repo_name"
    echo "  4. Follow the steps in HOSTINGER-DEPLOYMENT.md"
    echo ""
    echo "See DEPLOYMENT-STEPS.md for a complete checklist!"
else
    echo ""
    echo "❌ Failed to push to GitHub"
    echo ""
    echo "Possible solutions:"
    echo "  1. Make sure you created the repository on GitHub"
    echo "  2. Check your GitHub credentials"
    echo "  3. Try running manually: git push -u origin main"
fi
