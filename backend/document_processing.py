from fastapi import UploadFile


def extract_document_text(uploaded_file: UploadFile) -> str:
    # PLACEHOLDER: simple byte decode only. This does NOT properly parse PDF/DOCX structure.
    # CHANGE THIS: use a real parser (e.g., pypdf/docx/textract) and optional OCR for scanned files.
    content = uploaded_file.file.read()
    uploaded_file.file.seek(0)

    if not content:
        return ''

    try:
        return content.decode('utf-8', errors='ignore')
    except Exception:
        return ''
