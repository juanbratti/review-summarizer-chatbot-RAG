# 🚀 REVI.AI Deployment Guide - Vercel + Railway

This guide covers deploying your REVI.AI project to the internet using **Vercel** (frontend) and **Railway** (backend).

## 📋 Prerequisites

- ✅ GitHub account
- ✅ OpenAI API key
- ✅ Git repository with your code pushed to GitHub

## 🌐 Vercel + Railway Deployment

**Cost:** Free tier available  
**Difficulty:** ⭐⭐⭐ (Beginner-friendly)  
**Best for:** Small to medium projects, getting started quickly

### 🎯 **Step 1: Push Your Code to GitHub**

Make sure all your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Ready for deployment"
git push origin main  # or your main branch name
```

### 🎨 **Step 2: Deploy Frontend to Vercel**

1. **Sign up to [Vercel](https://vercel.com)**
   - Use your GitHub account for easy integration

2. **Create New Project**
   - Click "New Project" on your Vercel dashboard
   - Import your GitHub repository
   - Select your `review-summarizer-chatbot-RAG` repository

3. **Configure Build Settings:**
   - **Framework Preset:** `Create React App`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `build` (auto-detected)

4. **Add Environment Variables:**
   - Go to "Environment Variables" section
   - Add: `REACT_APP_API_URL` = `https://your-backend.railway.app` 
   - ⚠️ **Note:** You'll get the Railway URL in Step 3, so you can add this later

5. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - You'll get a URL like: `https://your-project.vercel.app`

### 🚂 **Step 3: Deploy Backend to Railway**

1. **Sign up to [Railway](https://railway.app)**
   - Use your GitHub account for easy integration

2. **Create New Project**
   - Click "New Project" on Railway dashboard
   - Select "Deploy from GitHub repo"
   - Choose your `review-summarizer-chatbot-RAG` repository

3. **Configure Service Settings:**
   - Railway will auto-detect it's a Python project
   - **Root Directory:** `backend`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Build Command:** `pip install -r requirements.txt`

4. **Add Environment Variables:**
   ```bash
   OPENAI_API_KEY=your_actual_openai_api_key_here
   CORS_ORIGINS=https://your-frontend.vercel.app
   DEBUG=False
   APP_NAME=REVI.AI
   APP_VERSION=1.0.0
   ```

5. **Deploy**
   - Railway will automatically deploy your backend
   - You'll get a URL like: `https://your-project.railway.app`

### 🔗 **Step 4: Connect Frontend and Backend**

1. **Update Frontend Environment Variable:**
   - Go back to your Vercel project settings
   - Update `REACT_APP_API_URL` with your Railway backend URL
   - Redeploy the frontend (Vercel will do this automatically)

2. **Update Backend CORS:**
   - In Railway, update the `CORS_ORIGINS` environment variable
   - Set it to your Vercel frontend URL: `https://your-project.vercel.app`

### ✅ **Step 5: Test Your Deployment**

1. **Visit your Vercel URL**
2. **Test the chat interface**
3. **Upload a file and ask questions**
4. **Verify everything works correctly**

## 🔧 **Environment Variables Reference**

### Frontend (Vercel)
```bash
REACT_APP_API_URL=https://your-backend.railway.app
```

### Backend (Railway)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
CORS_ORIGINS=https://your-frontend.vercel.app

# Optional
DEBUG=False
APP_NAME=REVI.AI
APP_VERSION=1.0.0
```

## 🌐 **Custom Domain Setup (Optional)**

### Vercel Custom Domain
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### Railway Custom Domain
1. Go to Service Settings → Networking
2. Add custom domain
3. Update CORS_ORIGINS to include your custom domain

## 🚨 **Troubleshooting**

### **CORS Errors**
```bash
# Make sure CORS_ORIGINS in Railway matches your Vercel URL exactly
CORS_ORIGINS=https://your-project.vercel.app
```

### **API Connection Issues**
```bash
# Verify REACT_APP_API_URL in Vercel points to your Railway backend
REACT_APP_API_URL=https://your-project.railway.app
```

### **Build Failures**
- Check build logs in Vercel/Railway dashboards
- Verify all dependencies are in package.json/requirements.txt
- Ensure environment variables are set correctly

### **File Upload Issues**
- Railway has ephemeral storage - uploaded files are temporary
- For persistent storage, consider adding a database or cloud storage

## 📊 **Monitoring Your App**

### **Vercel Analytics**
- Built-in analytics for frontend performance
- Real-time visitor data
- Core Web Vitals monitoring

### **Railway Metrics**
- Resource usage monitoring
- Request/response metrics
- Error tracking

### **Optional: Add Uptime Monitoring**
- Use [UptimeRobot](https://uptimerobot.com) (free)
- Monitor both frontend and backend URLs
- Get alerts if your app goes down

## 💡 **Optimization Tips**

1. **Enable Vercel Analytics** for performance insights
2. **Monitor Railway usage** to stay within free tier limits
3. **Use environment variables** for all configuration
4. **Keep your OpenAI API key secure** - never commit it to git
5. **Test thoroughly** before sharing with users

## 🎉 **You're Live!**

Congratulations! Your REVI.AI chatbot is now live on the internet:

- **Frontend:** `https://your-project.vercel.app`
- **Backend API:** `https://your-project.railway.app`

Share your chatbot with the world! 🌍

## 📞 **Need Help?**

- **Vercel Docs:** [vercel.com/docs](https://vercel.com/docs)
- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **GitHub Issues:** Report problems in your repository

---

**Total deployment time:** ~15-30 minutes  
**Monthly cost:** $0 (free tier)  
**Scalability:** Automatic scaling included 