# How to Clear Browser Cache and See the Fixes

## The Problem
Your browser is caching the old version of the HTML file, so you're still seeing:
1. RAG error messages in AgriBot
2. "Unknown" disease name in Plant Analysis

## The Solution - Clear Browser Cache

### Method 1: Hard Refresh (Quickest)
**Windows/Linux:**
- Press `Ctrl + Shift + R` or `Ctrl + F5`

**Mac:**
- Press `Cmd + Shift + R`

### Method 2: Clear Cache via DevTools (Most Reliable)
1. Open DevTools: Press `F12`
2. Right-click on the refresh button (while DevTools is open)
3. Select "Empty Cache and Hard Reload"

### Method 3: Clear All Browser Data
**Chrome/Edge:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Select "All time"
4. Click "Clear data"

**Firefox:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cache"
3. Click "Clear Now"

### Method 4: Clear localStorage (For AgriBot Chat History)
1. Open DevTools: Press `F12`
2. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
3. Expand "Local Storage"
4. Click on "http://localhost:3001"
5. Find keys starting with `pestivid_agribot_chat_`
6. Right-click and delete them
7. Refresh the page

## After Clearing Cache

### Test Plant Analysis:
1. Go to Plant Analysis page
2. Upload the sample image (20230712_114552.jpg)
3. Click "Analyze Plant"
4. **Expected Result:** Disease name should show (e.g., "Fungi", "Pest", etc.) instead of "Unknown"

### Test AgriBot:
1. Go to AgriBot page
2. You should see: "Welcome, [Your Name]!" (not "User: teja (Role: Farmer)")
3. Type a question: "How to prevent tomato blight?"
4. **Expected Result:** AgriBot responds with helpful advice (no RAG error)

## If Issues Persist

### Check Console for Errors:
1. Press `F12` to open DevTools
2. Go to "Console" tab
3. Look for any red error messages
4. Check the "Network" tab to see API responses

### Verify Servers are Running:
```bash
# Check if Flask server is running
curl http://localhost:5000/quick-tips

# Check if Node.js backend is running
curl http://localhost:3001
```

### Manual Test of Flask API:
Open a new terminal and run:
```bash
cd PestVid-main
curl -X POST http://localhost:5000/simple-ai-advice -H "Content-Type: application/json" -d "{\"query\":\"How to grow tomatoes?\"}"
```

Expected response should include `"advice"` field with helpful information.

## Quick Fix Script

Run this in your browser console (F12 → Console tab):
```javascript
// Clear all PestVid localStorage
Object.keys(localStorage).forEach(key => {
    if (key.includes('pestivid')) {
        localStorage.removeItem(key);
    }
});
console.log('PestVid cache cleared! Please refresh the page.');
```

Then press `Ctrl + Shift + R` to hard refresh.

---

## What Was Fixed in the Code

### 1. Plant Analysis (Disease Name)
- **Before:** Looking for `result.predicted_disease`
- **After:** Looking for `result.disease` (correct field from Flask API)
- **Line:** 3320 in index.html

### 2. AgriBot Chat
- **Before:** Using `/chat` endpoint (RAG system)
- **After:** Using `/simple-ai-advice` endpoint (Simple AI Agent)
- **Line:** 3395 in index.html

### 3. User Greeting
- **Before:** "User: teja (Role: Farmer)"
- **After:** "Welcome, teja!"
- **Line:** 1055 in index.html

All fixes are in the code - you just need to clear the cache to see them!
