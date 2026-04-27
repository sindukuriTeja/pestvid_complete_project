<div align="center">
  <h1>🌱 PestVid - AI-Powered Agricultural Platform</h1>
  <p><i>Empowering Farmers, Buyers, and Investors with cutting-edge AI and seamless marketplaces.</i></p>

  [![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)]()
  [![Node.js](https://img.shields.io/badge/Node.js-14+-green?style=for-the-badge&logo=nodedotjs)]()
  [![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)]()
  [![Vue.js](https://img.shields.io/badge/Vue.js-UI-4FC08D?style=for-the-badge&logo=vuedotjs)]()
  [![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb)]()
</div>

---

## 📖 Project Overview

**PestVid** is a comprehensive, full-stack agricultural ecosystem built to bridge the gap between technology and traditional farming. It leverages powerful AI (like Groq LLaMA-70B and PyTorch CLIP models) to instantly diagnose plant diseases and provide expert chatbot assistance, while simultaneously hosting a fully-fledged video marketplace and funding hub.

Whether you are a **Farmer** looking to protect your crops and secure investment, a **Buyer** sourcing high-quality produce tutorials, or an **Investor** looking to fund the future of agriculture, PestVid has the tools you need.

---

## ✨ Core Features

### 🚜 For Farmers
*   🔬 **AI Plant Disease Detection:** Upload an image of a crop (e.g., a potato leaf) and instantly receive a diagnosis using our custom-trained Vision-Language Model (CLIP) with 75%+ accuracy.
*   📋 **AI Treatment Recommendations:** Get actionable, text-to-text (T2T) treatment plans dynamically generated for diagnosed plant diseases.
*   🤖 **AgriBot AI Assistant:** A specialized chatbot powered by **Groq LLaMA-70B** and a localized **Pinecone RAG (Retrieval-Augmented Generation)** knowledge base, ready to answer complex agricultural questions.
*   📹 **Video Marketplace:** Upload and monetize agricultural videos, tutorials, and crop updates to build an additional revenue stream.
*   💰 **Funding Requests:** Connect with agricultural investors by submitting and tracking project funding requests.
*   💬 **Real-time Messaging:** Communicate directly with buyers and investors.

### 🛒 For Buyers
*   **Marketplace Access:** Browse, purchase, and download premium agricultural video content.
*   **Direct Messaging:** Contact farmers directly to inquire about produce or techniques.
*   **Transaction Tracking:** Maintain a clear history of all digital purchases.

### 💼 For Investors
*   **Discover Opportunities:** Browse active funding requests from vetted farmers.
*   **Track Investments:** Monitor the progress of funded agricultural projects securely.

---

## 🏗️ System Architecture & Tech Stack

PestVid is built on a split-backend architecture to efficiently separate heavy AI workloads from standard web traffic.

### 1. Frontend Interface
*   **Core:** HTML5, CSS3, Vanilla JavaScript
*   **Dynamic Components:** Vue.js (utilized for the real-time chat interface)
*   **Design System:** Custom Dark/Light theme, responsive layouts for mobile and desktop viewing.

### 2. Main Web Backend (Node.js)
*   **Runtime:** Node.js / Express.js
*   **Database:** MongoDB (Local or Atlas via Mongoose)
*   **Features:** User Authentication (JWT), Marketplace APIs, Video Metadata, Messaging, Funding Routes.

### 3. AI Processing Server (Python)
*   **Framework:** Flask API
*   **Vision Models:** PyTorch (CLIP VLM) for image classification.
*   **Text Models:** T5 / Custom T2T for recommendation generation.
*   **LLM & RAG:** LangChain, Groq API (LLaMA-70B), Pinecone (Vector Store), Cohere (Embeddings).

---

## 📂 Project Structure

```text
pestvid_complete_project/
├── backend/                  # Node.js Express Application
│   ├── config/               # Database configurations
│   ├── models/               # MongoDB Mongoose Schemas (User, Video, Message)
│   ├── routes/               # API endpoints (auth, videos, messaging)
│   ├── server.js             # Entry point for the Node.js server
│   └── .env                  # Backend environment variables
├── public/                   # Frontend Web Assets
│   ├── css/                  # Stylesheets
│   ├── js/                   # Vue.js components and Vanilla JS scripts
│   └── index.html            # Main entry point for the frontend
├── flask_server.py           # Python Flask API for AI Services
├── requirements.txt          # Python dependencies
├── start_all_servers.bat     # Windows script to launch both servers simultaneously
└── .env                      # AI Server environment variables
```

---

## 📡 Key API Endpoints Reference

### AI Server (Port 5000)
*   `POST /predict` - Upload image, get disease detection.
*   `POST /chat` - RAG chatbot with intelligent fallback.
*   `POST /simple-ai-advice` - Direct LLM advice endpoint.

### Web Backend (Port 3002)
*   `POST /api/auth/login` & `/api/auth/signup` - User Authentication.
*   `GET /api/videos` - Fetch marketplace videos.
*   `GET /api/funding-requests` - Fetch active funding requests.
*   `POST /api/messaging` - Send messages between users.

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
*   **Node.js** (v14 or higher)
*   **Python** (v3.10 to v3.14)
*   **MongoDB** (running locally on port 27017 or a cloud MongoDB Atlas URI)

### 2. Clone the Repository
```bash
git clone https://github.com/sindukuriTeja/pestvid_complete_project.git
cd pestvid_complete_project
```

### 3. Install Dependencies
**Backend (Node.js):**
```bash
cd backend
npm install
cd ..
```
**AI Server (Python):**
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
You must configure two `.env` files for the platform to function securely.

**File 1: Root Directory (`/.env`)**
Used by the Python AI Server:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
COHERE_API_KEY=your_cohere_api_key
GROQ_API_KEY=your_groq_api_key
```

**File 2: Backend Directory (`/backend/.env`)**
Used by the Node.js Server:
```env
MONGODB_URI=mongodb://127.0.0.1:27017/pestivid_db
PORT=3002
JWT_SECRET=your_super_secret_jwt_key
GROQ_API_KEY=your_groq_api_key
```

### 5. Running the Platform
**On Windows:**
Simply run the included batch script to launch both the Node.js and Python servers simultaneously:
```powershell
./start_all_servers.bat
```

**Manual Startup:**
*   **Start AI Server:** `python flask_server.py` (Runs on port 5000)
*   **Start Backend:** `cd backend && npm start` (Runs on port 3002)
*   **Launch UI:** Open `public/index.html` in your web browser.

---

## ⚠️ Important Note Regarding AI Models
Due to GitHub's strict 100MB file size limit, the large PyTorch model weights required for local offline disease detection are **ignored via `.gitignore`** and are not included in this repository. 
*   `best_vlm_model.pth` (~688 MB)
*   `best_t2t_recommendation_model.pth` (~293 MB)

*If you are deploying this from scratch, you will need to place these trained model files in the root directory for the local PyTorch inference to function properly.*

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
This project is proprietary. All rights reserved.
