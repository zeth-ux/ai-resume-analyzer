from fastapi import FastAPI
from app.routers import resume

app = FastAPI(title="AI Resume Analyzer")

app.include_router(resume.router, prefix="/resume", tags=["Resume"])

@app.get("/")
def root():
    return {"status": "ok", "message": "AI Resume Analyzer API is running"}