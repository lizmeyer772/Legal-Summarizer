import os

from dotenv import load_dotenv

load_dotenv()

# waiting on HF_API_TOKEN
HF_API_TOKEN = os.getenv('HF_API_TOKEN', '')
HF_MODEL_ID = os.getenv('HF_MODEL_ID', 'meta-llama/Llama-3.1-8B-Instruct')
HF_INFERENCE_BASE_URL = os.getenv('HF_INFERENCE_BASE_URL', 'https://api-inference.huggingface.co/models')

# need courtbase api key, to-do
COURTBASE_API_KEY = os.getenv('COURTBASE_API_KEY', '')
COURTBASE_BASE_URL = os.getenv('COURTBASE_BASE_URL', 'https://api.courtbase.example')
