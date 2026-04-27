"""
Test script to verify both models load correctly
This will help diagnose any model loading issues
"""
import sys
import os
import warnings
warnings.filterwarnings("ignore")

print("=" * 80)
print("🧪 PestVid Model Loading Test")
print("=" * 80)

# Check if model files exist
print("\n1️⃣ Checking model files...")
CLIP_MODEL_PATH = "best_vlm_model.pth"
T2T_MODEL_PATH = "best_t2t_recommendation_model.pth"

clip_exists = os.path.exists(CLIP_MODEL_PATH)
t2t_exists = os.path.exists(T2T_MODEL_PATH)

print(f"   CLIP model ({CLIP_MODEL_PATH}): {'✅ Found' if clip_exists else '❌ Missing'}")
if clip_exists:
    size_mb = os.path.getsize(CLIP_MODEL_PATH) / (1024 * 1024)
    print(f"      Size: {size_mb:.2f} MB")

print(f"   T2T model ({T2T_MODEL_PATH}): {'✅ Found' if t2t_exists else '❌ Missing'}")
if t2t_exists:
    size_mb = os.path.getsize(T2T_MODEL_PATH) / (1024 * 1024)
    print(f"      Size: {size_mb:.2f} MB")

if not clip_exists or not t2t_exists:
    print("\n❌ ERROR: Model files are missing!")
    print("   Please ensure both .pth files are in the current directory.")
    sys.exit(1)

# Check dependencies
print("\n2️⃣ Checking dependencies...")
missing_deps = []

try:
    import torch
    from torch import nn
    print(f"   ✅ PyTorch {torch.__version__}")
except ImportError:
    print("   ❌ PyTorch not installed")
    missing_deps.append("torch")

try:
    from transformers import CLIPProcessor, CLIPModel, T5TokenizerFast, T5ForConditionalGeneration
    import transformers
    print(f"   ✅ Transformers {transformers.__version__}")
except ImportError:
    print("   ❌ Transformers not installed")
    missing_deps.append("transformers")

try:
    from PIL import Image
    print("   ✅ Pillow")
except ImportError:
    print("   ❌ Pillow not installed")
    missing_deps.append("pillow")

if missing_deps:
    print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
    print(f"   Install with: pip install {' '.join(missing_deps)}")
    sys.exit(1)

# Device check
print("\n3️⃣ Checking compute device...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"   Device: {device}")
if device == "cuda":
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
    print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Define model classes
print("\n4️⃣ Loading CLIP model...")
classes = ['Bacteria', 'Fungi', 'Healthy', 'Nematode', 'Pest', 'Phytopthora', 'Virus']

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

try:
    print("   📦 Initializing CLIP architecture...")
    clip_model = CLIPFineTuner(num_classes=len(classes), unfreeze_layers=2)
    
    print("   📦 Loading checkpoint...")
    checkpoint = torch.load(CLIP_MODEL_PATH, map_location=device)
    
    print("   📦 Inspecting checkpoint...")
    if isinstance(checkpoint, dict):
        print(f"      Checkpoint keys: {list(checkpoint.keys())}")
        if 'model' in checkpoint:
            clip_model.load_state_dict(checkpoint['model'])
            if 'epoch' in checkpoint:
                print(f"      Trained epochs: {checkpoint['epoch']}")
        else:
            clip_model.load_state_dict(checkpoint)
    else:
        clip_model.load_state_dict(checkpoint)
    
    clip_model.to(device)
    clip_model.eval()
    
    print("   📦 Loading CLIP processor...")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    print("   ✅ CLIP Model loaded successfully!")
    CLIP_LOADED = True
except Exception as e:
    print(f"   ❌ CLIP loading failed: {str(e)}")
    import traceback
    traceback.print_exc()
    CLIP_LOADED = False

# Load T2T model
print("\n5️⃣ Loading T2T Recommendation model...")
T2T_BASE_MODEL_NAME = "google/flan-t5-small"

try:
    print(f"   📦 Loading tokenizer from {T2T_BASE_MODEL_NAME}...")
    t2t_tokenizer = T5TokenizerFast.from_pretrained(T2T_BASE_MODEL_NAME)
    
    print(f"   📦 Loading base T5 model...")
    t2t_model = T5ForConditionalGeneration.from_pretrained(T2T_BASE_MODEL_NAME)
    
    print("   📦 Loading fine-tuned weights...")
    checkpoint = torch.load(T2T_MODEL_PATH, map_location=device)
    
    if isinstance(checkpoint, dict):
        print(f"      Checkpoint keys: {list(checkpoint.keys())}")
        if 'model' in checkpoint:
            t2t_model.load_state_dict(checkpoint['model'])
        else:
            t2t_model.load_state_dict(checkpoint)
    else:
        t2t_model.load_state_dict(checkpoint)
    
    t2t_model.to(device)
    t2t_model.eval()
    
    print("   ✅ T2T Model loaded successfully!")
    T2T_LOADED = True
except Exception as e:
    print(f"   ❌ T2T loading failed: {str(e)}")
    import traceback
    traceback.print_exc()
    T2T_LOADED = False

# Summary
print("\n" + "=" * 80)
print("📊 FINAL RESULTS")
print("=" * 80)
print(f"CLIP Model: {'✅ LOADED' if CLIP_LOADED else '❌ FAILED'}")
print(f"T2T Model:  {'✅ LOADED' if T2T_LOADED else '❌ FAILED'}")

if CLIP_LOADED and T2T_LOADED:
    print("\n🎉 SUCCESS! Both models loaded correctly.")
    print("   You can now run the Flask server with:")
    print("   python flask_server.py")
    print("   or")
    print("   python flask_server_with_models.py")
else:
    print("\n❌ FAILURE! One or more models failed to load.")
    print("   Check the error messages above for details.")
    sys.exit(1)

print("=" * 80)
