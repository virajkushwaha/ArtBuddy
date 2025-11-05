#!/usr/bin/env python3
"""Simple backend test"""

try:
    from fastapi import FastAPI
    from models.database import create_tables
    print("✅ FastAPI imports successful")
    
    # Test database creation
    create_tables()
    print("✅ Database tables created")
    
    print("🎉 Backend test passed!")
    
except Exception as e:
    print(f"❌ Backend test failed: {e}")
    import traceback
    traceback.print_exc()