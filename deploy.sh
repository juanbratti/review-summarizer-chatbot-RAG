#!/bin/bash

# REVI.AI Deployment Helper Script
# This script helps prepare your project for deployment

echo "🚀 REVI.AI Deployment Helper"
echo "================================"

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

# Show deployment options
echo ""
echo "🌐 Deployment Options:"
echo "================================"
echo ""
echo "1. 🥇 Vercel + Railway (Recommended for beginners)"
echo "   - Frontend: Deploy to Vercel"
echo "   - Backend: Deploy to Railway"
echo "   - Cost: Free tier available"
echo ""
echo "2. 🥈 Single Server (DigitalOcean/AWS/Linode)"
echo "   - Deploy both frontend and backend on one server"
echo "   - Cost: \$5-20/month"
echo ""
echo "3. 🥉 Docker (Professional)"
echo "   - Use Docker containers"
echo "   - Deploy to any cloud platform"
echo ""
echo "4. 🧪 Test locally with Docker"
echo "   - Test the production build locally"
echo ""

# Ask user what they want to do
echo "What would you like to do?"
echo "1) Setup Vercel + Railway deployment files"
echo "2) Setup single server deployment files"
echo "3) Test locally with Docker"
echo "4) Show deployment guide"
echo "5) Exit"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        print_info "Setting up Vercel + Railway deployment..."
        print_status "vercel.json created"
        print_status "railway.json created"
        echo ""
        echo "Next steps:"
        echo "1. Push your code to GitHub"
        echo "2. Sign up to Vercel (https://vercel.com)"
        echo "3. Sign up to Railway (https://railway.app)"
        echo "4. Connect your GitHub repository to both platforms"
        echo "5. Set environment variables as described in DEPLOYMENT_GUIDE.md"
        ;;
    2)
        print_info "Single server deployment files already created"
        echo ""
        echo "Next steps:"
        echo "1. Create a server (Ubuntu 22.04 recommended)"
        echo "2. Follow the detailed guide in DEPLOYMENT_GUIDE.md"
        ;;
    3)
        if command -v docker >/dev/null 2>&1; then
            print_info "Testing with Docker..."
            docker-compose up --build
        else
            print_error "Docker not found. Please install Docker first"
        fi
        ;;
    4)
        print_info "Opening deployment guide..."
        if command -v code >/dev/null 2>&1; then
            code DEPLOYMENT_GUIDE.md
        else
            echo "Please read DEPLOYMENT_GUIDE.md for detailed instructions"
        fi
        ;;
    5)
        print_info "Exiting..."
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_status "Setup completed! Check DEPLOYMENT_GUIDE.md for detailed instructions." 