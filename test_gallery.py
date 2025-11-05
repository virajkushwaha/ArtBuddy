import requests
import json

def test_gallery():
    """Test gallery functionality"""
    
    print("Testing gallery endpoints...")
    
    # Test gallery endpoint
    try:
        response = requests.get("http://localhost:8001/gallery")
        if response.status_code == 200:
            data = response.json()
            print(f"Gallery loaded: {len(data.get('images', []))} images found")
            for img in data.get('images', [])[:3]:  # Show first 3
                print(f"  - {img['filename']}")
        else:
            print("Gallery endpoint failed")
    except Exception as e:
        print(f"Gallery test error: {e}")
    
    # Test image generation and gallery update
    try:
        print("\nGenerating test image...")
        response = requests.post("http://localhost:8001/generate", 
            json={"prompt": "a cute robot painting", "width": 512, "height": 512})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"Image generated: {data['image_url']}")
                
                # Check gallery again
                gallery_response = requests.get("http://localhost:8001/gallery")
                if gallery_response.status_code == 200:
                    gallery_data = gallery_response.json()
                    print(f"Gallery now has: {len(gallery_data.get('images', []))} images")
            else:
                print(f"Generation failed: {data.get('error')}")
        else:
            print("Generation request failed")
    except Exception as e:
        print(f"Generation test error: {e}")

if __name__ == "__main__":
    test_gallery()