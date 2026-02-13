from io import BytesIO
from pathlib import Path

from docx import Document
from fastapi import UploadFile
from pypdf import PdfReader


def extract_document_text(uploaded_file: UploadFile) -> str:
    # Supports .txt, .pdf, and .docx. Returns empty string on parse failure.
    content = uploaded_file.file.read()
    uploaded_file.file.seek(0)

    if not content:
        return ''

    extension = Path(uploaded_file.filename or '').suffix.lower()

    if extension == '.pdf':
        return _extract_pdf_text(content)
    if extension == '.docx':
        return _extract_docx_text(content)
    if extension == '.txt':
        return _decode_bytes(content)

    # Fallback for unknown extensions: attempt plain-text decode.
    return _decode_bytes(content)


def _extract_pdf_text(content: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(content))
        pages = [page.extract_text() or '' for page in reader.pages]
        return '\n'.join(pages).strip()
    except Exception:
        return ''


def _extract_docx_text(content: bytes) -> str:
    try:
        document = Document(BytesIO(content))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
        return '\n'.join(paragraphs).strip()
    except Exception:
        return ''


def _decode_bytes(content: bytes) -> str:
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return content.decode('latin-1')
        except Exception:
            return ''
