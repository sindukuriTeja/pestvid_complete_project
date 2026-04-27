# 🤖 Simple AI Agent for PestVid

## Overview
A lightweight, intelligent agricultural assistant integrated into your PestVid platform. This AI agent provides crop advice, pest identification, disease diagnosis, and farming recommendations to help farmers make better decisions.

## 🌟 Features

### 1. **Crop Advice & Consultation**
- Get expert agricultural advice using AI (Groq/LLaMA) or local knowledge base
- Covers pest management, disease control, soil health, and irrigation
- Provides practical, actionable recommendations

### 2. **Plant Disease Analysis**
- Analyze crop issues based on text descriptions
- Identify common symptoms and provide treatment recommendations
- Works alongside your existing VLM model for comprehensive analysis

### 3. **Seasonal Farming Guidance**
- Get season-specific farming advice (Spring, Summer, Fall, Winter)
- Crop-specific seasonal recommendations
- Key tasks and activities for each season

### 4. **Quick Tips & Best Practices**
- Daily farming tips and reminders
- Sustainable farming practices
- Integrated pest management (IPM) approaches

## 🚀 How It Works

### Current Integration
```
User Query → Simple AI Agent → {
    ├── Groq API (if available) → LLaMA-70B Response
    └── Local Knowledge Base → Predefined Expert Advice
}
```

### API Endpoints Added to Flask Server

1. **`/simple-ai-advice`** - Get general agricultural advice
2. **`/analyze-description`** - Analyze crop problems from text description
3. **`/seasonal-advice`** - Get seasonal farming guidance
4. **`/quick-tips`** - Get daily farming tips

## 📋 Complete Implementation Plan

### Phase 1: ✅ COMPLETED
- [x] Created simple AI agent (`simple_ai_agent.py`)
- [x] Integrated with Flask server
- [x] Added API endpoints
- [x] Local knowledge base for offline functionality

### Phase 2: Frontend Integration (NEXT STEPS)
- [ ] Add AI Agent section to navigation
- [ ] Create user interface for AI consultation
- [ ] Add quick tips widget to dashboard
- [ ] Integrate with existing plant analysis

### Phase 3: Enhanced Features (FUTURE)
- [ ] Voice interaction capabilities
- [ ] Multi-language support
- [ ] Weather-based recommendations
- [ ] Crop calendar integration

## 🛠️ Installation & Setup

### Prerequisites
```bash
pip install requests python-dotenv
```

### Environment Variables
Add to your `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Usage Examples

#### 1. Get Crop Advice
```python
from simple_ai_agent import pestivid_agent

result = pestivid_agent.get_crop_advice("How to control aphids on tomatoes?")
print(result['advice'])
```

#### 2. Analyze Plant Issues
```python
result = pestivid_agent.analyze_crop_image_description("My tomato leaves have brown spots")
print(result['diagnosis'])
print(result['recommendations'])
```

#### 3. Get Seasonal Advice
```python
result = pestivid_agent.get_seasonal_advice("spring", "tomato")
print(result['advice'])
print(result['key_tasks'])
```

## 🌐 API Usage

### Test the AI Agent
```bash
# Start Flask server
python flask_server.py

# Test AI advice endpoint
curl -X POST http://localhost:5000/simple-ai-advice \
  -H "Content-Type: application/json" \
  -d '{"query": "How to prevent tomato blight?"}'

# Test description analysis
curl -X POST http://localhost:5000/analyze-description \
  -H "Content-Type: application/json" \
  -d '{"description": "Yellow leaves with brown spots"}'

# Get quick tips
curl http://localhost:5000/quick-tips
```

## 🎯 Benefits for PestVid Platform

### For Farmers
- **Instant Expert Advice**: Get immediate answers to farming questions
- **Cost-Effective**: Reduces need for expensive agricultural consultants
- **24/7 Availability**: Access help anytime, anywhere
- **Integrated Experience**: Works seamlessly with existing PestVid features

### For Platform
- **Enhanced User Engagement**: Keeps farmers active on the platform
- **Value Addition**: Provides more reasons to use PestVid
- **Data Collection**: Learns from user queries to improve recommendations
- **Competitive Advantage**: Differentiates from other agricultural platforms

## 🔧 Technical Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask Server   │    │   AI Agent      │
│   (Vue.js)      │◄──►│   (Python)       │◄──►│   (Python)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Existing       │    │   Groq API      │
                       │   VLM Models     │    │   (LLaMA-70B)   │
                       └──────────────────┘    └─────────────────┘
```

## 📊 Knowledge Base Coverage

### Crops Supported
- Tomatoes, Potatoes, Corn, Wheat
- Common diseases and pests for each crop
- Treatment recommendations

### Topics Covered
- **Pest Management**: Aphids, caterpillars, spider mites, whiteflies, thrips
- **Disease Control**: Fungal, bacterial, and viral diseases
- **Soil Health**: pH testing, fertilization, organic amendments
- **Water Management**: Irrigation timing, drought stress, overwatering
- **Seasonal Care**: Planting, harvesting, winter preparation

## 🚀 Quick Start Guide

1. **Test Current Setup**:
   ```bash
   cd PestVid-main
   python flask_server.py
   ```

2. **Test AI Agent**:
   ```bash
   python -c "from simple_ai_agent import pestivid_agent; print(pestivid_agent.get_crop_advice('How to grow tomatoes?'))"
   ```

3. **Add to Frontend** (Next Step):
   - Add AI Agent navigation item
   - Create consultation interface
   - Integrate with existing plant analysis

## 🎉 Ready to Use!

Your simple AI agent is now integrated and ready to help farmers! The agent provides:
- ✅ Intelligent crop advice
- ✅ Disease diagnosis from descriptions  
- ✅ Seasonal farming guidance
- ✅ Quick daily tips
- ✅ Offline functionality with local knowledge base
- ✅ Online AI enhancement with Groq API

**Next Step**: Add the frontend interface to make it accessible to your users through the web application.
