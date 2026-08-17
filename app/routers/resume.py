from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import extract_text

router = APIRouter()

ALLOWED_TYPES = {".pdf", ".docx"}

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    content = await file.read()
    text = extract_text(content, ext)

    return {
        "filename": file.filename,
        "extracted_length": len(text),
        "preview": text[:500]
    }