# Legal Summarizer

Simple React frontend + simple Python (FastAPI) backend.

## Run locally

1. Start backend API (Python):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

2. Start frontend (new terminal):

```bash
cd /Users/lizmeyer/Desktop/Legal-Summarizer/Legal-Summarizer
npm install
npm run dev
```

Frontend calls `/api/*` and Vite proxies to `http://127.0.0.1:8000`.

## Minimal project structure

- `src/App.jsx`: UI + frontend API calls
- `src/main.jsx`: React entry
- `src/styles.css`: styling
- `backend/main.py`: FastAPI routes
- `backend/document_processing.py`: file text extraction
- `backend/llm.py`: Hugging Face calls + summary/next-step generation
- `backend/courtbase.py`: related cases retrieval
- `backend/schemas.py`: request models
- `backend/config.py`: environment variable loading
- `backend/requirements.txt`: backend dependencies
- `backend/.env.example`: environment variable template

## Environment setup

Copy and edit:

```bash
cp backend/.env.example backend/.env
```

Then set real values for:

- `HF_API_TOKEN`
- `HF_MODEL_ID`
- `COURTBASE_API_KEY`
