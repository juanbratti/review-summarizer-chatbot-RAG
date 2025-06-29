# 🤖 REVI.AI - RAG Chatbot for Review Analysis

A modern ChatGPT-style chatbot that analyzes product reviews using RAG (Retrieval-Augmented Generation) technology. Built with React frontend and FastAPI backend.

![REVI.AI Screenshot](https://via.placeholder.com/800x400/2a2f3a/f9fafb?text=REVI.AI+ChatGPT-Style+Interface)

## ✨ Features

- 🎨 **Modern ChatGPT-style interface** with message bubbles and typing indicators
- 🌙 **Dark/Light mode toggle** with system preference detection
- 📱 **Responsive design** for desktop, tablet, and mobile
- 🔍 **RAG-powered responses** using ChromaDB and OpenAI
- 📄 **File upload support** for review data
- 💬 **Real-time conversation** with source citations
- 🚀 **Production-ready** with Vercel + Railway deployment

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/review-summarizer-chatbot-RAG.git
   cd review-summarizer-chatbot-RAG
   ```

2. **Setup backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp env.production.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Setup frontend:**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Run the application:**
   ```bash
   # From project root
   chmod +x deploy.sh
   ./deploy.sh  # Follow the interactive setup
   
   # Or manually:
   # Terminal 1 (Backend):
   cd backend && source venv/bin/activate && uvicorn app.main:app --reload
   
   # Terminal 2 (Frontend):
   cd frontend && npm start
   ```

5. **Access the app:** Open http://localhost:3000

## 🌐 Deployment to Internet - Vercel + Railway

**Cost:** Free tier available  
**Difficulty:** ⭐⭐⭐ (Beginner-friendly)  
**Time:** ~15-30 minutes

### 🚀 **Quick Deployment Steps:**

1. **Push code to GitHub**
2. **Deploy frontend to [Vercel](https://vercel.com):**
   - Connect GitHub repository
   - Set root directory to `frontend`
   - Add environment variable: `REACT_APP_API_URL=https://your-backend.railway.app`

3. **Deploy backend to [Railway](https://railway.app):**
   - Connect GitHub repository
   - Set root directory to `backend`
   - Add environment variables (OpenAI API key, CORS origins)

4. **Connect them together and test!**

### 🎯 **Use the Deployment Helper:**

```bash
chmod +x deploy.sh
./deploy.sh
```

This interactive script will:
- ✅ Check all prerequisites
- 🏗️ Build your frontend for production
- 🐍 Setup your backend environment
- 📋 Guide you through the deployment process
- 🌐 Open deployment platforms in your browser

## 📚 Documentation

- **[📖 Deployment Guide](DEPLOYMENT_GUIDE.md)** - Step-by-step deployment instructions
- **[🎨 ChatGPT Interface](frontend/README_CHATGPT_STYLE.md)** - Frontend architecture details
- **[🌙 Dark Mode Implementation](frontend/README_DARK_LIGHT_MODE.md)** - Theme system documentation

## 🛠️ Technology Stack

### Frontend
- **React** - Modern UI library
- **CSS Custom Properties** - Theme system
- **Axios** - HTTP client
- **Context API** - State management

### Backend
- **FastAPI** - Modern Python web framework
- **ChromaDB** - Vector database for RAG
- **OpenAI GPT** - Language model
- **Uvicorn** - ASGI server

## 🔧 Configuration

### Environment Variables

**Backend (`backend/.env`):**
```bash
OPENAI_API_KEY=your_openai_api_key
CORS_ORIGINS=https://your-frontend-domain.com
DEBUG=False
```

**Frontend (`frontend/.env.local`):**
```bash
REACT_APP_API_URL=https://your-backend-url.com
```

## 📁 Project Structure

```
review-summarizer-chatbot-RAG/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── ChatInterface.js  # Main chat component
│   │   ├── ThemeContext.js   # Theme management
│   │   └── ...
│   └── package.json
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Main FastAPI app
│   │   ├── routers/         # API routes
│   │   └── ...
│   └── requirements.txt
├── vercel.json              # Vercel deployment config
├── railway.json             # Railway deployment config
├── deploy.sh                # Deployment helper script
└── DEPLOYMENT_GUIDE.md      # Detailed deployment guide
```

## 🚀 Deployment Helper

Use the interactive deployment script:

```bash
chmod +x deploy.sh
./deploy.sh
```

This script will:
- ✅ Check prerequisites
- 🏗️ Build the frontend for production
- 🐍 Setup the backend environment
- 📋 Guide you through deployment options
- 🌐 Open deployment platforms in browser

## 🔒 Security

- Environment variables for sensitive data
- CORS protection
- File upload size limits
- Input validation and sanitization
- HTTPS in production (handled by deployment platforms)

## 📊 Monitoring

- Health check endpoints (`/health`)
- Error handling and logging
- Platform-specific monitoring dashboards
- Optional: Sentry for error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

- 📖 Check the [Deployment Guide](DEPLOYMENT_GUIDE.md) for detailed instructions
- 🐛 Report issues on GitHub
- 💡 Feature requests welcome

---

**Ready to deploy?** Follow the [Deployment Guide](DEPLOYMENT_GUIDE.md) or run `./deploy.sh` to get started! 🚀
