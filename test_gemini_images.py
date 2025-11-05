import asyncio
import sys
import os
sys.path.append('backend')

from backend.utils.gemini_generator import gemini_generator

async def test_gemini_generation():
    """Test Gemini image generation"""
    
    print("Testing Gemini AI image generation...")
    
    try:
        # Test image generation
        prompt = "A beautiful sunset over mountains with vibrant colors"
        
        print(f"Generating image for: {prompt}")
        
        filepath, filename = await gemini_generator.generate_image(
            prompt=prompt,
            width=512,
            height=512
        )
        
        print(f"Image generated successfully!")
        print(f"  File: {filepath}")
        print(f"  Filename: {filename}")
        print(f"  URL: http://localhost:8001/static/images/{filename}")
        
        # Check if file exists
        if os.path.exists(filepath):
            print("Image file exists on disk")
        else:
            print("Image file not found")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini_generation())
    
    if success:
        print("\nGemini image generation is working!")
        print("Now start the Flask backend: python backend/flask_app.py")
    else:
        print("\nGemini image generation failed")