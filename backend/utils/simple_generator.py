import requests
import uuid
import os
from PIL import Image
from io import BytesIO

def generate_image_simple(prompt, width=512, height=512):
    """Generate real AI image using multiple APIs"""
    
    # Try multiple working APIs in order
    apis = [
        # API 1: Pollinations (most reliable)
        lambda: try_pollinations(prompt, width, height),
        # API 2: Replicate via web
        lambda: try_replicate_web(prompt, width, height),
        # API 3: Segmind API
        lambda: try_segmind(prompt, width, height)
    ]
    
    for api_func in apis:
        try:
            result = api_func()
            if result:
                return result
        except Exception as e:
            print(f"API failed: {e}")
            continue
    
    # Only use fallback if all APIs fail
    print("All APIs failed, using fallback")
    return create_fallback_image(prompt, width, height)

def try_pollinations(prompt, width, height):
    """Try Pollinations API - most reliable"""
    import urllib.parse
    
    encoded_prompt = urllib.parse.quote(prompt)
    api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&enhance=true&nologo=true"
    
    response = requests.get(api_url, timeout=30)
    
    if response.status_code == 200 and len(response.content) > 1000:
        # Check if it's actually an image
        try:
            image = Image.open(BytesIO(response.content))
            
            # Generate filename
            image_id = str(uuid.uuid4())[:8]
            filename = f"ai_{image_id}.png"
            
            os.makedirs("static/images", exist_ok=True)
            filepath = os.path.join("static", "images", filename)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image.save(filepath, "PNG")
            return filepath, filename
        except:
            pass
    
    return None

def try_replicate_web(prompt, width, height):
    """Try web-based Replicate API"""
    try:
        # Use a simple web API that doesn't require auth
        api_url = "https://api.deepai.org/api/text2img"
        
        data = {'text': prompt}
        
        response = requests.post(api_url, data=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if 'output_url' in result:
                # Download the generated image
                img_response = requests.get(result['output_url'], timeout=30)
                if img_response.status_code == 200:
                    image = Image.open(BytesIO(img_response.content))
                    
                    # Resize to requested size
                    image = image.resize((width, height), Image.Resampling.LANCZOS)
                    
                    image_id = str(uuid.uuid4())[:8]
                    filename = f"ai_{image_id}.png"
                    
                    os.makedirs("static/images", exist_ok=True)
                    filepath = os.path.join("static", "images", filename)
                    
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    image.save(filepath, "PNG")
                    return filepath, filename
    except:
        pass
    
    return None

def try_segmind(prompt, width, height):
    """Try Segmind API"""
    try:
        api_url = "https://api.segmind.com/v1/sd1.5-txt2img"
        
        data = {
            "prompt": prompt,
            "negative_prompt": "blurry, bad quality",
            "samples": 1,
            "width": width,
            "height": height,
            "steps": 20,
            "guidance_scale": 7.5
        }
        
        response = requests.post(api_url, json=data, timeout=60)
        
        if response.status_code == 200 and len(response.content) > 1000:
            image = Image.open(BytesIO(response.content))
            
            image_id = str(uuid.uuid4())[:8]
            filename = f"ai_{image_id}.png"
            
            os.makedirs("static/images", exist_ok=True)
            filepath = os.path.join("static", "images", filename)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image.save(filepath, "PNG")
            return filepath, filename
    except:
        pass
    
    return None

def create_fallback_image(prompt, width, height):
    """Create a visually appealing fallback image"""
    from PIL import ImageDraw, ImageFont
    import hashlib
    
    # Create hash-based colors from prompt
    hash_obj = hashlib.md5(prompt.encode())
    hash_hex = hash_obj.hexdigest()
    
    # Extract colors from hash
    r1 = int(hash_hex[0:2], 16)
    g1 = int(hash_hex[2:4], 16) 
    b1 = int(hash_hex[4:6], 16)
    r2 = int(hash_hex[6:8], 16)
    g2 = int(hash_hex[8:10], 16)
    b2 = int(hash_hex[10:12], 16)
    
    # Create gradient
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    for y in range(height):
        ratio = y / height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add abstract shapes based on prompt
    for i in range(len(prompt) % 10 + 5):
        x = (hash(prompt + str(i)) % width)
        y = (hash(prompt + str(i*2)) % height)
        size = 20 + (hash(prompt + str(i*3)) % 40)
        
        # Random shape color
        shape_r = (r1 + i * 30) % 255
        shape_g = (g1 + i * 40) % 255  
        shape_b = (b1 + i * 50) % 255
        
        draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                    fill=(shape_r, shape_g, shape_b, 100))
    
    # Add prompt text
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Wrap text
    words = prompt.split()[:6]  # First 6 words
    text = ' '.join(words)
    
    # Draw text with outline
    text_x = width // 2 - len(text) * 3
    text_y = height // 2
    
    # Text outline
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((text_x + dx, text_y + dy), text, fill=(0, 0, 0), font=font)
    
    # Main text
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    # Save
    image_id = str(uuid.uuid4())[:8]
    filename = f"art_{image_id}.png"
    
    os.makedirs("static/images", exist_ok=True)
    filepath = os.path.join("static", "images", filename)
    img.save(filepath, "PNG")
    
    return filepath, filename