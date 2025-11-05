from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/')
def home():
    return jsonify({"message": "ArtBuddy API working"})

@app.route('/test')
def test():
    return jsonify({"test": "success", "message": "Backend working!"})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'test image')
        
        # Create simple SVG image
        svg = f'''<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#667eea"/>
                    <stop offset="100%" stop-color="#764ba2"/>
                </linearGradient>
            </defs>
            <rect width="512" height="512" fill="url(#grad)"/>
            <text x="256" y="200" font-family="Arial" font-size="20" fill="white" text-anchor="middle">Generated Art</text>
            <text x="256" y="250" font-family="Arial" font-size="16" fill="white" text-anchor="middle">{prompt[:50]}</text>
            <circle cx="256" cy="350" r="50" fill="rgba(255,255,255,0.3)"/>
        </svg>'''
        
        import base64
        svg_b64 = base64.b64encode(svg.encode()).decode()
        
        return jsonify({
            "success": True,
            "image_url": f"data:image/svg+xml;base64,{svg_b64}",
            "prompt": prompt,
            "message": "Image generated successfully!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask on http://localhost:8001")
    print("Test: http://localhost:8001/test")
    app.run(host='0.0.0.0', port=8001, debug=True)