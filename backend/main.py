# needed libraries
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from courtbase import get_related_cases
from document_processing import extract_document_text
from llm import generate_attorney_next_steps, generate_summary
from schemas import RelatedCasesRequest

# do i need a version?
app = FastAPI(title='Legal Summarizer API', version='0.1.0')

# ask if i need this
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ask if i need this
@app.get('/health')
def health_check():
    return {'status': 'ok'}

# ask if i need this, like isnt this a url?
@app.post('/api/v1/analysis/summarize')

# so clarify if anything should change in the argument
def summarize_document(file: UploadFile = File(...)):
    # WHAT THIS ENDPOINT DOES NOW:
    # 1) Reads text from uploaded file.
    # 2) Generates summary.
    # 3) Generates next steps/questions from that summary.
    #
    # WHEN TO CHANGE THIS:
    # - Only if you decide to add a DB, queue, background jobs, or multi-step workflow tracking.
    document_text = extract_document_text(file)
    summary = generate_summary(file.filename, document_text)
    next_steps = generate_attorney_next_steps(file.filename, summary)
    return {'summary': summary, 'next_steps': next_steps}


@app.post('/api/v1/analysis/related-cases')
def related_cases(payload: RelatedCasesRequest):
    # WHAT THIS ENDPOINT DOES NOW:
    # - Calls Courtbase helper and returns mapped case data.
    # - If Courtbase is not configured, helper returns mock data.
    #
    # WHEN TO CHANGE THIS:
    # - Add extra request fields (jurisdiction/date/topic filters) once needed.
    cases = get_related_cases(payload.file_name, payload.summary)
    return {'cases': cases}
