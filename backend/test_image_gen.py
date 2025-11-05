from PIL import Image, ImageDraw
import os
import uuid

def create_test_image():
    """Create a test image to verify static serving works"""
    
    # Ensure directory exists
    os.makedirs("static/images", exist_ok=True)
    
    # Create a simple test image
    img = Image.new('RGB', (512, 512), color='#4CAF50')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    draw.text((50, 250), "TEST IMAGE - Static serving works!", fill='white')
    
    # Save with unique filename
    filename = f"test_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join("static", "images", filename)
    img.save(filepath)
    
    print(f"Test image created: {filepath}")
    print(f"URL should be: http://localhost:8000/static/images/{filename}")
    
    return filename

if __name__ == "__main__":
    create_test_image()