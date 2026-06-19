from fastapi import UploadFile, File
from backend.cv_parser import extract_text_from_pdf
import os
from fastapi import FastAPI

app = FastAPI(
    title="CareerPilot AI",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "CareerPilot AI is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "filename": file.filename,
        "status": "uploaded"
    }
