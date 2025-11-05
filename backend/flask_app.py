from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import base64
import asyncio
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from utils.simple_generator import generate_image_simple

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app, origins=["http://localhost:3000"])

# Create images directory
os.makedirs('static/images', exist_ok=True)

def create_sample_image(prompt, width=512, height=512):
    """Create a sample image with the prompt text"""
    # Create a colorful gradient background
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for y in range(height):
        r = int(26 + (y / height) * 100)
        g = int(26 + (y / height) * 50)
        b = int(46 + (y / height) * 150)
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add some decorative elements
    for i in range(20):
        x = (i * width // 20) + (width // 40)
        y = height // 2 + int(50 * (i % 3 - 1))
        draw.ellipse([x-10, y-10, x+10, y+10], fill=(255, 255, 255, 100))
    
    # Add prompt text
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Wrap text
    words = prompt.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 40:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw text
    y_offset = height // 2 - (len(lines) * 15)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset), line, fill='white', font=font)
        y_offset += 30
    
    return img

@app.route('/')
def home():
    return jsonify({"message": "ArtBuddy API is running", "status": "ok"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "ArtBuddy API"})

@app.route('/test')
def test():
    return jsonify({"test": "success", "python_version": "3.14", "message": "Backend is working!"})

@app.route('/generate', methods=['POST'])
def generate_art():
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'Abstract art')
        width = data.get('width', 512)
        height = data.get('height', 512)
        negative_prompt = data.get('negative_prompt', None)
        
        # Generate image
        filepath, filename = generate_image_simple(
            prompt=prompt,
            width=width,
            height=height
        )
        
        # Store in simple database (JSON file)
        import json
        from datetime import datetime
        
        gallery_file = 'gallery.json'
        gallery_data = []
        
        # Load existing gallery
        try:
            with open(gallery_file, 'r') as f:
                gallery_data = json.load(f)
        except:
            gallery_data = []
        
        # Add new image
        new_image = {
            'filename': filename,
            'prompt': prompt,
            'url': f"/static/images/{filename}",
            'full_url': f"http://localhost:8001/static/images/{filename}",
            'created_at': datetime.now().isoformat()
        }
        gallery_data.append(new_image)
        
        # Save gallery
        with open(gallery_file, 'w') as f:
            json.dump(gallery_data, f)
        
        return jsonify({
            "success": True,
            "image_url": f"/static/images/{filename}",
            "full_url": f"http://localhost:8001/static/images/{filename}",
            "prompt": prompt,
            "message": "Artwork generated successfully!"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), filename)

@app.route('/gallery')
def get_gallery():
    try:
        import json
        
        gallery_file = 'gallery.json'
        
        # Load gallery from JSON
        try:
            with open(gallery_file, 'r') as f:
                gallery_data = json.load(f)
        except:
            gallery_data = []
        
        # Sort by newest first
        gallery_data.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({'images': gallery_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_image(filename):
    try:
        return send_from_directory('static/images', filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)