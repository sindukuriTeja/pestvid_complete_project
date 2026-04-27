#!/usr/bin/env python3
"""
Test script to check T2T recommendation model functionality
"""

import torch
from transformers import T5TokenizerFast, T5ForConditionalGeneration
import warnings
warnings.filterwarnings("ignore")

# Configuration
T2T_MODEL_PATH = "best_t2t_recommendation_model.pth"
T2T_BASE_MODEL_NAME = "google/flan-t5-small"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")

def get_t2t_recommendation(t2t_model, t2t_tokenizer, disease_name, device):
    """Generate treatment recommendation for a given disease"""
    # Create more specific prompts for better recommendations
    input_text = f"Provide specific treatment recommendations for potato {disease_name.lower()} disease including prevention and management strategies:"
    print(f"Input text: {input_text}")

    t2t_model.eval()
    with torch.no_grad():
        inputs = t2t_tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
        print(f"Tokenized input shape: {inputs['input_ids'].shape}")

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
        print(f"Using fallback recommendation for {disease_name}")

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

def main():
    print("--- Testing T2T Recommendation Model ---")
    
    # Load model and tokenizer
    try:
        print("Loading tokenizer...")
        t2t_tokenizer = T5TokenizerFast.from_pretrained(T2T_BASE_MODEL_NAME)
        print("✅ Tokenizer loaded successfully.")
        
        print("Loading base model...")
        t2t_model_loaded = T5ForConditionalGeneration.from_pretrained(T2T_BASE_MODEL_NAME)
        print("✅ Base model loaded successfully.")
        
        print("Loading fine-tuned weights...")
        checkpoint = torch.load(T2T_MODEL_PATH, map_location=device)
        print(f"Checkpoint keys: {list(checkpoint.keys()) if isinstance(checkpoint, dict) else 'Not a dict'}")
        
        # Load the state dict
        if isinstance(checkpoint, dict) and 'model' in checkpoint:
            t2t_model_loaded.load_state_dict(checkpoint['model'])
        elif isinstance(checkpoint, dict):
            t2t_model_loaded.load_state_dict(checkpoint)
        else:
            print("❌ Unexpected checkpoint format")
            return
            
        t2t_model_loaded.to(device)
        t2t_model_loaded.eval()
        print("✅ T2T Recommendation Model loaded successfully.")
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: Model file not found: {e}")
        return
    except Exception as e:
        print(f"❌ ERROR loading model: {e}")
        return
    
    # Test with different disease types
    test_diseases = ['Bacteria', 'Fungi', 'Healthy', 'Nematode', 'Pest', 'Phytopthora', 'Virus']
    
    print("\n--- Testing Recommendations ---")
    for disease in test_diseases:
        print(f"\n🔍 Testing disease: {disease}")
        try:
            recommendation = get_t2t_recommendation(t2t_model_loaded, t2t_tokenizer, disease, device)
            print(f"📝 Recommendation: {recommendation}")
            print(f"📏 Length: {len(recommendation)} characters")
        except Exception as e:
            print(f"❌ Error generating recommendation for {disease}: {e}")

if __name__ == "__main__":
    main()
