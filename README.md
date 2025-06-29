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
- 🚀 **Production-ready** with comprehensive deployment options

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

## 🌐 Deployment to Internet

### 🥇 **Option 1: Vercel + Railway (Recommended)**

**Cost:** Free tier available  
**Difficulty:** Beginner-friendly

1. **Push code to GitHub**
2. **Deploy frontend to [Vercel](https://vercel.com):**
   - Connect GitHub repository
   - Set root directory to `frontend`
   - Add environment variable: `REACT_APP_API_URL=https://your-backend.railway.app`

3. **Deploy backend to [Railway](https://railway.app):**
   - Connect GitHub repository
   - Set root directory to `backend`
   - Add environment variables (OpenAI API key, CORS origins)

### 🥈 **Option 2: Single Server**

**Cost:** $5-20/month  
**Difficulty:** Intermediate

Deploy both frontend and backend on DigitalOcean, AWS, or Linode. Full server setup instructions in `DEPLOYMENT_GUIDE.md`.

### 🥉 **Option 3: Docker**

**Cost:** Varies  
**Difficulty:** Advanced

```bash
# Local testing
docker-compose up --build

# Deploy to any cloud platform supporting Docker
```

## 📚 Documentation

- **[📖 Deployment Guide](DEPLOYMENT_GUIDE.md)** - Comprehensive deployment instructions
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
├── docker-compose.yml        # Docker configuration
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
- 🔧 Test your setup with Docker

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
