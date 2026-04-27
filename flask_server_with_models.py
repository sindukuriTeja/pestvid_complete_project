"""
Flask Server with PyTorch Model Loading for Plant Disease Detection
This version loads the actual trained models without RAG dependencies
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from torch import nn
from transformers import CLIPProcessor, CLIPModel, T5TokenizerFast, T5ForConditionalGeneration
from PIL import Image
from pathlib import Path
import warnings
from dotenv import load_dotenv
from simple_ai_agent import pestivid_agent

warnings.filterwarnings("ignore")
load_dotenv()

app = Flask(__name__)
CORS(app)

print("=" * 80)
print("🌱 PestVid Flask Server with PyTorch Models")
print("=" * 80)

# Device configuration
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"📱 Using device: {device}")

# Disease classes
classes = ['Bacteria', 'Fungi', 'Healthy', 'Nematode', 'Pest', 'Phytopthora', 'Virus']
label_map = dict(zip(classes, range(len(classes))))

# Text prompts for CLIP model
text_prompts = {
    "Bacteria": "a potato leaf infected with bacterial disease",
    "Fungi": "a potato leaf infected with fungal disease",
    "Healthy": "a healthy potato leaf with no disease",
    "Nematode": "a potato leaf infected with nematode disease",
    "Pest": "a potato leaf damaged by pests",
    "Phytopthora": "a potato leaf infected with phytopthora disease",
    "Virus": "a potato leaf infected with viral disease"
}

# Model paths
CLIP_MODEL_PATH = "best_vlm_model.pth"
T2T_MODEL_PATH = "best_t2t_recommendation_model.pth"
T2T_BASE_MODEL_NAME = "google/flan-t5-small"

# Model definition
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

def get_clip_disease_prediction(clip_model, processor, image_path, device):
    """Predict disease from image using CLIP model"""
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

    scores_tensor = torch.tensor(list(class_scores.values()), device=device)
    probs = torch.softmax(scores_tensor, dim=0)
    all_probs = {name: prob.item() for name, prob in zip(class_scores.keys(), probs)}

    predicted_class = max(all_probs, key=all_probs.get)
    confidence = all_probs[predicted_class]

    return predicted_class, confidence, all_probs

def get_t2t_recommendation(t2t_model, t2t_tokenizer, disease_name, device):
    """Generate treatment recommendation using T2T model"""
    input_text = f"Provide specific treatment recommendations for potato {disease_name.lower()} disease including prevention and management strategies:"

    t2t_model.eval()
    with torch.no_grad():
        inputs = t2t_tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
        generated_ids = t2t_model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=256,
            num_beams=3,
            early_stopping=True,
            do_sample=True,
            temperature=0.7,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3
        )
        recommendation = t2t_tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    # Fallback if output is inadequate
    if len(recommendation) < 100 or recommendation.count("common disease") > 1:
        recommendation = get_fallback_recommendation(disease_name)

    return recommendation

def get_fallback_recommendation(disease_name):
    """Provide specific treatment recommendations"""
    recommendations = {
        "Bacteria": "Apply copper-based bactericides (copper sulfate or copper hydroxide). Remove infected plants immediately. Improve drainage and avoid overhead watering. Use certified disease-free seed potatoes. Rotate crops with non-solanaceous plants for 3-4 years.",
        "Fungi": "Apply fungicides containing chlorothalonil, mancozeb, or propiconazole. Ensure good air circulation around plants. Remove infected plant debris. Water at soil level to keep foliage dry. Use resistant potato varieties when available.",
        "Healthy": "Continue current care practices. Monitor regularly for early disease signs. Maintain proper spacing for air circulation. Water consistently at soil level. Apply balanced fertilizer and ensure good drainage.",
        "Nematode": "Use nematode-resistant potato varieties. Apply beneficial nematodes (Steinernema feltiae). Solarize soil before planting. Rotate with non-host crops like corn or wheat. Add organic matter to improve soil health.",
        "Pest": "Use integrated pest management (IPM). Apply neem oil or insecticidal soap for soft-bodied pests. Use row covers during vulnerable growth stages. Encourage beneficial insects. Remove pest-damaged plant parts promptly.",
        "Phytopthora": "Apply fungicides with metalaxyl or mefenoxam. Improve soil drainage immediately. Plant in raised beds if necessary. Use certified disease-free seed potatoes. Avoid overhead irrigation and ensure good air circulation.",
        "Virus": "Remove infected plants immediately to prevent spread. Control aphid vectors with insecticidal soap or neem oil. Use certified virus-free seed potatoes. Disinfect tools between plants. Plant resistant varieties when available."
    }
    return recommendations.get(disease_name, "Consult with a local agricultural extension office for specific treatment recommendations.")

# Initialize models
print("\n🔄 Loading PyTorch Models...")
print("-" * 80)

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
    print("✅ CLIP Model loaded successfully!")
    CLIP_LOADED = True
except Exception as e:
    print(f"❌ ERROR loading CLIP model: {str(e)}")

try:
    print("📦 Loading T2T Recommendation model...")
    t2t_tokenizer = T5TokenizerFast.from_pretrained(T2T_BASE_MODEL_NAME)
    t2t_model_loaded = T5ForConditionalGeneration.from_pretrained(T2T_BASE_MODEL_NAME)
    t2t_model_loaded.load_state_dict(torch.load(T2T_MODEL_PATH, map_location=device))
    t2t_model_loaded.to(device)
    t2t_model_loaded.eval()
    print("✅ T2T Recommendation Model loaded successfully!")
    T2T_LOADED = True
except Exception as e:
    print(f"❌ ERROR loading T2T model: {str(e)}")

print("-" * 80)
print(f"📊 Model Status: CLIP={CLIP_LOADED}, T2T={T2T_LOADED}")
print("=" * 80)

# API Endpoints
@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'PestVid Flask Server with PyTorch Models',
        'models_loaded': {
            'clip': CLIP_LOADED,
            't2t': T2T_LOADED
        },
        'available_endpoints': [
            '/predict',
            '/simple-ai-advice',
            '/analyze-description',
            '/seasonal-advice',
            '/quick-tips'
        ]
    })

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """Predict plant disease from uploaded image"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    print("=" * 60)
    print("🔍 Plant Disease Prediction Request")
    print("=" * 60)

    if not CLIP_LOADED or not T2T_LOADED:
        print("❌ Models not loaded")
        return jsonify({'error': 'Plant disease models are not properly loaded.'}), 500

    if 'file' not in request.files:
        print("❌ No file in request")
        return jsonify({'error': 'No image provided.'}), 400

    image_file = request.files['file']
    print(f"📁 File received: {image_file.filename}")
    
    image_path = Path("temp_image.jpg")
    image_file.save(image_path)
    
    try:
        print("🤖 Running CLIP disease prediction...")
        disease_class, confidence, all_probs = get_clip_disease_prediction(
            clip_model_loaded, clip_processor, image_path, device
        )
        print(f"📊 Predicted: {disease_class} ({confidence:.2%})")
        
        print("💊 Generating treatment recommendation...")
        recommendation = get_t2t_recommendation(
            t2t_model_loaded, t2t_tokenizer, disease_class, device
        )
        
        print("✅ Prediction complete!")
        print("=" * 60)
        
        import time
        response_data = {
            'disease': disease_class,
            'confidence': f"{confidence:.1%}",
            'all_probabilities': {k: f"{v:.1%}" for k, v in all_probs.items()},
            'recommendation': recommendation,
            'status': 'success',
            'timestamp': int(time.time()),
            'model': 'PyTorch CLIP + T5'
        }
        
        response = jsonify(response_data)
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.add('Pragma', 'no-cache')
        response.headers.add('Expires', '0')
        return response, 200
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        print("=" * 60)
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500
    finally:
        if image_path.exists():
            image_path.unlink()

@app.route('/simple-ai-advice', methods=['POST'])
def get_simple_ai_advice():
    """Get agricultural advice from simple AI agent"""
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
    try:
        tips = pestivid_agent.get_quick_tips()
        return jsonify({'tips': tips})
    except Exception as e:
        return jsonify({'error': f'Tips error: {str(e)}'}), 500

if __name__ == '__main__':
    print("\n🚀 Server starting on http://localhost:5000")
    print("📝 Test with: curl http://localhost:5000/quick-tips")
    print("=" * 80)
    app.run(host='0.0.0.0', port=5000, debug=True)
