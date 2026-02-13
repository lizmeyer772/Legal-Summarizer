import httpx

from config import HF_API_TOKEN, HF_INFERENCE_BASE_URL, HF_MODEL_ID

# add chunking, how?
def generate_summary(file_name: str, document_text: str) -> str:
    # PLACEHOLDER PROMPT:
    # - This prompt is generic and may not produce consistent legal output quality.
    #
    # EXACTLY WHAT TO CHANGE:
    # 1) Edit the prompt text below to match your required output style.
    # 2) If your documents are long, add chunking BEFORE this prompt call.
    # 3) Keep this function return value as a plain string summary.
    prompt = (
        f'You are a skilled attorney. Summarize the following legal complaint named {file_name}.\\n\\n'
        'Focus on obligations, deadlines, and legal risk.\\n\\n'
        f'DOCUMENT:\\n{document_text[:12000]}'
    )

    llm_text = call_huggingface(prompt)
    if llm_text:
        return llm_text

    # PLACEHOLDER FALLBACK:
    # - You see this text when HF token/model is missing OR HF request fails.
    # - Once your API call is stable, you can replace this with error raising/logging.
    # maybe change this
    return (
        f'Mock summary for "{file_name}": This legal document appears to define key duties, '
        'timelines, and potential legal exposure requiring attorney review.'
    )

# combo of string and text?
def generate_attorney_next_steps(file_name: str, summary: str) -> str:
    # PLACEHOLDER PROMPT:
    # - This currently returns free-form text.
    #
    # EXACTLY WHAT TO CHANGE:
    # 1) Decide desired format (example: bullet text OR strict JSON array).
    # 2) Update prompt instructions so the model always returns that format.
    # 3) If you choose JSON output, add parsing/validation before returning.
    prompt = (
        f'You are supporting an attorney reviewing {file_name}.\\n\\n'
        'Given this summary, provide next legal steps and clarifying questions.\\n\\n'
        f'SUMMARY:\\n{summary}'
    )

    llm_text = call_huggingface(prompt)
    if llm_text:
        return llm_text

    # PLACEHOLDER FALLBACK:
    # - Returned only when HF call fails or returns empty output.
    return (
        'Mock next steps: confirm filing deadlines, verify governing law and venue, '
        'and prepare follow-up questions for the client on disputed obligations.'
    )


def call_huggingface(prompt: str) -> str:
    # HUGGING FACE HTTP CALL (current implementation):
    # - Uses `HF_API_TOKEN`, `HF_MODEL_ID`, and `HF_INFERENCE_BASE_URL` from `backend/.env`.
    #
    # EXACTLY WHAT YOU MUST HAVE IN `.env`:
    # - HF_API_TOKEN=hf_...
    # - HF_MODEL_ID=<model-you-can-access>
    # - HF_INFERENCE_BASE_URL=https://api-inference.huggingface.co/models
    #
    # EXACTLY WHAT TO CHANGE LATER:
    # 1) Add better error handling (log status code and response body).
    # 2) Add retry logic for transient failures/timeouts.
    # 3) Adjust response parsing for your specific HF model output shape.
    if not HF_API_TOKEN:
        # This intentionally triggers mock fallback in caller functions.
        return ''

    url = f'{HF_INFERENCE_BASE_URL}/{HF_MODEL_ID}'
    headers = {
        'Authorization': f'Bearer {HF_API_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        'inputs': prompt,
        'parameters': {
            'max_new_tokens': 500,
            'temperature': 0.2,
        },
    }

    try:
        with httpx.Client(timeout=45.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception:
        # Current behavior: swallow errors and trigger mock fallback in caller.
        # Recommended later: log the exception and return a structured error.
        return ''

    if isinstance(data, list) and data and isinstance(data[0], dict):
        text = data[0].get('generated_text', '')
        return text.strip() if isinstance(text, str) else ''

    return ''
