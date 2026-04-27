import sys
import warnings

# Suppress Pydantic V1 deprecation warning on Python 3.14+
if sys.version_info >= (3, 14):
    warnings.filterwarnings("ignore", message=".*Pydantic V1.*", category=UserWarning)

# Ignore minor warnings
warnings.filterwarnings("ignore")

from flask import Flask, request, jsonify
import os
import requests as http_requests
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from typing_extensions import TypedDict
from flask_cors import CORS

# --- Check CORE dependencies (required) ---
_missing_deps = []

try:
    import torch
    from torch import nn
except ImportError:
    _missing_deps.append("torch")

try:
    from transformers import CLIPProcessor, CLIPModel, T5TokenizerFast, T5ForConditionalGeneration
except ImportError:
    _missing_deps.append("transformers")

try:
    from PIL import Image
except ImportError:
    _missing_deps.append("pillow")

try:
    import numpy as np
except ImportError:
    _missing_deps.append("numpy")

if _missing_deps:
    print("\n" + "=" * 60)
    print("❌ MISSING CORE PYTHON DEPENDENCIES")
    print("=" * 60)
    print(f"The following packages are not installed: {', '.join(_missing_deps)}")
    print("\nFix by running:")
    print(f"  pip install {' '.join(_missing_deps)}")
    print("=" * 60 + "\n")
    sys.exit(1)

# --- Check OPTIONAL RAG dependencies (graceful fallback) ---
RAG_AVAILABLE = True
_optional_missing = []

try:
    from langchain_cohere import CohereEmbeddings
except ImportError:
    RAG_AVAILABLE = False
    _optional_missing.append("langchain-cohere")

try:
    from langchain_pinecone import PineconeVectorStore
except ImportError:
    RAG_AVAILABLE = False
    _optional_missing.append("langchain-pinecone")

try:
    from langchain_groq import ChatGroq
except ImportError:
    RAG_AVAILABLE = False
    _optional_missing.append("langchain-groq")

try:
    from langchain_core.documents import Document
except ImportError:
    try:
        from langchain.schema import Document
    except ImportError:
        RAG_AVAILABLE = False
        _optional_missing.append("langchain")

try:
    from pinecone import Pinecone
except ImportError:
    RAG_AVAILABLE = False
    _optional_missing.append("pinecone-client")

try:
    from langgraph.graph import StateGraph, END
except ImportError:
    RAG_AVAILABLE = False
    _optional_missing.append("langgraph")

try:
    from simple_ai_agent import pestivid_agent
except ImportError:
    pestivid_agent = None
    print("⚠️  simple_ai_agent not available — /simple-ai-advice endpoints will be disabled.")

if _optional_missing:
    print("\n" + "=" * 60)
    print("⚠️  OPTIONAL RAG DEPENDENCIES MISSING (Python 3.14 compat)")
    print("=" * 60)
    print(f"Not installed: {', '.join(_optional_missing)}")
    print("RAG chat will use Groq API fallback instead.")
    print("Core disease prediction (CLIP/T5) still works fine!")
    print("=" * 60 + "\n")

load_dotenv()


app = Flask(__name__)
CORS(app)

# --- 1. PLANT DISEASE PREDICTION SETUP ---
print("--- Initializing Plant Disease Prediction Models ---")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

classes = ['Bacteria', 'Fungi', 'Healthy', 'Nematode', 'Pest', 'Phytopthora', 'Virus']
label_map = dict(zip(classes, range(len(classes))))

text_prompts = {
    "Bacteria": "a potato leaf infected with bacterial disease",
    "Fungi": "a potato leaf infected with fungal disease",
    "Healthy": "a healthy potato leaf with no disease",
    "Nematode": "a potato leaf infected with nematode disease",
    "Pest": "a potato leaf damaged by pests",
    "Phytopthora": "a potato leaf infected with phytopthora disease",
    "Virus": "a potato leaf infected with viral disease"
}

CLIP_MODEL_PATH = "best_vlm_model.pth"
T2T_MODEL_PATH = "best_t2t_recommendation_model.pth"
T2T_BASE_MODEL_NAME = "google/flan-t5-small"

# --- 2. RAG CHAT SETUP ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

rag = None  # Will be set if RAG deps are available

if RAG_AVAILABLE:
    print("--- Initializing RAG Chat System ---")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or "pcsk_2zLsPR_TW281dRvebjuvjaL6MbQLawuMjQyiYWj6wog7FSddx6otQaFj4ESRenCCnqYnmh"

    try:
        embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, model="embed-english-v3.0")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index("hi")
        vector_store = PineconeVectorStore(embedding=embeddings, index=index)
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192", temperature=0.1)
        print("✅ RAG components initialized.")
    except Exception as e:
        print(f"⚠️  RAG initialization failed: {e}")
        RAG_AVAILABLE = False
else:
    print("--- Skipping RAG Chat (dependencies unavailable) ---")
    print("   /chat endpoint will use Groq API fallback.")

# --- 3. MODEL DEFINITIONS ---
class CLIPFineTuner(nn.Module):
    def __init__(self, num_classes, unfreeze_layers=0):
        super(CLIPFineTuner, self).__init__()
        self.clip = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        for param in self.clip.parameters():
            param.requires_grad = False
        if unfreeze_layers > 0:
            for i, layer in enumerate(self.clip.vision_model.encoder.layers):
                if i >= len(self.clip.vision_model.encoder.layers) - unfreeze_layers:
                    for param in layer.parameters():
                        param.requires_grad = True
        projection_dim = self.clip.config.projection_dim
        self.classifier = nn.Sequential(
            nn.Linear(projection_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(512, num_classes)
        )

    def forward(self, batch):
        pixel_values = batch['pixel_values']
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        vision_outputs = self.clip.vision_model(pixel_values=pixel_values)
        image_embeds = vision_outputs[1]
        image_features = self.clip.visual_projection(image_embeds)
        text_outputs = self.clip.text_model(input_ids=input_ids, attention_mask=attention_mask)
        text_embeds = text_outputs[1]
        text_features = self.clip.text_projection(text_embeds)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        combined_features = image_features * 0.7 + text_features * 0.3
        logits = self.classifier(combined_features)
        return logits

if RAG_AVAILABLE:
    class RAGState(TypedDict):
        question: str
        documents: List[Document]
        answer: str

# --- 4. HELPER FUNCTIONS ---
def get_clip_disease_prediction(clip_model, processor, image_path, device):
    image = Image.open(image_path).convert("RGB")
    class_scores = {}

    clip_model.eval()
    with torch.no_grad():
        for class_name in classes:
            text = text_prompts[class_name]
            inputs = processor(
                text=text,
                images=image,
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=77
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            logits = clip_model(inputs)
            class_idx = label_map[class_name]
            class_scores[class_name] = logits[0, class_idx].item()

    # Move scores_tensor to the same device
    scores_tensor = torch.tensor(list(class_scores.values()), device=device)
    probs = torch.softmax(scores_tensor, dim=0)
    all_probs = {name: prob.item() for name, prob in zip(class_scores.keys(), probs)}

    predicted_class = max(all_probs, key=all_probs.get)
    confidence = all_probs[predicted_class]

    return predicted_class, confidence, all_probs

def get_t2t_recommendation(t2t_model, t2t_tokenizer, disease_name, device):
    # Create more specific prompts for better recommendations
    input_text = f"Provide specific treatment recommendations for potato {disease_name.lower()} disease including prevention and management strategies:"

    t2t_model.eval()
    with torch.no_grad():
        inputs = t2t_tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
        generated_ids = t2t_model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=256,  # Reduced for more focused output
            num_beams=3,     # Reduced beams for faster generation
            early_stopping=True,
            do_sample=True,  # Enable sampling for variety
            temperature=0.7, # Add some randomness
            repetition_penalty=1.2,  # Reduce repetition
            no_repeat_ngram_size=3   # Prevent 3-gram repetition
        )
        recommendation = t2t_tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    # If the model output is too generic, repetitive, or incomplete, provide fallback recommendations
    if (len(recommendation) < 100 or
        recommendation.count("common disease") > 1 or
        recommendation.endswith(":") or
        recommendation.count("include") > 2 or
        "strategies:" in recommendation and len(recommendation) < 150):
        recommendation = get_fallback_recommendation(disease_name)

    return recommendation

def get_fallback_recommendation(disease_name):
    """Provide specific treatment recommendations when T2T model output is inadequate"""
    recommendations = {
        "Bacteria": "Apply copper-based bactericides (copper sulfate or copper hydroxide). Remove infected plants immediately. Improve drainage and avoid overhead watering. Use certified disease-free seed potatoes. Rotate crops with non-solanaceous plants for 3-4 years.",

        "Fungi": "Apply fungicides containing chlorothalonil, mancozeb, or propiconazole. Ensure good air circulation around plants. Remove infected plant debris. Water at soil level to keep foliage dry. Use resistant potato varieties when available.",

        "Healthy": "Continue current care practices. Monitor regularly for early disease signs. Maintain proper spacing for air circulation. Water consistently at soil level. Apply balanced fertilizer and ensure good drainage.",

        "Nematode": "Use nematode-resistant potato varieties. Apply beneficial nematodes (Steinernema feltiae). Solarize soil before planting. Rotate with non-host crops like corn or wheat. Add organic matter to improve soil health.",

        "Pest": "Use integrated pest management (IPM). Apply neem oil or insecticidal soap for soft-bodied pests. Use row covers during vulnerable growth stages. Encourage beneficial insects. Remove pest-damaged plant parts promptly.",

        "Phytopthora": "Apply fungicides with metalaxyl or mefenoxam. Improve soil drainage immediately. Plant in raised beds if necessary. Use certified disease-free seed potatoes. Avoid overhead irrigation and ensure good air circulation.",

        "Virus": "Remove infected plants immediately to prevent spread. Control aphid vectors with insecticidal soap or neem oil. Use certified virus-free seed potatoes. Disinfect tools between plants. Plant resistant varieties when available."
    }

    return recommendations.get(disease_name, "Consult with a local agricultural extension office for specific treatment recommendations based on your location and growing conditions.")

def ask_via_groq(question: str) -> str:
    """Fallback: answer plant disease questions via Groq API directly."""
    if not GROQ_API_KEY:
        return "Chat service unavailable — GROQ_API_KEY not set."
    try:
        resp = http_requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": "You are an expert plant pathologist. Provide practical, actionable advice about crop diseases, pest management, and farming best practices."},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 600, "temperature": 0.7
            },
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        return f"Groq API error: {resp.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

if RAG_AVAILABLE:
    def retrieve(state: RAGState) -> RAGState:
        docs = vector_store.similarity_search(state["question"], k=3)
        return {"question": state["question"], "documents": docs, "answer": ""}

    def generate(state: RAGState) -> RAGState:
        context = "\n\n".join([doc.page_content for doc in state["documents"]])
        prompt = f"""You are an expert plant pathologist. Answer based on the research context.

Context: {context}

Question: {state["question"]}

Answer:"""
        response = llm.invoke(prompt)
        return {"question": state["question"], "documents": state["documents"], "answer": response.content}

def ask(question: str) -> str:
    """Ask a plant disease question and get an answer."""
    if rag is not None:
        try:
            result = rag.invoke({"question": question})
            return result["answer"]
        except Exception as e:
            print(f"RAG error, falling back to Groq: {e}")
    # Fallback to direct Groq
    return ask_via_groq(question)

# --- 5. INITIALIZE MODELS ---
print("\n--- Loading Models ---")

# Initialize plant disease prediction models
CLIP_LOADED = False
T2T_LOADED = False
clip_model_loaded = None
clip_processor = None
t2t_model_loaded = None
t2t_tokenizer = None

try:
    print("📦 Loading CLIP model...")
    clip_model_loaded = CLIPFineTuner(num_classes=len(classes), unfreeze_layers=2)
    checkpoint = torch.load(CLIP_MODEL_PATH, map_location=device)
    clip_model_loaded.load_state_dict(checkpoint["model"])
    clip_model_loaded.to(device)
    clip_model_loaded.eval()
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    print("✅ CLIP Model loaded successfully.")
    CLIP_LOADED = True
except Exception as e:
    print(f"❌ ERROR loading CLIP model: {str(e)}")
    print(f"   Model path: {CLIP_MODEL_PATH}")
    CLIP_LOADED = False

try:
    print("📦 Loading T2T Recommendation model...")
    t2t_tokenizer = T5TokenizerFast.from_pretrained(T2T_BASE_MODEL_NAME)
    t2t_model_loaded = T5ForConditionalGeneration.from_pretrained(T2T_BASE_MODEL_NAME)
    t2t_model_loaded.load_state_dict(torch.load(T2T_MODEL_PATH, map_location=device))
    t2t_model_loaded.to(device)
    t2t_model_loaded.eval()
    print("✅ T2T Recommendation Model loaded successfully.")
    T2T_LOADED = True
except Exception as e:
    print(f"❌ ERROR loading T2T model: {str(e)}")
    print(f"   Model path: {T2T_MODEL_PATH}")
    T2T_LOADED = False

print(f"\n📊 Model Loading Status:")
print(f"   CLIP Model: {'✅ Loaded' if CLIP_LOADED else '❌ Failed'}")
print(f"   T2T Model: {'✅ Loaded' if T2T_LOADED else '❌ Failed'}")

# Initialize RAG workflow (only if dependencies available)
if RAG_AVAILABLE:
    try:
        workflow = StateGraph(RAGState)
        workflow.add_node("retrieve", retrieve)
        workflow.add_node("generate", generate)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        rag = workflow.compile()
        print("✅ RAG System initialized successfully.")
    except Exception as e:
        print(f"⚠️  RAG workflow failed: {e}  — using Groq fallback for /chat")
        rag = None
else:
    print("ℹ️  RAG skipped — /chat will use Groq API directly.")

# --- 6. API ENDPOINTS ---
@app.route('/predict', methods=['POST'])
def predict():
    if not CLIP_LOADED or not T2T_LOADED:
        return jsonify({'error': 'Plant disease models are not properly loaded.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No image provided.'}), 400

    image_file = request.files['file']
    image_path = Path("temp_image.jpg")
    image_file.save(image_path)
    
    try:
        disease_class, confidence, all_probs = get_clip_disease_prediction(
            clip_model_loaded, clip_processor, image_path, device
        )
        
        recommendation = get_t2t_recommendation(
            t2t_model_loaded, t2t_tokenizer, disease_class, device
        )
        
        return jsonify({
            'disease': disease_class,
            'confidence': float(confidence),
            'all_probabilities': {k: float(v) for k, v in all_probs.items()},
            'recommendation': recommendation
        })
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500
    finally:
        # Clean up the temporary file
        if image_path.exists():
            image_path.unlink()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    answer = ask(question)
    return jsonify({'question': question, 'answer': answer})

@app.route('/simple-ai-advice', methods=['POST'])
def get_simple_ai_advice():
    """Get agricultural advice from simple AI agent"""
    if pestivid_agent is None:
        return jsonify({'error': 'Simple AI agent is not available. Install simple_ai_agent module.'}), 503

    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        result = pestivid_agent.get_crop_advice(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'AI advice error: {str(e)}'}), 500

@app.route('/analyze-description', methods=['POST'])
def analyze_crop_description():
    """Analyze crop issues based on text description"""
    if pestivid_agent is None:
        return jsonify({'error': 'Simple AI agent is not available. Install simple_ai_agent module.'}), 503

    data = request.json
    description = data.get('description', '')

    if not description:
        return jsonify({'error': 'Description is required'}), 400

    try:
        result = pestivid_agent.analyze_crop_image_description(description)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

@app.route('/seasonal-advice', methods=['POST'])
def get_seasonal_advice():
    """Get seasonal farming advice"""
    if pestivid_agent is None:
        return jsonify({'error': 'Simple AI agent is not available. Install simple_ai_agent module.'}), 503

    data = request.json
    season = data.get('season', '')
    crop = data.get('crop', None)

    if not season:
        return jsonify({'error': 'Season is required'}), 400

    try:
        result = pestivid_agent.get_seasonal_advice(season, crop)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Seasonal advice error: {str(e)}'}), 500

@app.route('/quick-tips', methods=['GET'])
def get_quick_tips():
    """Get quick farming tips"""
    if pestivid_agent is None:
        return jsonify({'error': 'Simple AI agent is not available. Install simple_ai_agent module.'}), 503

    try:
        tips = pestivid_agent.get_quick_tips()
        return jsonify({'tips': tips})
    except Exception as e:
        return jsonify({'error': f'Tips error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'clip_model': CLIP_LOADED,
        't2t_model': T2T_LOADED,
        'rag_system': rag is not None,
        'rag_fallback': rag is None and GROQ_API_KEY is not None,
        'simple_ai_agent': pestivid_agent is not None,
        'device': device
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
