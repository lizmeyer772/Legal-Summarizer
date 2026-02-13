import os

from dotenv import load_dotenv

load_dotenv()

# REQUIRED SETUP STEPS:
# 1) Open `backend/.env`.
# 2) Replace `HF_API_TOKEN=replace-with-your-token` with your real Hugging Face token.
# 3) Set `HF_MODEL_ID` to the exact model id you have access to (example: meta-llama/Llama-3.1-8B-Instruct).
# 4) Keep HF_INFERENCE_BASE_URL as-is unless Hugging Face gives you a different endpoint.
HF_API_TOKEN = os.getenv('HF_API_TOKEN', '')
HF_MODEL_ID = os.getenv('HF_MODEL_ID', 'meta-llama/Llama-3.1-8B-Instruct')
HF_INFERENCE_BASE_URL = os.getenv('HF_INFERENCE_BASE_URL', 'https://api-inference.huggingface.co/models')

# REQUIRED SETUP STEPS:
# 1) Open `backend/.env`.
# 2) Replace `COURTBASE_API_KEY=replace-with-your-key` with your real Courtbase key.
# 3) Replace `COURTBASE_BASE_URL=https://api.courtbase.example` with the real base URL from Courtbase docs.
COURTBASE_API_KEY = os.getenv('COURTBASE_API_KEY', '')
COURTBASE_BASE_URL = os.getenv('COURTBASE_BASE_URL', 'https://api.courtbase.example')
