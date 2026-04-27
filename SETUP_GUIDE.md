# PestVid Project Setup Guide

## Overview
PestVid is an agricultural platform with AI-powered plant disease detection, RAG-based chat, and blockchain-inspired features.

## Prerequisites

### Required Software
- Node.js (v16 or higher)
- Python (3.8 or higher)
- MongoDB (local or Atlas)
- Git

### Optional
- CUDA-capable GPU (for faster AI inference)
- MongoDB Compass (for database visualization)

## Setup Instructions

### 1. Clone and Navigate
```bash
cd PestVid-main
```

### 2. Backend Setup (Node.js)

#### Install Dependencies
```bash
cd backend
npm install
```

#### Configure Environment
Edit `backend/.env` and update:
```env
MONGODB_URI=mongodb://127.0.0.1:27017/pest
PORT=3001
JWT_SECRET=your_super_secret_key_replace_this_in_production
```

#### Start MongoDB
Make sure MongoDB is running:
```bash
# Windows (if installed as service)
net start MongoDB

# Or run manually
mongod
```

#### Seed Database (Optional)
```bash
npm run seed
```

#### Start Backend Server
```bash
npm start
# Or for development with auto-reload:
npm run dev
```

Backend will run on: http://localhost:3001

### 3. Python/Flask Setup

#### Create Virtual Environment (Recommended)
```bash
# From PestVid-main directory
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment
The `.env` file in root directory should have:
```env
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-east-1
COHERE_API_KEY=your_cohere_key
GROQ_API_KEY=your_groq_key
```

#### Download AI Models
The project expects these model files in the root:
- `best_vlm_model.pth` (CLIP model for disease detection)
- `best_t2t_recommendation_model.pth` (T5 model for recommendations)

If you don't have these files, the Flask server will show warnings but still run with limited functionality.

#### Start Flask Server
```bash
python flask_server.py
```

Flask server will run on: http://localhost:5000

### 4. Frontend Setup

#### Install Dependencies
```bash
cd public
npm install
```

#### Start Frontend Server
```bash
# If there's a dev script in package.json:
npm run dev
# Or serve the static files
```

Frontend will typically run on: http://localhost:8080 or similar

## Testing the Setup

### Test Backend API
```bash
curl http://localhost:3001/api/health
```

### Test Flask Server
```bash
# Test simple AI advice
curl -X POST http://localhost:5000/simple-ai-advice \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"How to prevent tomato blight?\"}"

# Test quick tips
curl http://localhost:5000/quick-tips
```

### Test Plant Disease Prediction
```bash
python test_flask_endpoint.py
```

### Test AI Agent
```bash
python test_simple_ai_agent.py
```

## Common Issues & Solutions

### MongoDB Connection Error
- Ensure MongoDB is running
- Check connection string in `backend/.env`
- Try: `mongodb://localhost:27017/pest` or `mongodb://127.0.0.1:27017/pest`

### Python Package Installation Errors
- Upgrade pip: `pip install --upgrade pip`
- Install packages one by one if batch install fails
- For torch: Visit https://pytorch.org for platform-specific installation

### Port Already in Use
- Backend (3001): Change PORT in `backend/.env`
- Flask (5000): Change port in `flask_server.py` last line
- Frontend: Check package.json scripts

### Missing AI Model Files
- The Flask server will run without model files but with limited functionality
- Disease prediction endpoint will return errors
- RAG chat and simple AI agent will still work

### CUDA/GPU Issues
- The code automatically falls back to CPU if CUDA is unavailable
- For CPU-only: Models will be slower but functional

## Project Structure

```
PestVid-main/
├── backend/              # Node.js/Express API
│   ├── models/          # MongoDB schemas
│   ├── routes/          # API routes
│   ├── server.js        # Main server file
│   └── .env             # Backend config
├── public/              # Frontend files
│   ├── js/             # JavaScript/Vue components
│   ├── css/            # Stylesheets
│   └── index.html      # Main HTML
├── flask_server.py      # Python AI server
├── simple_ai_agent.py   # AI agent logic
├── requirements.txt     # Python dependencies
└── .env                # Python/Flask config
```

## API Endpoints

### Backend (Node.js) - Port 3001
- POST `/api/auth/register` - User registration
- POST `/api/auth/login` - User login
- GET `/api/videos` - List videos
- POST `/api/videos` - Upload video
- GET `/api/listings` - Marketplace listings
- POST `/api/messages` - Send message

### Flask Server - Port 5000
- POST `/predict` - Plant disease prediction (requires image)
- POST `/chat` - RAG-based plant disease chat
- POST `/simple-ai-advice` - Get agricultural advice
- POST `/analyze-description` - Analyze crop issues from text
- POST `/seasonal-advice` - Get seasonal farming advice
- GET `/quick-tips` - Get quick farming tips

## Next Steps

1. Configure all API keys in `.env` files
2. Download or train AI model files
3. Customize frontend branding and styling
4. Set up production database (MongoDB Atlas)
5. Configure cloud storage for videos (Storj/S3)
6. Deploy to production server

## Support

For issues or questions:
- Check the AI_AGENT_README.md for AI agent details
- Review COMPLETE_AI_PLAN.md for architecture overview
- Ensure all dependencies are correctly installed
- Verify environment variables are set

## Development Tips

- Use `nodemon` for backend auto-reload
- Keep virtual environment activated for Python work
- Test API endpoints with Postman or curl
- Monitor MongoDB with MongoDB Compass
- Check browser console for frontend errors
