# 🗑️ Waste Classification System - YOLOv8

AI-powered waste classification system using YOLOv8 for automated sorting of garbage into **BIODEGRADABLE**, **RECYCLABLE**, and **HAZARDOUS** categories.

## 📁 Project Structure

```
D:\Hackthone-garbage\
├── backend\
│   ├── app.py              # Flask API server
│   ├── utils.py            # Helper functions
│   ├── requirements.txt    # Python dependencies
│   └── model\
│       └── best.pt         # YOLOv8 trained model
├── frontend\               # Frontend files (to be added)
└── README.md              # This file
```

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Backend Framework**: Flask
- **AI Framework**: Ultralytics YOLOv8
- **Image Processing**: OpenCV, Pillow
- **Optional**: Gemini API for explanations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

Server will start at `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```http
GET /health
```

Returns server status and model loading state.

### Predict Waste Class
```http
POST /predict
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "class": "RECYCLABLE",
    "confidence": 0.9542,
    "dustbin_color": "BLUE",
    "awareness_tip": "🔵 Recyclable waste can be reprocessed..."
  }
}
```

### Get Available Classes
```http
GET /classes
```

Returns all waste classes and dustbin color mapping.

## 🎯 Waste Categories

| Class | Dustbin Color | Examples |
|-------|--------------|----------|
| 🌱 BIODEGRADABLE | 🟢 GREEN | Food scraps, leaves, paper |
| ♻️ RECYCLABLE | 🔵 BLUE | Plastic, glass, metal, cardboard |
| ⚠️ HAZARDOUS | 🔴 RED | Batteries, chemicals, e-waste |

## 🔒 Model Information

- **Model**: YOLOv8 (best.pt)
- **Purpose**: Inference only (no training)
- **Location**: `backend/model/best.pt`
- **Format**: PyTorch (.pt)

## 📝 Notes

- Model file has been safely moved from Downloads to production path
- No duplicate model files exist
- Ready for deployment

## 🤝 Contributing

This is a hackathon project. Feel free to extend functionality.

---

**Built with ❤️ for cleaner environment**
