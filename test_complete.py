import requests
import json
import time

def test_complete_flow():
    """Test the complete image generation and display flow"""
    
    print("Testing complete ArtBuddy flow...")
    
    # Test 1: Backend health
    try:
        response = requests.get("http://localhost:8001/test", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is running")
        else:
            print("✗ Backend not responding")
            return False
    except:
        print("✗ Backend not running. Start with: python backend/flask_app.py")
        return False
    
    # Test 2: Generate image
    try:
        print("Generating test image...")
        response = requests.post("http://localhost:8001/generate", 
            json={"prompt": "a cute robot", "width": 512, "height": 512},
            timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ Image generated: {data['image_url']}")
                
                # Test 3: Check if image is accessible
                image_response = requests.get(data['full_url'], timeout=10)
                if image_response.status_code == 200:
                    print("✓ Image is accessible via URL")
                    print(f"✓ Image size: {len(image_response.content)} bytes")
                    return True
                else:
                    print("✗ Image URL not accessible")
            else:
                print(f"✗ Generation failed: {data.get('error')}")
        else:
            print("✗ Generation request failed")
    except Exception as e:
        print(f"✗ Generation error: {e}")
    
    return False

if __name__ == "__main__":
    success = test_complete_flow()
    if success:
        print("\n🎉 All tests passed! Your ArtBuddy is working!")
        print("Frontend should now display images properly.")
    else:
        print("\n❌ Tests failed. Check backend is running.")