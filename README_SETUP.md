# 🌱 PestVid Agricultural Platform - Setup Complete!

## 🎯 Quick Start (30 seconds)

```bash
# Start the server
python flask_server_simple.py

# In another terminal, test it
curl http://localhost:5000/quick-tips
```

**That's it! Your AI agricultural assistant is running!** 🎉

---

## 📦 What's Installed

| Component | Status | Version |
|-----------|--------|---------|
| Python | ✅ Installed | 3.14.3 |
| Node.js | ✅ Installed | v24.14.1 |
| npm | ✅ Installed | 11.11.0 |
| Flask | ✅ Installed | Latest |
| Backend Deps | ✅ Installed | All packages |
| AI Agent | ✅ Working | Ready |
| API Keys | ✅ Configured | Groq, Cohere, Pinecone |
| Model Files | ✅ Present | CLIP, T5 |

---

## 🚀 Three Ways to Start

### 1️⃣ Double-Click (Easiest)
```
📁 PestVid-main/
   └── start_flask.bat  ← Double-click this!
```

### 2️⃣ Command Line
```bash
python flask_server_simple.py
```

### 3️⃣ Full Stack (Requires MongoDB)
```bash
# Terminal 1: Backend
cd backend
npm start

# Terminal 2: Flask
python flask_server_simple.py
```

---

## 🎮 Test Your Setup

### Quick Test
```bash
python test_setup.py
```

### API Test
```bash
# Start server first, then:
test_api.bat
```

### Manual Test
```bash
# Get farming tips
curl http://localhost:5000/quick-tips

# Get AI advice
curl -X POST http://localhost:5000/simple-ai-advice \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"How to prevent pests?\"}"
```

---

## 🌟 Available Features

### ✅ Working Now (No Extra Setup)
- 🤖 AI Agricultural Advice (powered by Groq/LLaMA)
- 🌾 Crop Problem Analysis
- 📅 Seasonal Farming Guidance
- 💡 Quick Farming Tips
- 🔍 Pest Treatment Recommendations

### 🔄 Requires MongoDB
- 👤 User Authentication
- 📹 Video Upload & Management
- 🛒 Marketplace Features
- 💬 Messaging System
- 💰 Transaction History

### 🔄 Requires Advanced Setup
- 🖼️ Plant Disease Image Detection
- 🧠 RAG-based Expert Chat
- 📊 Advanced Analytics

---

## 📖 Documentation Guide

| File | Purpose | When to Read |
|------|---------|--------------|
| **START_HERE.md** | Main guide | Start here! |
| **QUICK_START.md** | Quick reference | Need quick help |
| **SETUP_GUIDE.md** | Detailed setup | Full installation |
| **SETUP_COMPLETE.md** | Status summary | Check what's done |
| **AI_AGENT_README.md** | AI features | Learn about AI |

---

## 🎯 Common Tasks

### Start Flask Server
```bash
python flask_server_simple.py
```
Server runs on: http://localhost:5000

### Start Backend (needs MongoDB)
```bash
cd backend
npm start
```
Server runs on: http://localhost:3001

### Install MongoDB
**Option A: Local**
- Download: https://www.mongodb.com/try/download/community
- Install as Windows Service

**Option B: Cloud (Free)**
- Sign up: https://www.mongodb.com/cloud/atlas/register
- Create free cluster
- Update `backend/.env` with connection string

### Install Advanced AI Features
```bash
pip install torch torchvision transformers
pip install langchain langchain-cohere langchain-pinecone
python flask_server.py  # Use full server
```

---

## 🌐 API Endpoints

### Flask Server (Port 5000)
```
GET  /                      Health check
POST /simple-ai-advice      Get farming advice
POST /analyze-description   Analyze crop issues
POST /seasonal-advice       Get seasonal tips
GET  /quick-tips           Get quick tips
```

### Backend Server (Port 3001)
```
POST /api/auth/register    Register user
POST /api/auth/login       Login user
GET  /api/videos          List videos
POST /api/videos          Upload video
GET  /api/listings        View marketplace
```

---

## 💡 Example API Calls

### Get Farming Advice
```bash
curl -X POST http://localhost:5000/simple-ai-advice \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"How to grow tomatoes?\"}"
```

### Analyze Crop Problem
```bash
curl -X POST http://localhost:5000/analyze-description \
  -H "Content-Type: application/json" \
  -d "{\"description\": \"Yellow leaves with spots\"}"
```

### Get Seasonal Advice
```bash
curl -X POST http://localhost:5000/seasonal-advice \
  -H "Content-Type: application/json" \
  -d "{\"season\": \"spring\", \"crop\": \"tomato\"}"
```

### Get Quick Tips
```bash
curl http://localhost:5000/quick-tips
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install <module>` |
| Port in use | Change port in config |
| MongoDB error | Install MongoDB or use Atlas |
| API key error | Check `.env` file |

---

## 📁 Project Structure

```
PestVid-main/
├── 📄 START_HERE.md              ← Read this first!
├── 📄 QUICK_START.md             ← Quick reference
├── 📄 SETUP_GUIDE.md             ← Detailed guide
├── 📄 SETUP_COMPLETE.md          ← Setup status
│
├── 🐍 flask_server_simple.py    ← Start this!
├── 🐍 flask_server.py            ← Full version
├── 🐍 simple_ai_agent.py         ← AI logic
├── 🐍 test_setup.py              ← Test installation
│
├── 🪟 start_flask.bat            ← Double-click to start
├── 🪟 test_api.bat               ← Test endpoints
├── 🪟 start_backend.bat          ← Start backend
│
├── 📦 requirements.txt           ← Python packages
├── 🔐 .env                       ← API keys
│
├── 📁 backend/                   ← Node.js backend
│   ├── server.js
│   ├── models/
│   └── routes/
│
└── 📁 public/                    ← Frontend
    ├── index.html
    └── js/
```

---

## 🎊 You're All Set!

### To Start Using PestVid:

1. **Open terminal** in `PestVid-main` folder
2. **Run**: `python flask_server_simple.py`
3. **Test**: `curl http://localhost:5000/quick-tips`
4. **Enjoy!** 🎉

### Next Steps:
- ✅ Server is running - test the API
- 📚 Read START_HERE.md for detailed info
- 🔧 Install MongoDB for full features
- 🚀 Deploy to production when ready

---

## 🆘 Need Help?

1. Check **START_HERE.md** for getting started
2. Run `python test_setup.py` to diagnose issues
3. Review error messages in terminal
4. Check API keys in `.env` file
5. Ensure ports 5000 and 3001 are available

---

## 🌟 Features Highlight

### AI Agricultural Assistant
- Expert farming advice powered by LLaMA-70B
- Local knowledge base for offline use
- Pest and disease identification
- Treatment recommendations
- Seasonal farming guidance

### Platform Features (with MongoDB)
- User authentication and profiles
- Video upload and sharing
- Marketplace for agricultural products
- Messaging between farmers
- Transaction tracking

---

**Happy Farming! 🌱🚜**

*Your AI-powered agricultural platform is ready to help farmers grow better crops!*
