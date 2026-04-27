# 🌱 PestVid - AI-Powered Agricultural Platform

PestVid is a comprehensive, full-stack agricultural platform designed to empower farmers, buyers, and investors. It combines a robust video marketplace with state-of-the-art Artificial Intelligence (AI) to provide instant plant disease diagnostics, treatment recommendations, and expert farming advice.

## ✨ Key Features

### 🚜 For Farmers
*   **AI Plant Disease Detection:** Upload an image of a crop (e.g., a potato leaf) and instantly receive a diagnosis using our custom-trained Vision-Language Model (CLIP) with 75%+ accuracy.
*   **AI Treatment Recommendations:** Get actionable, text-to-text (T2T) treatment plans for diagnosed plant diseases.
*   **AgriBot AI Assistant:** A specialized chatbot (powered by Groq LLaMA-70B and a localized knowledge base) ready to answer any farming, crop, or pest-related questions.
*   **Video Marketplace:** Upload and monetize agricultural videos, tutorials, and crop updates.
*   **Funding Requests:** Connect with agricultural investors by submitting project funding requests.
*   **Messaging System:** Communicate directly in real-time with buyers and investors.

### 🛒 For Buyers
*   **Marketplace Access:** Browse, purchase, and download premium agricultural video content.
*   **Direct Messaging:** Contact farmers directly to inquire about produce or techniques.

### 💼 For Investors
*   **Discover Opportunities:** Browse active funding requests from vetted farmers.
*   **Track Investments:** Monitor the progress of funded agricultural projects.

---

## 🛠️ Tech Stack

**Frontend**
*   HTML5, CSS3 (Modern, Responsive UI)
*   Vanilla JavaScript & Vue.js (for dynamic components like Chat)

**Backend (Node.js)**
*   **Runtime:** Node.js / Express.js
*   **Database:** MongoDB (Local or Atlas)
*   **Features:** User Authentication (JWT), Marketplace API, Messaging, Funding Routes

**AI Server (Python)**
*   **Framework:** Flask
*   **Models:** PyTorch (CLIP VLM, T5/T2T Models)
*   **LLM & RAG:** LangChain, Groq API (LLaMA-70B), Pinecone (Vector Store), Cohere (Embeddings)

---

## 🚀 Getting Started

### 1. Prerequisites
*   **Node.js** (v14 or higher)
*   **Python** (v3.10 to v3.14 recommended)
*   **MongoDB** (running locally on port 27017 or a cloud MongoDB Atlas URI)

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sindukuriTeja/pestvid_complete_project.git
   cd pestvid_complete_project
   ```

2. **Install Node.js Dependencies (Backend):**
   ```bash
   cd backend
   npm install
   cd ..
   ```

3. **Install Python Dependencies (AI Server):**
   ```bash
   pip install -r requirements.txt
   ```

### 3. Environment Variables (.env)

You need to set up two environment files to handle your API keys and database connections safely.

**File 1: `/.env` (Root Directory for AI)**
Create a `.env` file in the main folder and add your AI service keys:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
COHERE_API_KEY=your_cohere_api_key
GROQ_API_KEY=your_groq_api_key
```

**File 2: `/backend/.env` (Backend Directory)**
Create a `.env` file in the `backend/` folder:
```env
MONGODB_URI=mongodb://127.0.0.1:27017/pestivid_db
PORT=3002
JWT_SECRET=your_super_secret_jwt_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Running the Application

You can start the entire application (both the Node.js backend and the Python AI server) using the provided startup script:

**On Windows:**
```powershell
./start_all_servers.bat
```

Alternatively, run them separately:
*   **Start AI Server:** `python flask_server.py` (Runs on http://localhost:5000)
*   **Start Backend Server:** `cd backend && npm start` (Runs on http://localhost:3002)
*   **Open Frontend:** Open `public/index.html` in your web browser.

---

## 🤖 AI Models Required (Note)
Due to GitHub's file size limits, the large `.pth` model weights for local disease detection are ignored via `.gitignore` and are not included in this repository. 
*   `best_vlm_model.pth`
*   `best_t2t_recommendation_model.pth`

*(If you are deploying this from scratch, you will need to place these model files in the root directory for the local PyTorch inference to function).*

---

## 📝 License
This project is proprietary. All rights reserved.
