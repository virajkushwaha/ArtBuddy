import requests
import json
import uuid
import os
from PIL import Image
from io import BytesIO
import base64
from typing import Optional

class GeminiImageGenerator:
    def __init__(self):
        # Using your existing API key from HealthBuddy
        self.api_key = "GEMINI_API_KEY"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512
    ) -> tuple[str, str]:
        """Generate image using Imagen 3 via Gemini API"""
        
        try:
            # Use Imagen 3 model for actual image generation
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:generateImage?key={self.api_key}"
            
            payload = {
                "prompt": prompt,
                "config": {
                    "aspectRatio": "1:1",
                    "safetyFilterLevel": "BLOCK_ONLY_HIGH",
                    "personGeneration": "ALLOW_ADULT"
                }
            }
            
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract base64 image data
                if 'generatedImages' in result and len(result['generatedImages']) > 0:
                    image_data = result['generatedImages'][0]['bytesBase64Encoded']
                    
                    # Decode and save image
                    image_bytes = base64.b64decode(image_data)
                    img = Image.open(BytesIO(image_bytes))
                    
                    # Generate filename and save
                    image_id = str(uuid.uuid4())
                    filename = f"imagen_{image_id}.png"
                    
                    os.makedirs("static/images", exist_ok=True)
                    full_path = os.path.join("static", "images", filename)
                    
                    img.save(full_path)
                    return full_path, filename
            
            # If Imagen fails, try alternative approach
            return await self._try_alternative_generation(prompt, width, height)
            
        except Exception as e:
            print(f"Imagen API error: {e}")
            return await self._try_alternative_generation(prompt, width, height)
    
    async def _try_alternative_generation(self, prompt: str, width: int, height: int) -> tuple[str, str]:
        """Try alternative image generation methods"""
        try:
            # Try using Pollinations API (free)
            return await self._generate_with_pollinations(prompt, width, height)
        except:
            # Final fallback to enhanced sample
            return self._create_enhanced_sample(prompt, width, height)
    
    async def _generate_with_pollinations(self, prompt: str, width: int, height: int) -> tuple[str, str]:
        """Generate image using Pollinations API"""
        import urllib.parse
        
        # Encode prompt for URL
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Force PNG format and add seed for consistency
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&enhance=true&format=png&seed={hash(prompt) % 1000000}"
        
        response = requests.get(api_url, timeout=30, headers={'Accept': 'image/png'})
        
        if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
            # Convert to PNG if needed
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if RGBA
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            image_id = str(uuid.uuid4())
            filename = f"ai_{image_id}.png"
            
            os.makedirs("static/images", exist_ok=True)
            full_path = os.path.join("static", "images", filename)
            
            img.save(full_path, 'PNG')
            return full_path, filename
        
        raise Exception("Failed to get valid image")
    
    def _create_enhanced_sample(self, prompt: str, width: int, height: int) -> tuple[str, str]:
        """Create a sample image with Gemini branding"""
        from PIL import ImageDraw, ImageFont
        
        # Create gradient background
        img = Image.new('RGB', (width, height), color='#4285f4')
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for y in range(height):
            r = int(66 + (y / height) * 100)
            g = int(133 + (y / height) * 50) 
            b = int(244 - (y / height) * 50)
            color = (r, g, b)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Add decorative elements
        for i in range(15):
            x = (i * width // 15) + (width // 30)
            y = height // 2 + int(30 * ((i % 3) - 1))
            draw.ellipse([x-8, y-8, x+8, y+8], fill=(255, 255, 255, 120))
        
        # Add text
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Wrap prompt text
        words = prompt.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 35:
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
        y_offset = height // 2 - (len(lines) * 12)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_offset), line, fill='white', font=font)
            y_offset += 25
        
        # Add "AI Generated" text
        ai_text = "AI Generated Art"
        bbox = draw.textbbox((0, 0), ai_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, height - 30), ai_text, fill=(255, 255, 255), font=font)
        
        # Save image
        image_id = str(uuid.uuid4())
        filename = f"sample_{image_id}.png"
        
        # Ensure directory exists
        os.makedirs("static/images", exist_ok=True)
        
        # Full path for saving
        full_path = os.path.join("static", "images", filename)
        img.save(full_path, 'PNG')
        
        return full_path, filename

# Global instance
gemini_generator = GeminiImageGenerator()
