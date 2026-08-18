from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.parser import extract_text
from app.services.scorer import keyword_score, ROLE_PROFILES

router = APIRouter()

ALLOWED_TYPES = {".pdf", ".docx"}


@router.get("/roles")
def get_roles():
    """Return available target roles for the dropdown."""
    return {key: profile["title"] for key, profile in ROLE_PROFILES.items()}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    if role not in ROLE_PROFILES:
        raise HTTPException(status_code=400, detail=f"Invalid role. Choose from: {list(ROLE_PROFILES.keys())}")

    content = await file.read()
    text = extract_text(content, ext)

    result = keyword_score(text, role)

    return {
        "filename": file.filename,
        "extracted_length": len(text),
        "analysis": result
    }