import os
from huggingface_hub import InferenceClient
from PIL import Image
import uuid
from typing import Optional

class AIArtGenerator:
    def __init__(self):
        self.client = InferenceClient(
            api_key=os.environ.get("HF_TOKEN")
        )
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512
    ) -> tuple[str, str]:
        """
        Generate AI artwork and return image path and filename
        """
        try:
            # Generate image using HuggingFace
            image = self.client.text_to_image(
                prompt,
                model="black-forest-labs/FLUX.1-schnell",
                negative_prompt=negative_prompt,
                width=width,
                height=height
            )
            
            # Generate unique filename
            image_id = str(uuid.uuid4())
            filename = f"{image_id}.png"
            
            # Ensure directory exists
            os.makedirs("static/images", exist_ok=True)
            
            # Full path for saving
            full_path = os.path.join("static", "images", filename)
            
            # Save image
            image.save(full_path)
            
            return full_path, filename
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")

# Global instance
ai_generator = AIArtGenerator()