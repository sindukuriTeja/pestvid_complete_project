# PestVid Model Loading Guide

## Overview

PestVid uses two PyTorch models for plant disease detection:

1. **CLIP VLM Model** (`best_vlm_model.pth`) - 721 MB
   - Vision-Language Model for disease classification
   - Identifies 7 disease types: Bacteria, Fungi, Healthy, Nematode, Pest, Phytopthora, Virus

2. **T2T Recommendation Model** (`best_t2t_recommendation_model.pth`) - 307 MB
   - Text-to-Text model for treatment recommendations
   - Based on Google's FLAN-T5-small architecture

## Quick Start

### 1. Test Model Loading

Run the test script to verify both models load correctly:

```bash
python test_model_loading.py
```

This will check:
- ✅ Model files exist
- ✅ Dependencies are installed
- ✅ Models load without errors
- ✅ Device (CPU/GPU) is configured

### 2. Start the Server

**Option A: Use the startup script (Windows)**
```bash
START_SERVER.bat
```

**Option B: Run directly**
```bash
python flask_server_with_models.py
```

**Option C: Full server with RAG (requires additional dependencies)**
```bash
python flask_server.py
```

## Troubleshooting

### Issue: Models Not Loading

**Symptoms:**
- Error messages during server startup
- `/predict` endpoint returns 500 error
- "Models not properly loaded" message

**Solutions:**

1. **Check model files exist:**
   ```bash
   dir *.pth
   ```
   You should see both `.pth` files in the directory.

2. **Verify file sizes:**
   - `best_vlm_model.pth` should be ~721 MB
   - `best_t2t_recommendation_model.pth` should be ~307 MB
   
   If files are much smaller, they may be corrupted.

3. **Check dependencies:**
   ```bash
   pip install torch transformers pillow
   ```

4. **Test with diagnostic script:**
   ```bash
   python test_model_loading.py
   ```

### Issue: FileNotFoundError

**Cause:** Model files are not in the correct location.

**Solution:** Ensure both `.pth` files are in the same directory as the Flask server scripts.

### Issue: KeyError or RuntimeError

**Cause:** Model checkpoint format mismatch.

**Solution:** The updated code now handles both checkpoint formats:
- Dictionary with 'model' key: `checkpoint['model']`
- Direct state dict: `checkpoint`

### Issue: Out of Memory (OOM)

**Cause:** Models are too large for available RAM/VRAM.

**Solutions:**
1. Close other applications
2. Use CPU instead of GPU (automatic fallback)
3. Increase system swap/page file

### Issue: Slow Loading

**Cause:** Large model files take time to load.

**Expected behavior:**
- First load: 30-60 seconds (downloads CLIP/T5 base models)
- Subsequent loads: 10-20 seconds

## Model Loading Process

### CLIP Model Loading Steps:

1. Initialize CLIPFineTuner architecture
2. Load checkpoint from `best_vlm_model.pth`
3. Extract state dict (handles both formats)
4. Load weights into model
5. Move to device (CPU/GPU)
6. Set to evaluation mode
7. Load CLIP processor

### T2T Model Loading Steps:

1. Load T5 tokenizer from HuggingFace
2. Load base T5 model from HuggingFace
3. Load fine-tuned weights from `best_t2t_recommendation_model.pth`
4. Extract state dict (handles both formats)
5. Load weights into model
6. Move to device (CPU/GPU)
7. Set to evaluation mode

## Error Handling Improvements

The updated code now includes:

✅ **Comprehensive exception handling** - Catches all exceptions, not just FileNotFoundError
✅ **Detailed error messages** - Shows exact error and model path
✅ **Graceful degradation** - Server starts even if models fail (with limited functionality)
✅ **Status reporting** - `/health` endpoint shows model loading status
✅ **Diagnostic logging** - Clear console output during loading

## Server Options

### flask_server_with_models.py (Recommended)
- ✅ Loads both PyTorch models
- ✅ Full disease prediction
- ✅ Treatment recommendations
- ✅ Simple AI agent features
- ❌ No RAG chat (requires LangChain)

### flask_server.py (Full Featured)
- ✅ Loads both PyTorch models
- ✅ Full disease prediction
- ✅ Treatment recommendations
- ✅ RAG chat system (if dependencies available)
- ✅ Simple AI agent features
- ⚠️ Requires additional dependencies

### flask_server_simple.py (Lightweight)
- ❌ No model loading
- ❌ No disease prediction
- ✅ Simple AI agent features only
- ✅ Minimal dependencies

## Health Check

Check model status via API:

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "ok",
  "clip_model": true,
  "t2t_model": true,
  "device": "cuda",
  "rag_system": false
}
```

## Performance Tips

1. **Use GPU if available** - Automatic detection, 5-10x faster
2. **Keep models loaded** - Don't restart server unnecessarily
3. **Batch predictions** - Process multiple images in sequence
4. **Monitor memory** - Each model uses ~1-2 GB RAM

## Dependencies

### Core (Required for models):
```
torch>=2.0.0
transformers>=4.30.0
pillow>=9.0.0
```

### Server (Required):
```
flask>=2.0.0
flask-cors>=3.0.0
python-dotenv>=0.19.0
```

### Optional (RAG features):
```
langchain
langchain-cohere
langchain-pinecone
langchain-groq
pinecone-client
langgraph
```

## Support

If you continue to experience issues:

1. Run `python test_model_loading.py` and share the output
2. Check the console output when starting the server
3. Verify model file integrity (checksums if available)
4. Ensure Python version is 3.8 or higher

## Changes Made

### Fixed Issues:

1. ✅ **Exception handling** - Changed from `FileNotFoundError` to `Exception` to catch all errors
2. ✅ **Variable initialization** - Added explicit initialization of model variables to None
3. ✅ **Error messages** - Added detailed error output with model paths
4. ✅ **Status reporting** - Added summary of loading status
5. ✅ **Diagnostic tools** - Created test script for troubleshooting

### Files Modified:

- `flask_server.py` - Improved error handling
- `test_model_loading.py` - New diagnostic script
- `START_SERVER.bat` - New startup script with validation
- `MODEL_LOADING_GUIDE.md` - This guide

Both models should now load correctly and provide detailed error messages if any issues occur.
