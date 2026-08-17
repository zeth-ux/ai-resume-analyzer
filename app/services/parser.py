import io
from pypdf import PdfReader
from docx import Document

def extract_text(content: bytes, ext: str) -> str:
    if ext == ".pdf":
        return _extract_pdf(content)
    elif ext == ".docx":
        return _extract_docx(content)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def _extract_pdf(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

def _extract_docx(content: bytes) -> str:
    doc = Document(io.BytesIO(content))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return text.strip()