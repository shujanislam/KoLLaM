import uvicorn
import os
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from image_generator.generate_single_kolam import test_setup 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify list like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],   # Authorization, Content-Type, etc.
)

@app.get('/')
def main():
    return { "data": "json bhai" }

@app.post('/generate-kolam')
def generateKolam():
    output_path = test_setup(8)
    return FileResponse(output_path, media_type="image/png", filename="ayan.png")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
