#!/usr/bin/env python3
"""
ArtBuddy Setup Test Script
Tests basic functionality and dependencies
"""

import sys
import os
import subprocess

def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_dependencies():
    """Test if required packages can be imported"""
    print("\nTesting Python dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'huggingface_hub',
        'PIL',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'dotenv':
                import dotenv
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def test_environment():
    """Test environment configuration"""
    print("\nTesting environment setup...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        # Check for required environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        hf_token = os.getenv('HF_TOKEN')
        if hf_token and hf_token != 'your_huggingface_token_here':
            print("✅ HF_TOKEN is configured")
        else:
            print("⚠️  HF_TOKEN not configured - Add your HuggingFace token to .env")
            
        secret_key = os.getenv('SECRET_KEY')
        if secret_key and secret_key != 'your-super-secret-jwt-key-change-in-production':
            print("✅ SECRET_KEY is configured")
        else:
            print("⚠️  SECRET_KEY using default - Change for production")
            
    else:
        print("⚠️  .env file not found - Copy from .env.example")

def test_directories():
    """Test required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = [
        'backend',
        'frontend',
        'static',
        'static/images',
        'backend/models',
        'backend/routes',
        'backend/utils'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - Missing")
            os.makedirs(directory, exist_ok=True)
            print(f"   Created {directory}")

def main():
    """Run all tests"""
    print("🎨 ArtBuddy Setup Test\n" + "="*50)
    
    # Test Python version
    python_ok = test_python_version()
    
    # Test dependencies
    deps_ok, missing = test_dependencies()
    
    # Test environment
    test_environment()
    
    # Test directories
    test_directories()
    
    print("\n" + "="*50)
    
    if python_ok and deps_ok:
        print("🎉 Setup test completed successfully!")
        print("\nNext steps:")
        print("1. Configure your HuggingFace token in .env")
        print("2. Run: .\\start-artbuddy.ps1")
        print("3. Visit: http://localhost:3000")
    else:
        print("❌ Setup issues found!")
        if not python_ok:
            print("- Upgrade Python to 3.8+")
        if not deps_ok:
            print(f"- Install missing packages: pip install {' '.join(missing)}")

if __name__ == "__main__":
    main()