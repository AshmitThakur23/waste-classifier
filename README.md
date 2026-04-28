# 🌍 SmartWaste AI

[![Python](https://img.shields.io/badge/Python-3.13-3776ab?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00ACC1?style=flat-square)](https://ultralytics.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-EA4335?style=flat-square&logo=google)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

> **AI-powered waste classification & real-time littering detection** | Powered by YOLOv8, Computer Vision & Generative AI

---

## 🎯 Two Powerful Modules

| 🗑️ **Module 1: Waste Classifier** | 📹 **Module 2: Littering Detector** |
|---|---|
| Upload photo → AI classifies waste | Real-time camera monitoring |
| 4 waste categories | Detects littering behavior |
| Dustbin color recommendations | 10-second grace period |
| AI-powered disposal tips | Auto-captures evidence |
| **Stack:** FastAPI + YOLOv8 + Gemini | **Stack:** OpenCV + 4 YOLOv8 Models |

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  🌐 SMARTWASTE AI SYSTEM FLOW                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐   ┌──────────────────────────────┐
│  📱 WASTE CLASSIFICATION     │   │  📹 LITTERING DETECTION      │
│  Module 1                    │   │  Module 2                    │
└──────────────┬───────────────┘   └──────────────┬───────────────┘
               │                                  │
        ┌──────▼──────┐                   ┌──────▼──────┐
        │ User Uploads│                   │ Webcam Feed │
        │ Waste Image │                   │   Stream    │
        └──────┬──────┘                   └──────┬──────┘
               │                                  │
        ┌──────▼──────────────────┐      ┌──────▼──────────────┐
        │ YOLOv8 Classification   │      │ Multi-Model Detect: │
        │ (4 Waste Categories)    │      │ 1. Person (98%)     │
        │ ✅ Recyclable (Blue)    │      │ 2. Hand (99.4%)     │
        │ 🌱 Organic (Green)      │      │ 3. Garbage (89.7%)  │
        │ ⚠️ Hazardous (Red)      │      │ 4. Dustbin (96.6%)  │
        │ ⬛ General (Black)      │      └──────┬──────────────┘
        └──────┬──────────────────┘             │
               │                          ┌──────▼──────────┐
        ┌──────▼──────────┐              │ Grace Period    │
        │ Gemini AI       │              │ Logic (10 sec)  │
        │ • Eco Tips      │              └──────┬──────────┘
        │ • Disposal Info │                     │
        │ • Fun Facts     │              ┌──────▼──────────┐
        └──────┬──────────┘              │ Evidence Saved  │
               │                        │ • Screenshot    │
        ┌──────▼──────────┐             │ • Video Clip    │
        │ DISPLAY RESULT  │             └──────────────────┘
        │ • Bin Color     │                    │
        │ • Category      │             ┌──────▼──────────┐
        │ • Tips          │             │ Flask Dashboard │
        │ • Confidence %  │             │ Port 5000       │
        └─────────────────┘             └──────────────────┘
         FastAPI Port 8000
```

---

## 📁 Project Structure

```
waste-classifier/
│
├─ 🎯 main.py                    # Littering Detection Entry Point
├─ 📦 requirements.txt           # All Dependencies
│
├─ 📂 backend/                   # Waste Classification API (Port 8000)
│  ├─ app.py                     # FastAPI Server
│  ├─ gemini_service.py          # Gemini AI Integration
│  └─ utils.py                   # Helper Functions
│
├─ 📂 frontend/                  # Web UI
│  ├─ index.html                 # Main Interface
│  ├─ script.js                  # Frontend Logic
│  └─ style.css                  # Styling
│
├─ 📂 detection/                 # Littering Detection Module
│  ├─ person_detection.py        # Person Detection (YOLOv8n)
│  ├─ hand_detection.py          # Hand Tracking (99.4% mAP50)
│  ├─ garbage_detection.py       # Garbage Detection (89.7% mAP50)
│  ├─ dustbin_detection.py       # Dustbin Detection (96.6% mAP50)
│  ├─ garbage_classification.py  # Waste Classification
│  ├─ logic/
│  │  └─ littering_decision.py   # Grace Period & Warning Logic
│  └─ utils/
│     ├─ evidence_manager.py     # Screenshot & Video Capture
│     └─ video_utils.py          # Video Processing
│
├─ 📂 dashboard/                 # Evidence Dashboard (Port 5000)
│  ├─ app.py                     # Flask Server
│  └─ templates/                 # Cyberpunk UI
│
├─ 📂 models/                    # YOLOv8 Model Weights
│  ├─ waste_classify.pt          # Waste Classification
│  ├─ hand_detect.pt             # Hand Detection
│  ├─ garbage_detect.pt          # Garbage Detection
│  ├─ dustbin_detect.pt          # Dustbin Detection
│  └─ person_detect.pt           # Person Detection (COCO)
│
├─ 📂 evidence/                  # Auto-Captured Evidence
│  ├─ images/                    # Screenshots
│  ├─ videos/                    # Recorded Evidence
│  └─ logs/                      # Event Logs
│
└─ 📂 training/                  # Model Training Scripts
   ├─ train.py
   ├─ train_v2.py
   └─ waste_data.yaml
```

---

## 🤖 Model Performance at a Glance

| Model | Task | Accuracy | Size | Status |
|-------|------|----------|------|--------|
| **Waste Classifier** | 4-Class Segregation | 53.6% mAP50 | 17.6 MB | ✅ |
| **Hand Detection** | Object Tracking | 99.4% mAP50 | 6.0 MB | ✅ |
| **Garbage Detection** | Garbage Objects | 89.7% mAP50 | 5.9 MB | ✅ |
| **Dustbin Detection** | Dustbin Location | 96.6% mAP50 | 6.0 MB | ✅ |
| **Person Detection** | YOLOv8n COCO | High | 6.3 MB | ✅ |

---

## 🎨 Waste Categories

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ ♻️ RECYCL.   │  │ 🌱 ORGANIC   │  │ ⚠️ HAZARD.   │  │ ⬛ GENERAL   │
├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤
│ BLUE BIN     │  │ GREEN BIN    │  │ RED BIN      │  │ BLACK BIN    │
├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤
│ • Bottles    │  │ • Food       │  │ • Batteries  │  │ • Mixed      │
│ • Paper      │  │ • Leaves     │  │ • Chemicals  │  │ • Non-Recycle│
│ • Cardboard  │  │ • Flowers    │  │ • Medical    │  │ • Other      │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🚀 Quick Start Guide

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Set Gemini API Key
```bash
# Create backend/.env
GEMINI_API_KEY=your_api_key_here
```

### 3️⃣ Run Waste Classification API
```bash
cd backend
uvicorn app:app --reload --port 8000
```
Open `frontend/index.html` in your browser

### 4️⃣ Run Littering Detection
```bash
python main.py
```
Controls: `q` = quit | `r` = reset

### 5️⃣ View Dashboard
```bash
cd dashboard
python app.py
```
Open http://localhost:5000

---

## 💡 Tech Stack Overview

```
🎨 Frontend       → HTML5 | CSS3 | JavaScript
🔧 Backend        → FastAPI | Flask  
🤖 AI/ML          → YOLOv8 | PyTorch | OpenCV
🧠 Generative AI  → Google Gemini 1.5 Flash
💻 Language       → Python 3.13
🖥️ Hardware       → NVIDIA RTX 3050 (4GB VRAM)
```

---

## 📈 Code Composition

| Language | Percentage |
|----------|-----------|
| Python | 51.9% |
| HTML | 37.3% |
| CSS | 5.7% |
| JavaScript | 5.1% |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for a cleaner planet**

⭐ Star this repo if you found it helpful!

</div>