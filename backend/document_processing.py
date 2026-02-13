from fastapi import UploadFile


async def extract_document_text(uploaded_file: UploadFile) -> str:
    # TODO: Replace with robust parsing for PDF/DOCX and OCR if needed.
    content = await uploaded_file.read()
    await uploaded_file.seek(0)

    if not content:
        return ''

    try:
        return content.decode('utf-8', errors='ignore')
    except Exception:
        return ''
