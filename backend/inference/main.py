import uvicorn
import os
import sys
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Add the image_generator directory to Python path
image_generator_path = os.path.join(os.path.dirname(__file__), "image_generator")
sys.path.insert(0, image_generator_path)

# Import test_setup
try:
    from generate_single_kolam import test_setup
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

app = FastAPI(title="Kolam Generator API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Kolam Generator API is running"}

@app.post("/generate-kolam")
async def generate_kolam(request: Request):
    """
    Receive JSON body like: { "size": 8 }
    Call the main test_setup function and return generated PNG
    """
    try:
        data = await request.json()
        size = data.get("size", 8)
        if not isinstance(size, int) or size < 2 or size > 50:
            raise HTTPException(status_code=400, detail="Size must be an integer between 2 and 50")

        print(f"Generating kolam with size={size}...")

        # Call test_setup directly
        output_path = test_setup(size)

        if not output_path or not os.path.isfile(output_path):
            raise HTTPException(status_code=500, detail="Kolam generation failed")

        return FileResponse(
            output_path,
            media_type="image/png",
            filename="kolam.png",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache"
            }
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
