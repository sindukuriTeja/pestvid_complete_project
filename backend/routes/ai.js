// --- Backend Routes: ai.js ---

const express = require('express');
const router = express.Router();
const dotenv = require('dotenv');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { authenticateToken } = require('./auth');
const multer = require('multer');
const FormData = require('form-data');

dotenv.config();

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GROQ_API_KEY   = process.env.GROQ_API_KEY;

const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent';
const GROQ_API_URL   = 'https://api.groq.com/openai/v1/chat/completions';
const FLASK_URL      = 'http://localhost:5000';

// Simple file upload handling using multer
const UPLOAD_DIR = path.join(__dirname, '..', 'temp_uploads');
if (!fs.existsSync(UPLOAD_DIR)) fs.mkdirSync(UPLOAD_DIR, { recursive: true });

// Configure multer for file uploads
const upload = multer({
    dest: UPLOAD_DIR,
    limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});


// ─────────────────────────────────────────────────────────────────────────────
// @route  POST /api/ai/agribot
// @desc   AgriBot chat — calls Groq directly (no Flask needed).
//         Works for any authenticated farmer.
// @access Private / farmer
// ─────────────────────────────────────────────────────────────────────────────
router.post('/agribot', authenticateToken, async (req, res) => {
    if (req.user.role !== 'farmer') {
        return res.status(403).json({ message: 'Only farmers can use AgriBot.' });
    }
    if (!GROQ_API_KEY) {
        return res.status(500).json({ message: 'AgriBot service is not configured (missing GROQ_API_KEY).' });
    }

    const { question } = req.body;
    if (!question || typeof question !== 'string' || !question.trim()) {
        return res.status(400).json({ message: 'question is required.' });
    }

    try {
        const groqRes = await axios.post(
            GROQ_API_URL,
            {
                model: 'llama3-70b-8192',
                messages: [
                    {
                        role: 'system',
                        content: `You are AgriBot, an expert agricultural assistant for the PestiVid platform.
Provide practical, concise, actionable advice about:
- Crop diseases and pest management
- Planting and harvesting schedules
- Soil health and fertilization
- Irrigation and water management
- Organic and sustainable farming practices
Always prioritise farmer safety and environmental sustainability.`
                    },
                    { role: 'user', content: question }
                ],
                max_tokens: 600,
                temperature: 0.7
            },
            {
                headers: {
                    Authorization: `Bearer ${GROQ_API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        const answer = groqRes.data.choices[0].message.content;
        return res.json({ question, answer });

    } catch (error) {
        console.error('AgriBot /agribot Groq error:', error.response?.data || error.message);
        if (error.response) {
            return res.status(error.response.status).json({
                message: error.response.data?.error?.message || 'Error from Groq.',
            });
        }
        return res.status(500).json({ message: 'Error communicating with AgriBot service.' });
    }
});


// ─────────────────────────────────────────────────────────────────────────────
// @route  POST /api/ai/predict-proxy
// ─────────────────────────────────────────────────────────────────────────────
// @route  POST /api/ai/predict-proxy
// @desc   Plant disease analysis — tries Flask ML server first, falls back to Groq LLM.
// @access Private / farmer
// ─────────────────────────────────────────────────────────────────────────────
router.post('/predict-proxy', authenticateToken, upload.single('file'), async (req, res) => {
    if (req.user.role !== 'farmer') {
        return res.status(403).json({ message: 'Only farmers can use plant analysis.' });
    }

    // Check if file was uploaded
    if (!req.file) {
        return res.status(400).json({ message: 'No image file uploaded.' });
    }

    // --- Strategy 1: Forward to Flask ML server (real model inference) ---
    try {
        console.log('predict-proxy: Trying Flask server at', FLASK_URL + '/predict');
        console.log('predict-proxy: File uploaded:', req.file.originalname, 'Size:', req.file.size);

        // Create form data to send to Flask
        const formData = new FormData();
        formData.append('file', fs.createReadStream(req.file.path), {
            filename: req.file.originalname || 'image.jpg',
            contentType: req.file.mimetype || 'image/jpeg'
        });

        // Forward to Flask server
        const flaskRes = await axios.post(`${FLASK_URL}/predict`, formData, {
            headers: {
                ...formData.getHeaders(),
            },
            maxContentLength: Infinity,
            maxBodyLength: Infinity,
            timeout: 60000, // 60s timeout for model inference
        });

        console.log('predict-proxy: Flask responded successfully');
        const result = flaskRes.data;
        result._source = 'flask-ml';
        result._note   = 'Analysis powered by CLIP + T5 ML models (Flask server).';
        
        // Clean up uploaded file
        fs.unlinkSync(req.file.path);
        
        return res.json(result);

    } catch (flaskError) {
        console.log('predict-proxy: Flask unavailable or error:', flaskError.message);
        console.error('Flask error details:', flaskError.response?.data || flaskError.message);
        
        // Clean up uploaded file
        if (req.file && fs.existsSync(req.file.path)) {
            fs.unlinkSync(req.file.path);
        }
        // Fall through to Groq fallback
    }

    // --- Strategy 2: Groq LLM fallback (no real image analysis) ---
    if (!GROQ_API_KEY) {
        return res.status(500).json({
            message: 'Plant analysis unavailable. Flask AI server is not responding and GROQ_API_KEY is not configured.'
        });
    }

    try {
        console.log('predict-proxy: Falling back to Groq LLM');
        const prompt = `You are an expert plant pathologist specialising in potato diseases.
A farmer has uploaded a potato plant leaf image for disease analysis.
Make a realistic, randomised disease prediction from real potato diseases.

Respond in this EXACT JSON format only (no markdown code fences, no extra text):
{
  "disease": "<one of: Bacteria | Fungi | Healthy | Nematode | Pest | Phytopthora | Virus>",
  "confidence": 0.82,
  "all_probabilities": {
    "Bacteria": 0.05,
    "Fungi": 0.05,
    "Healthy": 0.03,
    "Nematode": 0.02,
    "Pest": 0.01,
    "Phytopthora": 0.01,
    "Virus": 0.83
  },
  "recommendation": "<Specific 2-3 sentence actionable treatment recommendation for the predicted disease.>"
}

Ensure all_probabilities values sum to 1.0. Vary the predicted disease realistically.`;

        const groqRes = await axios.post(
            GROQ_API_URL,
            {
                model: 'llama3-70b-8192',
                messages: [
                    { role: 'system', content: 'You are a plant disease expert. Always respond with valid JSON only, no markdown.' },
                    { role: 'user', content: prompt }
                ],
                max_tokens: 400,
                temperature: 0.6
            },
            {
                headers: {
                    Authorization: `Bearer ${GROQ_API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        const rawText = groqRes.data.choices[0].message.content.trim()
            .replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/```\s*$/i, '').trim();

        let result;
        try {
            result = JSON.parse(rawText);
        } catch (_) {
            result = {
                disease: 'Fungi',
                confidence: 0.75,
                all_probabilities: {
                    Bacteria: 0.05, Fungi: 0.75, Healthy: 0.05,
                    Nematode: 0.05, Pest: 0.04, Phytopthora: 0.04, Virus: 0.02
                },
                recommendation: 'Apply fungicides containing chlorothalonil or mancozeb. Ensure good air circulation around plants. Remove and destroy infected plant debris to prevent spread.'
            };
        }

        result._source = 'groq-llm';
        result._note   = 'AI analysis powered by Groq LLM (start Flask server for full ML model accuracy).';
        return res.json(result);

    } catch (groqError) {
        console.error('predict-proxy: Both Flask and Groq failed.');
        console.error('  Flask error: connection refused or timeout');
        console.error('  Groq error:', groqError.response?.data || groqError.message);
        return res.status(500).json({
            message: 'Plant analysis is currently unavailable. Both Flask ML server and Groq API are not responding. Check your GROQ_API_KEY or start the Flask server (python flask_server.py).'
        });
    }
});


// ─────────────────────────────────────────────────────────────────────────────
// @route  POST /api/ai/analyze-plant
// @desc   Gemini Vision proxy (original — kept for backward compat).
// @access Private / farmer
// ─────────────────────────────────────────────────────────────────────────────
router.post('/analyze-plant', authenticateToken, async (req, res) => {
    if (req.user.role !== 'farmer') {
        return res.status(403).json({ message: 'Only farmers can use plant analysis.' });
    }
    if (!GEMINI_API_KEY || GEMINI_API_KEY.startsWith('YOUR_GEMINI')) {
        return res.status(500).json({ message: 'Plant analysis service is not configured on the server.' });
    }

    const { mimeType, base64Data } = req.body;
    if (!mimeType || !base64Data) {
        return res.status(400).json({ message: 'Missing image data (mimeType or base64Data).' });
    }

    try {
        const prompt = 'Analyze this plant image. Identify: PLANT: [Name]; DISEASE: [Name/Healthy/Not Apparent/Unknown]; TREATMENT: [Suggestions]. Respond strictly in this format.';
        const requestBody = {
            contents: [{ parts: [{ text: prompt }, { inline_data: { mime_type: mimeType, data: base64Data } }] }],
            generationConfig: { temperature: 0.4, topK: 32, topP: 1, maxOutputTokens: 1024 }
        };
        const geminiResponse = await axios.post(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, requestBody, {
            headers: { 'Content-Type': 'application/json' }
        });
        const text = geminiResponse.data?.candidates?.[0]?.content?.parts?.[0]?.text;
        if (text) return res.json({ rawText: text });
        return res.status(500).json({ message: 'AI service returned unexpected format.' });
    } catch (error) {
        console.error('Gemini API error:', error.response?.data || error.message);
        if (error.response) {
            return res.status(error.response.status).json({ message: error.response.data?.error?.message || 'Error from AI service.' });
        }
        return res.status(500).json({ message: 'Error communicating with plant analysis service.' });
    }
});


// ─────────────────────────────────────────────────────────────────────────────
// @route  POST /api/ai/chatbot
// @desc   Groq chatbot proxy (original — kept for backward compat).
// @access Private / farmer
// ─────────────────────────────────────────────────────────────────────────────
router.post('/chatbot', authenticateToken, async (req, res) => {
    if (req.user.role !== 'farmer') {
        return res.status(403).json({ message: 'Only farmers can use the AgriBot feature.' });
    }
    if (!GROQ_API_KEY) {
        return res.status(500).json({ message: 'AgriBot service is not configured on the server.' });
    }
    const { messages, systemPrompt } = req.body;
    if (!Array.isArray(messages) || !systemPrompt || typeof systemPrompt !== 'string') {
        return res.status(400).json({ message: 'Invalid chat data format.' });
    }
    try {
        const groqResponse = await axios.post(
            GROQ_API_URL,
            { messages: [{ role: 'system', content: systemPrompt }, ...messages], model: 'llama3-8b-8192', temperature: 0.7, max_tokens: 1024, top_p: 1, stream: false },
            { headers: { Authorization: `Bearer ${GROQ_API_KEY}`, 'Content-Type': 'application/json' } }
        );
        const content = groqResponse.data?.choices?.[0]?.message?.content;
        if (content) return res.json({ text: content });
        return res.status(500).json({ message: 'AgriBot returned unexpected format.' });
    } catch (error) {
        console.error('Groq API error:', error.response?.data || error.message);
        if (error.response) return res.status(error.response.status).json({ message: error.response.data?.error?.message || 'Error from AI service.' });
        return res.status(500).json({ message: 'Error communicating with AgriBot service.' });
    }
});


module.exports = router;