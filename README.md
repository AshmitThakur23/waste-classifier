# SmartWaste AI

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)](https://flask.palletsprojects.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple.svg)](https://ultralytics.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A combined AI platform for waste classification + real-time littering detection using Computer Vision, YOLOv8, and Generative AI.**

---

## What It Does

**Two modules, one mission** â€” reduce waste mismanagement using AI:

### Module 1: Waste Classification (Web App)
- Upload a photo of waste â†’ AI classifies it into 4 categories
- Shows the correct dustbin color for disposal
- Generates awareness tips using Gemini AI
- **Stack:** FastAPI + YOLOv8 + Gemini 1.5 Flash

### Module 2: Littering Detection (Camera System)
- Real-time camera monitoring for littering behavior
- Detects person â†’ tracks hands â†’ detects garbage â†’ monitors if dropped
- 10-second grace period to pick up before flagging
- Auto-captures evidence (screenshot + video) on confirmed littering
- **Stack:** OpenCV + 4 custom YOLOv8 models + Evidence Manager

---

## Project Structure

```
SmartWaste-AI/
â”œâ”€â”€ main.py                    # Littering detection entry point (camera)
â”œâ”€â”€ requirements.txt           # All dependencies
â”‚
â”œâ”€â”€ backend/                   # Module 1: Waste Classification API
â”‚   â”œâ”€â”€ app.py                 # FastAPI server (port 8000)
â”‚   â”œâ”€â”€ gemini_service.py      # Gemini AI text tips
â”‚   â”œâ”€â”€ utils.py               # Dustbin colors, helpers
â”‚
â”œâ”€â”€ frontend/                  # Waste Classification Web UI
â”‚   â”œâ”€â”€ index.html
â”‚   â”œâ”€â”€ script.js
â”‚   â””â”€â”€ style.css
â”‚
â”œâ”€â”€ detection/                 # Module 2: Littering Detection
â”‚   â”œâ”€â”€ hand_detection.py      # Hand tracking (99.4% mAP50)
â”‚   â”œâ”€â”€ garbage_detection.py   # Garbage detection (89.7% mAP50)
â”‚   â”œâ”€â”€ dustbin_detection.py   # Dustbin detection (96.6% mAP50)
â”‚   â”œâ”€â”€ garbage_classification.py
â”‚   â”œâ”€â”€ person_detection.py    # YOLOv8n person detection
â”‚   â”œâ”€â”€ logic/
â”‚   â”‚   â””â”€â”€ littering_decision.py  # Grace period + warning logic
â”‚   â””â”€â”€ utils/
â”‚       â”œâ”€â”€ evidence_manager.py    # Screenshot + video capture
â”‚       â””â”€â”€ video_utils.py
â”‚
â”œâ”€â”€ dashboard/                 # Littering Dashboard (Flask)
â”‚   â”œâ”€â”€ app.py                 # Flask server (port 5000)
â”‚   â””â”€â”€ templates/             # Cyberpunk dashboard UI
â”‚
â”œâ”€â”€ models/                    # All YOLOv8 model weights
â”‚   â”œâ”€â”€ waste_classify.pt    # Waste classification (4 classes)
â”‚   â”œâ”€â”€ hand_detect.pt         # Hand detection
â”‚   â”œâ”€â”€ garbage_detect.pt      # Garbage detection
â”‚   â”œâ”€â”€ dustbin_detect.pt      # Dustbin detection
â”‚   â””â”€â”€ person_detect.pt       # Person detection
â”‚
â”œâ”€â”€ evidence/                  # Auto-captured littering evidence
â”‚   â”œâ”€â”€ images/
â”‚   â”œâ”€â”€ videos/
â”‚   â””â”€â”€ logs/
â”‚
â””â”€â”€ training/                  # Training scripts + dataset config
    â”œâ”€â”€ train.py
    â”œâ”€â”€ train_v2.py
    â””â”€â”€ waste_data.yaml
```

---

## Trained Models

| Model | Purpose | mAP50 | Size |
|-------|---------|-------|------|
| Waste Classifier | 4-class segregation (Recyclable, Organic, Hazardous, General) | 53.6% | 17.6 MB |
| Hand Detection | Track objects in hands | 99.4% | 6.0 MB |
| Garbage Detection | Detect garbage objects (Bottle, Cup, Plastic, etc.) | 89.7% | 5.9 MB |
| Dustbin Detection | Locate dustbins in frame | 96.6% | 6.0 MB |
| Person Detection | YOLOv8n COCO pretrained | - | 6.3 MB |

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API (for waste classification tips)
```bash
# Create backend/.env
GEMINI_API_KEY=your_key_here
```

### 3. Run Waste Classification API
```bash
cd backend
uvicorn app:app --reload --port 8000
```
Then open `frontend/index.html` in a browser.

### 4. Run Littering Detection
```bash
python main.py
```
Controls: `q` = quit, `r` = reset

### 5. Run Littering Dashboard
```bash
cd dashboard
python app.py
```
Opens at http://localhost:5000

---

## Waste Categories

| Category | Dustbin Color | Examples |
|----------|--------------|----------|
| Recyclable | Blue | Plastic bottles, paper, cardboard |
| Organic | Green | Food waste, leaves, flowers |
| Hazardous | Red | Batteries, chemicals, medical waste |
| General | Black | Mixed waste, non-recyclable items |

---

## Tech Stack

- **AI/ML:** YOLOv8n (Ultralytics), PyTorch, OpenCV
- **Backend:** FastAPI (classification), Flask (dashboard)
- **Frontend:** HTML/CSS/JS
- **AI Tips:** Google Gemini 1.5 Flash (text generation only)
- **GPU:** Trained on NVIDIA RTX 3050 (4GB VRAM)

