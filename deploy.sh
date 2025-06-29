#!/bin/bash

# REVI.AI Deployment Helper Script - Vercel + Railway
# This script helps prepare your project for Vercel + Railway deployment

echo "🚀 REVI.AI Deployment Helper - Vercel + Railway"
echo "=================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
echo ""
echo "📋 Checking prerequisites..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_error "Git repository not found. Please initialize git first:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    echo "  git remote add origin https://github.com/yourusername/your-repo.git"
    echo "  git push -u origin main"
    exit 1
fi

# Check if OpenAI API key is set
if [ -f "backend/.env" ]; then
    if grep -q "OPENAI_API_KEY=your_openai_api_key_here" backend/.env; then
        print_warning "OpenAI API key not set in backend/.env"
        echo "Please update backend/.env with your actual OpenAI API key"
    else
        print_status "Environment file exists"
    fi
else
    print_warning "Backend environment file not found"
    echo "Copying example environment file..."
    cp backend/env.production.example backend/.env
    print_info "Please edit backend/.env and set your actual values"
fi

# Check Node.js version
if command -v node >/dev/null 2>&1; then
    NODE_VERSION=$(node --version)
    print_status "Node.js $NODE_VERSION found"
else
    print_error "Node.js not found. Please install Node.js 16 or higher"
    exit 1
fi

# Check Python version
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version)
    print_status "$PYTHON_VERSION found"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi

# Build frontend for production
echo ""
echo "🏗️  Building frontend..."
cd frontend
if [ -f "package.json" ]; then
    print_info "Installing frontend dependencies..."
    npm install
    
    print_info "Building React app for production..."
    npm run build
    
    if [ -d "build" ]; then
        print_status "Frontend build completed successfully"
    else
        print_error "Frontend build failed"
        exit 1
    fi
else
    print_error "Frontend package.json not found"
    exit 1
fi

cd ..

# Test backend setup
echo ""
echo "🐍 Testing backend setup..."
cd backend

if [ -f "requirements.txt" ]; then
    print_info "Backend requirements found"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    print_info "Activating virtual environment and installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    print_status "Backend setup completed"
else
    print_error "Backend requirements.txt not found"
    exit 1
fi

cd ..

# Check git status
echo ""
echo "📝 Checking git status..."
if git diff --quiet && git diff --staged --quiet; then
    print_status "All changes are committed"
else
    print_warning "You have uncommitted changes"
    echo "Do you want to commit and push them now? (y/n)"
    read -r commit_choice
    if [ "$commit_choice" = "y" ] || [ "$commit_choice" = "Y" ]; then
        git add .
        git commit -m "Prepare for Vercel + Railway deployment"
        git push
        print_status "Changes committed and pushed"
    else
        print_info "Please commit and push your changes before deploying"
    fi
fi

# Show deployment steps
echo ""
echo "🌐 Vercel + Railway Deployment Steps:"
echo "====================================="
echo ""
echo "🎯 Step 1: Push to GitHub"
print_status "✅ Your code should be on GitHub now"
echo ""

echo "🎨 Step 2: Deploy Frontend to Vercel"
echo "1. Go to https://vercel.com and sign up/login"
echo "2. Click 'New Project' and import your GitHub repository"
echo "3. Configure:"
echo "   - Framework: Create React App"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: build"
echo "4. Add environment variable:"
echo "   REACT_APP_API_URL = https://your-backend.railway.app"
echo "   (You'll get this URL in Step 3)"
echo "5. Click Deploy"
echo ""

echo "🚂 Step 3: Deploy Backend to Railway"
echo "1. Go to https://railway.app and sign up/login"
echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
echo "3. Select your repository"
echo "4. Configure:"
echo "   - Root Directory: backend"
echo "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "5. Add environment variables:"
echo "   OPENAI_API_KEY = your_actual_openai_api_key"
echo "   CORS_ORIGINS = https://your-project.vercel.app"
echo "   DEBUG = False"
echo "   APP_NAME = REVI.AI"
echo "6. Deploy"
echo ""

echo "🔗 Step 4: Connect Frontend and Backend"
echo "1. Copy your Railway backend URL"
echo "2. Go back to Vercel project settings"
echo "3. Update REACT_APP_API_URL with Railway URL"
echo "4. Update Railway CORS_ORIGINS with Vercel URL"
echo "5. Test your deployment!"
echo ""

echo "📚 Need detailed help?"
echo "Check DEPLOYMENT_GUIDE.md for step-by-step instructions with screenshots"
echo ""

# Ask if user wants to open the deployment guide
echo "Would you like to:"
echo "1) Open the deployment guide"
echo "2) Open Vercel in browser"
echo "3) Open Railway in browser"
echo "4) Exit"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        print_info "Opening deployment guide..."
        if command -v code >/dev/null 2>&1; then
            code DEPLOYMENT_GUIDE.md
        elif command -v xdg-open >/dev/null 2>&1; then
            xdg-open DEPLOYMENT_GUIDE.md
        else
            echo "Please read DEPLOYMENT_GUIDE.md for detailed instructions"
        fi
        ;;
    2)
        print_info "Opening Vercel..."
        if command -v xdg-open >/dev/null 2>&1; then
            xdg-open https://vercel.com
        else
            echo "Please visit: https://vercel.com"
        fi
        ;;
    3)
        print_info "Opening Railway..."
        if command -v xdg-open >/dev/null 2>&1; then
            xdg-open https://railway.app
        else
            echo "Please visit: https://railway.app"
        fi
        ;;
    4)
        print_info "Exiting..."
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_status "Setup completed! Your app is ready for Vercel + Railway deployment."
echo ""
echo "🎉 Next steps:"
echo "1. Deploy to Vercel (frontend)"
echo "2. Deploy to Railway (backend)"
echo "3. Connect them together"
echo "4. Share your REVI.AI chatbot with the world!" 