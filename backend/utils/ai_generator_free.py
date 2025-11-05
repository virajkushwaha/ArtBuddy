import os
import requests
import uuid
from PIL import Image
from io import BytesIO
from typing import Optional

class FreeAIArtGenerator:
    """Alternative AI generator using free APIs"""
    
    def __init__(self):
        self.hf_token = os.environ.get("HF_TOKEN")
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512
    ) -> tuple[str, str]:
        """Generate AI artwork using free Hugging Face models"""
        
        try:
            # Use free Stable Diffusion model
            api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": negative_prompt or "",
                    "guidance_scale": guidance_scale,
                    "width": width,
                    "height": height
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")
            
            # Convert response to image
            image = Image.open(BytesIO(response.content))
            
            # Generate unique filename
            image_id = str(uuid.uuid4())
            filename = f"{image_id}.png"
            image_path = f"static/images/{filename}"
            
            # Ensure directory exists
            os.makedirs("static/images", exist_ok=True)
            
            # Save image
            image.save(image_path)
            
            return image_path, filename
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")

# Global instance
free_ai_generator = FreeAIArtGenerator()