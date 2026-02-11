"""
Vercel Serverless Function - Waste Classification API
Uses native Python HTTP handler for maximum compatibility
"""
from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/health' or self.path == '/api/health':
            response = {
                "status": "healthy",
                "platform": "Vercel",
                "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))
            }
        elif self.path == '/api/categories':
            response = {
                "categories": {
                    "ORGANIC": {"color": "green", "icon": "leaf"},
                    "RECYCLABLE": {"color": "blue", "icon": "recycle"},
                    "HAZARDOUS": {"color": "red", "icon": "warning"},
                    "GENERAL": {"color": "grey", "icon": "trash"}
                }
            }
        else:
            response = {
                "message": "Waste Classification API",
                "version": "1.0.0",
                "endpoints": ["/health", "/api/classify", "/api/categories"]
            }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if '/classify' in self.path:
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                result = self._classify_image(post_data)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e), "success": False}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _classify_image(self, raw_data):
        """Classify waste image using Gemini Vision AI"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "GEMINI_API_KEY not configured",
                "category": "GENERAL",
                "dustbin_color": "grey",
                "dustbin_icon": "trash"
            }
        
        try:
            import google.generativeai as genai
            from PIL import Image
            import io
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Extract image from multipart form data
            image_bytes = self._extract_image(raw_data)
            if not image_bytes:
                return {
                    "success": False,
                    "error": "No image found in request",
                    "category": "GENERAL",
                    "dustbin_color": "grey",
                    "dustbin_icon": "trash"
                }
            
            image = Image.open(io.BytesIO(image_bytes))
            
            prompt = """Analyze this image and classify the waste into ONE category:
            - ORGANIC (food, garden waste, biodegradable)
            - RECYCLABLE (plastic bottles, glass, metal, cardboard, paper)
            - HAZARDOUS (batteries, chemicals, electronics, bulbs)
            - GENERAL (chip packets, tissues, styrofoam, mixed waste)
            
            Reply with ONLY the category name."""
            
            response = model.generate_content([prompt, image])
            text = response.text.strip().upper()
            
            category = "GENERAL"
            for cat in ["HAZARDOUS", "ORGANIC", "RECYCLABLE", "GENERAL"]:
                if cat in text:
                    category = cat
                    break
            
            colors = {"ORGANIC": "green", "RECYCLABLE": "blue", "HAZARDOUS": "red", "GENERAL": "grey"}
            icons = {"ORGANIC": "leaf", "RECYCLABLE": "recycle", "HAZARDOUS": "warning", "GENERAL": "trash"}
            
            return {
                "success": True,
                "category": category,
                "confidence": 0.85,
                "dustbin_color": colors[category],
                "dustbin_icon": icons[category],
                "model_used": "Gemini Vision AI"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "category": "GENERAL",
                "dustbin_color": "grey",
                "dustbin_icon": "trash"
            }
    
    def _extract_image(self, raw_data):
        """Extract image bytes from multipart form data"""
        content_type = self.headers.get('Content-Type', '')
        
        if 'boundary=' in content_type:
            boundary = content_type.split('boundary=')[1].strip()
            parts = raw_data.split(f'--{boundary}'.encode())
            
            for part in parts:
                if b'filename=' in part or b'image' in part.lower():
                    if b'\r\n\r\n' in part:
                        image_bytes = part.split(b'\r\n\r\n', 1)[1]
                        if image_bytes.endswith(b'\r\n'):
                            image_bytes = image_bytes[:-2]
                        if image_bytes.endswith(b'--'):
                            image_bytes = image_bytes[:-2]
                        return image_bytes
        
        return raw_data if raw_data else None
