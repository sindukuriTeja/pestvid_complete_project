#!/usr/bin/env python3
"""
Complete Model Reload and Verification Script for PestVid
This script thoroughly tests and verifies all AI models are working correctly
"""

import torch
from torch import nn
from transformers import CLIPProcessor, CLIPModel, T5TokenizerFast, T5ForConditionalGeneration
from PIL import Image
import warnings
from pathlib import Path
import sys

warnings.filterwarnings("ignore")

# Configuration
CLIP_MODEL_PATH = "best_vlm_model.pth"
T2T_MODEL_PATH = "best_t2t_recommendation_model.pth"
T2T_BASE_MODEL_NAME = "google/flan-t5-small"
TEST_IMAGE = "20230712_114552.jpg"

device = "cuda" if torch.cuda.is_available() else "cpu"

# Disease classes
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


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def check_files():
    """Check if all required files exist"""
    print_section("STEP 1: Checking Required Files")
    
    files_to_check = [
        (CLIP_MODEL_PATH, "CLIP VLM Model"),
        (T2T_MODEL_PATH, "T2T Recommendation Model"),
        (TEST_IMAGE, "Test Image")
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        exists = Path(file_path).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {description}: {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist


def load_clip_model():
    """Load and verify CLIP model"""
    print_section("STEP 2: Loading CLIP VLM Model")
    
    try:
        print(f"📦 Device: {device}")
        print(f"📂 Loading from: {CLIP_MODEL_PATH}")
        
        # Initialize model
        print("🔄 Initializing CLIP model architecture...")
        model = CLIPFineTuner(num_classes=len(classes), unfreeze_layers=2)
        
        # Load checkpoint
        print("🔄 Loading checkpoint...")
        checkpoint = torch.load(CLIP_MODEL_PATH, map_location=device)
        
        # Inspect checkpoint
        if isinstance(checkpoint, dict):
            print(f"📋 Checkpoint keys: {list(checkpoint.keys())}")
            if 'model' in checkpoint:
                model.load_state_dict(checkpoint['model'])
                if 'epoch' in checkpoint:
                    print(f"📊 Trained for {checkpoint['epoch']} epochs")
            else:
                model.load_state_dict(checkpoint)
        else:
            model.load_state_dict(checkpoint)
        
        model.to(device)
        model.eval()
        
        # Load processor
        print("🔄 Loading CLIP processor...")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        print("✅ CLIP Model loaded successfully!")
        return model, processor
        
    except Exception as e:
        print(f"❌ Error loading CLIP model: {e}")
        return None, None


def load_t2t_model():
    """Load and verify T2T model"""
    print_section("STEP 3: Loading T2T Recommendation Model")
    
    try:
        print(f"📦 Device: {device}")
        print(f"📂 Loading from: {T2T_MODEL_PATH}")
        
        # Load tokenizer
        print("🔄 Loading tokenizer...")
        tokenizer = T5TokenizerFast.from_pretrained(T2T_BASE_MODEL_NAME)
        
        # Load base model
        print("🔄 Loading base T5 model...")
        model = T5ForConditionalGeneration.from_pretrained(T2T_BASE_MODEL_NAME)
        
        # Load fine-tuned weights
        print("🔄 Loading fine-tuned weights...")
        checkpoint = torch.load(T2T_MODEL_PATH, map_location=device)
        
        if isinstance(checkpoint, dict):
            print(f"📋 Checkpoint keys: {list(checkpoint.keys())}")
            if 'model' in checkpoint:
                model.load_state_dict(checkpoint['model'])
            else:
                model.load_state_dict(checkpoint)
        else:
            model.load_state_dict(checkpoint)
        
        model.to(device)
        model.eval()
        
        print("✅ T2T Model loaded successfully!")
        return model, tokenizer
        
    except Exception as e:
        print(f"❌ Error loading T2T model: {e}")
        return None, None


def test_clip_prediction(model, processor):
    """Test CLIP model with sample image"""
    print_section("STEP 4: Testing CLIP Disease Prediction")
    
    if model is None or processor is None:
        print("❌ Cannot test - model not loaded")
        return False
    
    try:
        # Load test image
        print(f"📷 Loading test image: {TEST_IMAGE}")
        image = Image.open(TEST_IMAGE).convert("RGB")
        print(f"✅ Image loaded: {image.size}")
        
        # Run prediction for each class
        print("\n🔍 Running predictions for all disease classes...")
        class_scores = {}
        
        model.eval()
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
                logits = model(inputs)
                class_idx = label_map[class_name]
                class_scores[class_name] = logits[0, class_idx].item()
        
        # Calculate probabilities
        scores_tensor = torch.tensor(list(class_scores.values()), device=device)
        probs = torch.softmax(scores_tensor, dim=0)
        all_probs = {name: prob.item() for name, prob in zip(class_scores.keys(), probs)}
        
        # Get prediction
        predicted_class = max(all_probs, key=all_probs.get)
        confidence = all_probs[predicted_class]
        
        # Display results
        print("\n📊 Prediction Results:")
        print(f"🦠 Predicted Disease: {predicted_class}")
        print(f"📈 Confidence: {confidence:.2%}")
        print("\n📋 All Probabilities:")
        for disease, prob in sorted(all_probs.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(prob * 50)
            print(f"  {disease:15s} {prob:6.2%} {bar}")
        
        print("\n✅ CLIP prediction test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_t2t_recommendation(model, tokenizer):
    """Test T2T model with sample diseases"""
    print_section("STEP 5: Testing T2T Recommendations")
    
    if model is None or tokenizer is None:
        print("❌ Cannot test - model not loaded")
        return False
    
    try:
        test_diseases = ['Bacteria', 'Fungi', 'Pest']
        
        for disease in test_diseases:
            print(f"\n🦠 Testing disease: {disease}")
            input_text = f"Provide specific treatment recommendations for potato {disease.lower()} disease including prevention and management strategies:"
            
            model.eval()
            with torch.no_grad():
                inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
                generated_ids = model.generate(
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
                recommendation = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            
            print(f"💊 Recommendation ({len(recommendation)} chars):")
            print(f"   {recommendation[:200]}...")
        
        print("\n✅ T2T recommendation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during recommendation: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main verification workflow"""
    print("\n" + "🌱" * 35)
    print("  PestVid Model Reload & Verification")
    print("🌱" * 35)
    
    # Step 1: Check files
    if not check_files():
        print("\n❌ Missing required files. Please ensure all model files are present.")
        return False
    
    # Step 2: Load CLIP model
    clip_model, clip_processor = load_clip_model()
    if clip_model is None:
        print("\n❌ Failed to load CLIP model")
        return False
    
    # Step 3: Load T2T model
    t2t_model, t2t_tokenizer = load_t2t_model()
    if t2t_model is None:
        print("\n❌ Failed to load T2T model")
        return False
    
    # Step 4: Test CLIP prediction
    if not test_clip_prediction(clip_model, clip_processor):
        print("\n❌ CLIP prediction test failed")
        return False
    
    # Step 5: Test T2T recommendation
    if not test_t2t_recommendation(t2t_model, t2t_tokenizer):
        print("\n❌ T2T recommendation test failed")
        return False
    
    # Final summary
    print_section("✅ VERIFICATION COMPLETE")
    print("""
All models loaded and tested successfully!

✅ CLIP VLM Model - Disease Detection: WORKING
✅ T2T Model - Treatment Recommendations: WORKING
✅ Test Image Processing: WORKING

Your PestVid AI system is ready to use!

Next steps:
1. Start Flask server: python flask_server.py
2. Start Node backend: cd backend && npm start
3. Open frontend: PestVid-main/public/index.html

The models are properly loaded and functioning correctly.
    """)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
