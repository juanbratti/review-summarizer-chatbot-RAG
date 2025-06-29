# 🚀 REVI.AI Deployment Guide

This guide covers multiple ways to deploy your REVI.AI project to the internet.

## 📋 Prerequisites

- ✅ GitHub account
- ✅ OpenAI API key
- ✅ Git repository with your code

## 🌐 Deployment Options

### 🥇 **Option 1: Vercel + Railway (Recommended for Beginners)**

**Cost:** Free tier available  
**Difficulty:** ⭐⭐⭐  
**Best for:** Small to medium projects

#### Frontend Deployment (Vercel)

1. **Sign up to [Vercel](https://vercel.com)**
2. **Connect GitHub repository**
   - Click "New Project"
   - Import your GitHub repository
3. **Configure build settings:**
   - Framework Preset: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
4. **Add environment variables:**
   ```
   REACT_APP_API_URL=https://your-backend.railway.app
   ```
5. **Deploy:** Click "Deploy"

#### Backend Deployment (Railway)

1. **Sign up to [Railway](https://railway.app)**
2. **Create new project from GitHub**
3. **Configure service:**
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Add environment variables:**
   ```
   OPENAI_API_KEY=your_openai_api_key
   CORS_ORIGINS=https://your-frontend.vercel.app
   DEBUG=False
   APP_NAME=REVI.AI
   ```
5. **Deploy:** Railway will auto-deploy

### 🥈 **Option 2: Single Server (DigitalOcean/AWS/Linode)**

**Cost:** $5-20/month  
**Difficulty:** ⭐⭐⭐⭐  
**Best for:** Full control, custom domains

#### Server Setup

1. **Create a server** (Ubuntu 22.04 recommended)
2. **Connect via SSH:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install dependencies:**
   ```bash
   # Update system
   apt update && apt upgrade -y
   
   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   apt-get install -y nodejs
   
   # Install Python
   apt install -y python3 python3-pip python3-venv
   
   # Install Nginx
   apt install -y nginx
   
   # Install PM2 for process management
   npm install -g pm2
   ```

4. **Clone your repository:**
   ```bash
   git clone https://github.com/yourusername/review-summarizer-chatbot-RAG.git
   cd review-summarizer-chatbot-RAG
   ```

5. **Build frontend:**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

6. **Setup backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Copy environment file
   cp env.production.example .env
   # Edit .env with your actual values
   nano .env
   ```

7. **Configure Nginx:**
   ```bash
   nano /etc/nginx/sites-available/revi-ai
   ```
   
   Add this configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           root /root/review-summarizer-chatbot-RAG/frontend/build;
           try_files $uri $uri/ /index.html;
       }
       
       location /app/ {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

8. **Enable site and start services:**
   ```bash
   ln -s /etc/nginx/sites-available/revi-ai /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx
   
   # Start backend with PM2
   cd /root/review-summarizer-chatbot-RAG/backend
   source venv/bin/activate
   pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name revi-ai
   pm2 startup
   pm2 save
   ```

### 🥉 **Option 3: Docker Deployment**

**Cost:** Varies by platform  
**Difficulty:** ⭐⭐⭐⭐⭐  
**Best for:** Professional deployments, scaling

#### Local Testing

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8000
```

#### Deploy to Cloud Platforms

**Heroku:**
```bash
# Install Heroku CLI
heroku create your-app-name
heroku container:push web
heroku container:release web
heroku config:set OPENAI_API_KEY=your_key
```

**Google Cloud Run:**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/revi-ai
gcloud run deploy --image gcr.io/PROJECT-ID/revi-ai --platform managed
```

## 🔧 Configuration

### Frontend Environment Variables

Create `frontend/.env.production`:
```bash
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_APP_NAME=REVI.AI
```

### Backend Environment Variables

Copy `backend/env.production.example` to `backend/.env`:
```bash
# Required
OPENAI_API_KEY=your_openai_api_key
CORS_ORIGINS=https://your-frontend-domain.com

# Optional
DEBUG=False
APP_NAME=REVI.AI
```

## 🔒 Security Checklist

- [ ] **Environment variables** properly set
- [ ] **CORS origins** restricted to your domains
- [ ] **Debug mode** disabled in production
- [ ] **HTTPS** enabled (use Cloudflare or Let's Encrypt)
- [ ] **API keys** stored securely
- [ ] **File uploads** size-limited
- [ ] **Rate limiting** implemented (if needed)

## 🌐 Custom Domain Setup

### Vercel + Railway
1. **Vercel:** Project Settings → Domains → Add domain
2. **Railway:** Service Settings → Networking → Custom Domain
3. **Update CORS:** Add your custom domain to `CORS_ORIGINS`

### Single Server
1. **Point domain to server IP** (A record)
2. **Install SSL certificate:**
   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d your-domain.com
   ```

## 📊 Monitoring

### Basic Monitoring
- **Uptime:** [UptimeRobot](https://uptimerobot.com) (free)
- **Logs:** Check platform-specific logs
- **Performance:** Built-in platform metrics

### Advanced Monitoring
- **Application Performance:** Sentry
- **Infrastructure:** Datadog, New Relic
- **Custom metrics:** Prometheus + Grafana

## 🚨 Troubleshooting

### Common Issues

**CORS Errors:**
```bash
# Add your frontend domain to backend CORS_ORIGINS
CORS_ORIGINS=https://your-frontend.vercel.app
```

**Build Failures:**
```bash
# Ensure Node.js version compatibility
# Check package.json engines field
```

**API Connection Issues:**
```bash
# Verify API URL in frontend environment
REACT_APP_API_URL=https://your-backend.railway.app
```

**File Upload Issues:**
```bash
# Check upload directory permissions
mkdir -p uploads
chmod 755 uploads
```

## 💡 Optimization Tips

1. **Enable gzip compression** in Nginx
2. **Use CDN** for static assets (Cloudflare)
3. **Implement caching** for API responses
4. **Monitor API usage** and costs
5. **Set up automatic backups** for data
6. **Use environment-specific configs**

## 📞 Support

If you encounter issues:
1. Check the platform-specific documentation
2. Review error logs
3. Verify environment variables
4. Test API endpoints individually
5. Check CORS configuration

---

## 🎉 Quick Start Commands

```bash
# Test locally with Docker
docker-compose up --build

# Deploy to Railway (with CLI)
railway login
railway link
railway up

# Deploy to Vercel (with CLI)
npm i -g vercel
vercel --prod
```

Choose the deployment option that best fits your needs and technical expertise! 