# Quick Start Guide for PestVid

## Current Status
✅ Python 3.14.3 installed
✅ Node.js v24.14.1 installed
✅ npm 11.11.0 installed
✅ Backend dependencies installed
✅ Basic Python packages installed
❌ MongoDB not installed (required for backend)
⚠️ AI model files missing (optional - for disease prediction)
⚠️ Advanced Python packages needed (for full AI features)

## Quick Setup Options

### Option 1: Run Without MongoDB (Flask Server Only)
If you just want to test the AI features without the full backend:

```bash
# Start Flask server
python flask_server.py
```

This will give you:
- ✅ Simple AI agricultural advice
- ✅ Crop description analysis
- ✅ Seasonal farming tips
- ✅ Quick farming tips
- ❌ No plant disease image prediction (needs model files)
- ❌ No RAG chat (needs Pinecone/Cohere setup)
- ❌ No user authentication or database features

### Option 2: Install MongoDB for Full Backend

#### Download MongoDB Community Server
1. Visit: https://www.mongodb.com/try/download/community
2. Download Windows version
3. Run installer (choose "Complete" installation)
4. Install as Windows Service (recommended)

#### After Installation
```bash
# Verify MongoDB is running
mongosh

# Or check Windows Services
# Press Win+R, type: services.msc
# Look for "MongoDB" service
```

#### Then Start Backend
```bash
cd backend
npm start
```

Backend will run on: http://localhost:3001

### Option 3: Use MongoDB Atlas (Cloud - No Installation)

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Create free account
3. Create a free cluster
4. Get connection string
5. Update `backend/.env`:
   ```env
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pest
   ```

## Testing the Setup

### Test Flask Server (AI Features)
```bash
# Terminal 1: Start Flask
python flask_server.py

# Terminal 2: Test endpoints
curl http://localhost:5000/quick-tips

curl -X POST http://localhost:5000/simple-ai-advice ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"How to grow tomatoes?\"}"
```

### Test Backend (if MongoDB installed)
```bash
# Terminal 1: Start backend
cd backend
npm start

# Terminal 2: Test API
curl http://localhost:3001/api/health
```

## What Works Right Now

### Without Any Additional Setup
- ✅ Simple AI agent with local knowledge base
- ✅ Crop advice for common issues
- ✅ Pest treatment recommendations
- ✅ Seasonal farming guidance
- ✅ Quick farming tips

### With Groq API Key (Free)
1. Get free API key: https://console.groq.com
2. Add to `.env`: `GROQ_API_KEY=your_key_here`
3. Restart Flask server
4. Now you get AI-powered responses using LLaMA-70B

### With MongoDB
- ✅ User registration and authentication
- ✅ Video uploads and listings
- ✅ Marketplace features
- ✅ Messaging system
- ✅ Transaction history

### With AI Model Files
- ✅ Plant disease detection from images
- ✅ Treatment recommendations

## Recommended Next Steps

1. **Test Flask Server First** (easiest)
   ```bash
   python flask_server.py
   ```

2. **Get Groq API Key** (free, improves AI responses)
   - Visit: https://console.groq.com
   - Sign up and get API key
   - Add to `.env` file

3. **Install MongoDB** (for full features)
   - Choose local installation OR MongoDB Atlas
   - Update connection string in `backend/.env`
   - Start backend server

4. **Optional: Setup AI Models** (advanced)
   - Requires training or downloading model files
   - See COMPLETE_AI_PLAN.md for details

## Common Commands

```bash
# Start Flask server (AI features)
python flask_server.py

# Start backend (requires MongoDB)
cd backend
npm start

# Test AI agent
python test_simple_ai_agent.py

# Seed database (after MongoDB setup)
cd backend
npm run seed
```

## Troubleshooting

### "Module not found" errors
```bash
pip install <missing-module>
```

### Port already in use
- Flask (5000): Change port in `flask_server.py` line 331
- Backend (3001): Change PORT in `backend/.env`

### MongoDB connection error
- Check if MongoDB service is running
- Verify connection string in `backend/.env`
- Try: `mongodb://localhost:27017/pest` or `mongodb://127.0.0.1:27017/pest`

## Need Help?

Check these files:
- `SETUP_GUIDE.md` - Detailed setup instructions
- `AI_AGENT_README.md` - AI agent documentation
- `COMPLETE_AI_PLAN.md` - Full architecture overview

## Quick Test Script

Save this as `test_setup.py`:
```python
print("Testing PestVid Setup...")
print("=" * 50)

# Test imports
try:
    import flask
    print("✅ Flask installed")
except:
    print("❌ Flask not installed - run: pip install flask")

try:
    import requests
    print("✅ Requests installed")
except:
    print("❌ Requests not installed - run: pip install requests")

try:
    from simple_ai_agent import pestivid_agent
    print("✅ AI Agent loaded")
    result = pestivid_agent.get_quick_tips()
    print(f"✅ AI Agent working - {len(result)} tips available")
except Exception as e:
    print(f"❌ AI Agent error: {e}")

print("=" * 50)
print("Setup test complete!")
```

Run with: `python test_setup.py`
