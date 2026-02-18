# needed libraries
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from courtbase import get_related_cases
from document_processing import extract_document_text
from llm import generate_attorney_next_steps, generate_summary
from schemas import RelatedCasesRequest


app = FastAPI(title='Legal Summarizer API', version='0.1.0')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health')
def health_check():
    return {'status': 'ok'}


@app.post('/api/v1/analysis/summarize')


def summarize_document(file: UploadFile = File(...)):
    document_text = extract_document_text(file)
    summary = generate_summary(file.filename, document_text)
    next_steps = generate_attorney_next_steps(file.filename, summary)
    return {'summary': summary, 'next_steps': next_steps}


@app.post('/api/v1/analysis/related-cases')
def related_cases(payload: RelatedCasesRequest):
    # leave for later
    cases = get_related_cases(payload.file_name, payload.summary)
    return {'cases': cases}
