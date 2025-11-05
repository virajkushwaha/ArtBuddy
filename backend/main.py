from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.database import create_tables
from routes import auth, artworks
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify HF_TOKEN is set
if not os.getenv("HF_TOKEN"):
    raise ValueError("HF_TOKEN environment variable is required")

app = FastAPI(
    title="ArtBuddy API",
    description="Modern AI Art Generator & Gallery",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files - ensure directory exists first
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(artworks.router)

@app.on_event("startup")
async def startup_event():
    create_tables()
    # Create static directories
    os.makedirs("static/images", exist_ok=True)
    os.makedirs("static/uploads", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to ArtBuddy - AI Art Generator & Gallery"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ArtBuddy API"}

@app.get("/test-image")
async def test_image():
    """Test endpoint to create and return a sample image"""
    from PIL import Image, ImageDraw
    import uuid
    
    # Create test image
    img = Image.new('RGB', (512, 512), color='#2196F3')
    draw = ImageDraw.Draw(img)
    draw.text((50, 250), "Backend Image Test - SUCCESS!", fill='white')
    
    # Save image
    filename = f"test_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join("static", "images", filename)
    img.save(filepath)
    
    return {
        "success": True,
        "image_url": f"/static/images/{filename}",
        "full_url": f"http://localhost:8000/static/images/{filename}",
        "message": "Test image created successfully"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)