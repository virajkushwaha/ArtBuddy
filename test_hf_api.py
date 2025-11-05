import os
import asyncio
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

async def test_huggingface_api():
    """Test Hugging Face API connection and image generation"""
    
    # Check if API key is set
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token or hf_token == "your_huggingface_token_here":
        print("ERROR: HF_TOKEN not set or using placeholder value")
        print("Please set your actual Hugging Face token in .env file")
        return False
    
    print(f"HF_TOKEN found: {hf_token[:10]}...")
    
    try:
        # Test 1: Basic client initialization
        print("\nTesting client initialization...")
        client = InferenceClient(api_key=hf_token)
        print("Client initialized successfully")
        
        # Test 2: Simple text-to-image generation
        print("\nTesting image generation...")
        prompt = "a simple red apple on white background"
        
        # Try with a reliable model
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell"  # Fast, reliable model
        )
        
        # Save test image
        os.makedirs("test_output", exist_ok=True)
        test_path = "test_output/test_image.png"
        image.save(test_path)
        
        print(f"Image generated successfully and saved to: {test_path}")
        print(f"Image size: {image.size}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        
        # Common error suggestions
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("\nSuggestion: Check if your HF_TOKEN is valid")
            print("   - Go to https://huggingface.co/settings/tokens")
            print("   - Create a new token with 'Read' permissions")
            print("   - Update your .env file")
        elif "quota" in str(e).lower() or "rate limit" in str(e).lower():
            print("\nSuggestion: You may have hit rate limits")
            print("   - Wait a few minutes and try again")
            print("   - Consider upgrading your HF account")
        elif "model" in str(e).lower():
            print("\nSuggestion: Model may not be available")
            print("   - Try a different model")
        
        return False

if __name__ == "__main__":
    print("Testing Hugging Face API...")
    success = asyncio.run(test_huggingface_api())
    
    if success:
        print("\nAll tests passed! Your Hugging Face API is working correctly.")
    else:
        print("\nTests failed. Please check the errors above.")