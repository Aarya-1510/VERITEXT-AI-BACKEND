import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.text_extractor import extract_text
from app.services.plagiarism_checker import check_plagiarism


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


UPLOAD_DIR = "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


@router.post("/")
async def upload_document(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed."
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from the uploaded document
        text = extract_text(file_path)

        # Analyze the extracted text using Gemini
        plagiarism_result = check_plagiarism(text)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "text": text,
            "plagiarism_percentage": plagiarism_result.get(
                "plagiarism_percentage",
                0
            ),
            "results": plagiarism_result.get(
                "results",
                []
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )