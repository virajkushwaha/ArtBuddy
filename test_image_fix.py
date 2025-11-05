import requests
import json

def test_image_generation():
    """Test the complete image generation flow"""
    
    print("Testing ArtBuddy image generation...")
    
    # Test 1: Health check
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Backend is running")
        else:
            print("✗ Backend not responding")
            return
    except:
        print("✗ Backend not running. Start with: python main.py")
        return
    
    # Test 2: Test image endpoint
    try:
        response = requests.get("http://localhost:8000/test-image")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Test image created: {data['full_url']}")
        else:
            print("✗ Test image creation failed")
    except Exception as e:
        print(f"✗ Test image error: {e}")
    
    # Test 3: Static file serving
    try:
        response = requests.get("http://localhost:8000/static/images/test_66876978.png")
        if response.status_code == 200:
            print("✓ Static file serving works")
        else:
            print("✗ Static file serving failed")
    except:
        print("✗ Static file serving error")

if __name__ == "__main__":
    test_image_generation()