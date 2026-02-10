# 🚀 QUICK START - Smart Waste Classifier

##⚡ **START IN 3 COMMANDS**

```bash
# 1. Activate environment
D:\Hackthon-garbage\.venv\Scripts\activate

# 2. Start server (from backend directory)
cd D:\Hackthon-garbage\backend
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

# 3. Open browser
http://127.0.0.1:8000
```

---

## 🎯 **WHAT WORKS RIGHT NOW**

✅ **Backend (FastAPI)**
- Model loaded: YOLO v8 with 3 classes
- API endpoints: `/health`, `/api/classify`, `/api/categories`
- Gemini fallback: Working without API key

✅ **Frontend**
- Beautiful UI with drag-drop upload
- Color-coded dustbin visuals
- Confidence scoring
- Awareness tips display

✅ **AI Model**
- File: `backend/model/best.pt` (5.95 MB)
- Classes: BIODEGRADABLE → ORGANIC, RECYCLABLE, HAZARDOUS
- Detection: Object detection task

---

## 🔑 **OPTIONAL: ADD GEMINI AI**

Get FREE API key: https://makersuite.google.com/app/apikey

```bash
# Add to backend/.env
GEMINI_API_KEY=your_actual_api_key_here
ENABLE_GEMINI=true
```

Then restart server. Gemini will generate smart awareness tips!

---

## 🧪 **TEST THE API**

```bash
# Health check
curl http://127.0.0.1:8000/health

# Classify image
curl -X POST http://127.0.0.1:8000/api/classify \
  -F "file=@your_waste_image.jpg"
```

---

## 📱 **HOW TO USE**

1. Open `http://127.0.0.1:8000` in browser
2. Upload/drag waste image
3. Click "Classify Waste"
4. See results:
   - Category (ORGANIC/RECYCLABLE/HAZARDOUS)
   - Dustbin color
   - Confidence score
   - Awareness tip
   - Safety warning (if low confidence)

---

## 🛠️ **TROUBLESHOOTING**

**Server won't start?**
```bash
# Check if port is free
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F

# Restart
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Model not loading?**
```bash
# Test model directly
python test_model.py

# Output should show:
# ✅ Model loaded successfully!
# Model Classes: BIODEGRADABLE, RECYCLABLE, HAZARDOUS
```

**Frontend not showing?**
- Ensure server is running first
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors

---

## 🌐 **FOR JUDGES / DEMO**

**Best Demo Flow**:
1. Show homepage - clean UI
2. Upload **food waste** → See ORGANIC (green)
3. Upload **plastic bottle** → See RECYCLABLE (blue)
4. Upload **battery** → See HAZARDOUS (red)
5. Show awareness tips
6. Mention safety logic (low confidence → hazardous)

**Key Points to Highlight**:
- ✨ AI-powered (YOLOv8 + Gemini)
- 🛡️ Safety-first approach
- 🎨 Professional UI/UX
- ☁️ Azure-ready deployment
- 📚 Educational value (awareness tips)

---

## 📂 **PROJECT STRUCTURE**

```
Hackthon-garbage/
├── backend/
│   ├── app.py              # ⭐ Main FastAPI server
│   ├── utils.py            # Helper functions
│   ├── gemini_service.py   # Gemini AI integration
│   ├── model/best.pt       # YOLOv8 model
│   ├── requirements.txt    # Dependencies
│   └── .env               # Environment variables
│
├── frontend/
│   ├── index.html         # ⭐ Web interface
│   ├── style.css          # Beautiful styling
│   └── script.js          # Classification logic
│
├── README.md              # Full documentation
├── DEPLOYMENT.md          # Azure deployment guide
└── QUICKSTART.md          # ⭐ This file
```

---

## 🎯 **EVALUATION CRITERIA COVERAGE**

| Criteria | Status | Evidence |
|----------|--------|----------|
| Image upload | ✅ | Drag-drop + click upload |
| 3 categories | ✅ | ORGANIC, RECYCLABLE, HAZARDOUS |
| Awareness tips | ✅ | Gemini AI + fallbacks |
| Code quality | ✅ | Modular, documented, typed |
| Deployment ready | ✅ | See DEPLOYMENT.md |
| UI/UX | ✅ | Modern, responsive |
| Innovation | ✅ | Safety logic, Gemini integration |

**Target Score**: 80+ / 100 ⭐

---

## 🚀 **NEXT STEPS**

### **For Local Testing**
- ✅ Application is ready to use!
- 📸 Test with various waste images
- 🔑 Add Gemini key for smart tips (optional)

### **For Deployment**
- 📖 Read `DEPLOYMENT.md`
- 🔑 Get Gemini API key
- ☁️ Deploy to Azure
- 🌐 Share demo URL

### **For Presentation**
- 🎤 Practice demo flow
- 📊 Prepare test images
- 💡 Highlight innovation
- 🛡️ Emphasize safety logic

---

## ⚡ **ONE-LINE RESTART**

```bash
cd D:\Hackthon-garbage\backend && D:/Hackthon-garbage/.venv/Scripts/python.exe -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

---

## 🎉 **YOU'RE READY!**

**Current Status**: ✅ FULLY FUNCTIONAL

Open http://127.0.0.1:8000 and start classifying waste! 🗑️✨

For questions or issues, check:
- README.md (full guide)
- DEPLOYMENT.md (Azure deployment)
- Code comments (inline documentation)

**Good luck with the hackathon!** 🏆
