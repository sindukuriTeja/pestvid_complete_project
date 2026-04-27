# 📚 PestVid Project - Documentation Index

## 🎯 Where to Start?

### New to the Project?
👉 **[START_HERE.md](START_HERE.md)** - Your main getting started guide

### Need Quick Help?
👉 **[QUICK_START.md](QUICK_START.md)** - Quick reference for common tasks

### Want Visual Overview?
👉 **[README_SETUP.md](README_SETUP.md)** - Visual guide with tables and examples

---

## 📖 All Documentation Files

### Setup & Installation
| File | Description | When to Use |
|------|-------------|-------------|
| **START_HERE.md** | Main getting started guide | First time setup |
| **QUICK_START.md** | Quick reference guide | Need quick help |
| **SETUP_GUIDE.md** | Detailed setup instructions | Full installation guide |
| **SETUP_COMPLETE.md** | Setup status summary | Check what's done |
| **README_SETUP.md** | Visual overview | Quick visual reference |
| **INDEX.md** | This file | Find documentation |

### AI Features
| File | Description | When to Use |
|------|-------------|-------------|
| **AI_AGENT_README.md** | AI agent documentation | Learn about AI features |
| **COMPLETE_AI_PLAN.md** | Full architecture overview | Understand system design |

### Scripts & Tools
| File | Type | Description |
|------|------|-------------|
| **flask_server_simple.py** | Python | Simplified Flask server (use this!) |
| **flask_server.py** | Python | Full Flask server with AI models |
| **simple_ai_agent.py** | Python | AI agent logic |
| **test_setup.py** | Python | Test your installation |
| **test_simple_ai_agent.py** | Python | Test AI agent |
| **test_flask_endpoint.py** | Python | Test Flask endpoints |
| **start_flask.bat** | Batch | Start Flask server (Windows) |
| **test_api.bat** | Batch | Test API endpoints (Windows) |
| **start_backend.bat** | Batch | Start backend server (Windows) |

### Configuration
| File | Description |
|------|-------------|
| **requirements.txt** | Python dependencies |
| **.env** | Environment variables (API keys) |
| **backend/.env** | Backend configuration |
| **backend/package.json** | Node.js dependencies |

---

## 🚀 Quick Actions

### I want to...

#### Start the Server
```bash
python flask_server_simple.py
```
Or double-click: `start_flask.bat`

#### Test the Installation
```bash
python test_setup.py
```

#### Test the API
```bash
curl http://localhost:5000/quick-tips
```
Or double-click: `test_api.bat`

#### Start Backend (needs MongoDB)
```bash
cd backend
npm start
```
Or double-click: `start_backend.bat`

#### Get Farming Advice
```bash
curl -X POST http://localhost:5000/simple-ai-advice \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"How to grow tomatoes?\"}"
```

---

## 📁 Project Structure

```
PestVid-main/
│
├── 📚 DOCUMENTATION
│   ├── START_HERE.md              ⭐ Start here!
│   ├── QUICK_START.md             Quick reference
│   ├── SETUP_GUIDE.md             Detailed guide
│   ├── SETUP_COMPLETE.md          Setup status
│   ├── README_SETUP.md            Visual overview
│   ├── INDEX.md                   This file
│   ├── AI_AGENT_README.md         AI features
│   └── COMPLETE_AI_PLAN.md        Architecture
│
├── 🐍 PYTHON SCRIPTS
│   ├── flask_server_simple.py     ⭐ Use this!
│   ├── flask_server.py            Full version
│   ├── simple_ai_agent.py         AI logic
│   ├── test_setup.py              Test install
│   ├── test_simple_ai_agent.py    Test AI
│   └── test_flask_endpoint.py     Test API
│
├── 🪟 BATCH FILES (Windows)
│   ├── start_flask.bat            ⭐ Start server
│   ├── test_api.bat               Test API
│   └── start_backend.bat          Start backend
│
├── ⚙️ CONFIGURATION
│   ├── requirements.txt           Python deps
│   ├── .env                       API keys
│   └── .gitignore                 Git ignore
│
├── 📁 backend/                    Node.js backend
│   ├── server.js                  Main server
│   ├── models/                    DB models
│   ├── routes/                    API routes
│   ├── package.json               Dependencies
│   └── .env                       Config
│
└── 📁 public/                     Frontend
    ├── index.html                 Main page
    ├── js/                        JavaScript
    └── css/                       Styles
```

---

## 🎯 Common Scenarios

### Scenario 1: First Time Setup
1. Read **START_HERE.md**
2. Run `python test_setup.py`
3. Run `python flask_server_simple.py`
4. Test with `curl http://localhost:5000/quick-tips`

### Scenario 2: Quick Reference
1. Open **QUICK_START.md**
2. Find the command you need
3. Copy and run it

### Scenario 3: Full Installation
1. Read **SETUP_GUIDE.md**
2. Install MongoDB
3. Setup all dependencies
4. Run full stack

### Scenario 4: Understanding AI Features
1. Read **AI_AGENT_README.md**
2. Check **COMPLETE_AI_PLAN.md**
3. Test with `python test_simple_ai_agent.py`

### Scenario 5: Troubleshooting
1. Run `python test_setup.py`
2. Check error messages
3. Refer to troubleshooting section in **START_HERE.md**
4. Check configuration files

---

## 🌟 Key Features

### ✅ Working Now
- AI Agricultural Advice
- Crop Problem Analysis
- Seasonal Guidance
- Quick Farming Tips
- Pest Treatment Info

### 🔄 Requires MongoDB
- User Authentication
- Video Management
- Marketplace
- Messaging
- Transactions

### 🔄 Requires Advanced Setup
- Disease Image Detection
- RAG Expert Chat
- Advanced Analytics

---

## 🆘 Getting Help

### Check These First
1. **START_HERE.md** - Main guide
2. **QUICK_START.md** - Quick help
3. Run `python test_setup.py` - Diagnose issues
4. Check terminal error messages

### Common Issues
- Module not found → `pip install <module>`
- Port in use → Change port in config
- MongoDB error → Install MongoDB
- API key error → Check `.env` file

---

## 📊 Setup Status

| Component | Status |
|-----------|--------|
| Python | ✅ 3.14.3 |
| Node.js | ✅ v24.14.1 |
| npm | ✅ 11.11.0 |
| Flask | ✅ Installed |
| Backend Deps | ✅ Installed |
| AI Agent | ✅ Working |
| API Keys | ✅ Configured |
| Model Files | ✅ Present |
| MongoDB | ⚠️ Optional |

---

## 🎉 Ready to Start!

Your PestVid project is fully set up. Choose your path:

### Path 1: Quick Test (2 minutes)
```bash
python flask_server_simple.py
```

### Path 2: Full Setup (30 minutes)
1. Install MongoDB
2. Start backend
3. Setup frontend
4. Install advanced AI packages

### Path 3: Learn More
Read the documentation files to understand the system better.

---

**Happy Farming! 🌱**

*Navigate this index to find exactly what you need!*
