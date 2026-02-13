import httpx

from config import HF_API_TOKEN, HF_INFERENCE_BASE_URL, HF_MODEL_ID


def generate_summary(file_name: str, document_text: str) -> str:
    # PLACEHOLDER PROMPT: good enough for scaffold output, not tuned for legal quality.
    # CHANGE THIS: refine prompt + add structured output format you can reliably parse.
    prompt = (
        f'You are a legal assistant. Summarize the following document named {file_name}.\\n\\n'
        'Focus on obligations, deadlines, and legal risk.\\n\\n'
        f'DOCUMENT:\\n{document_text[:12000]}'
    )

    llm_text = call_huggingface(prompt)
    if llm_text:
        return llm_text

    # PLACEHOLDER FALLBACK: used when Hugging Face is not configured or request fails.
    return (
        f'Mock summary for "{file_name}": This legal document appears to define key duties, '
        'timelines, and potential legal exposure requiring attorney review.'
    )


def generate_attorney_next_steps(file_name: str, summary: str) -> str:
    # PLACEHOLDER PROMPT: produces generic guidance.
    # CHANGE THIS: enforce exact output schema (e.g., JSON list of steps/questions).
    prompt = (
        f'You are supporting an attorney reviewing {file_name}.\\n\\n'
        'Given this summary, provide next legal steps and clarifying questions.\\n\\n'
        f'SUMMARY:\\n{summary}'
    )

    llm_text = call_huggingface(prompt)
    if llm_text:
        return llm_text

    # PLACEHOLDER FALLBACK: static text until real model responses are dependable.
    return (
        'Mock next steps: confirm filing deadlines, verify governing law and venue, '
        'and prepare follow-up questions for the client on disputed obligations.'
    )


def call_huggingface(prompt: str) -> str:
    # PLACEHOLDER HTTP CLIENT: minimal error handling and response parsing.
    # CHANGE THIS: add retries/timeouts by error type + model-specific response parsing.
    if not HF_API_TOKEN:
        # PLACEHOLDER BEHAVIOR: empty string triggers mock fallback in caller.
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
        # PLACEHOLDER BEHAVIOR: swallow error and fall back to mock output.
        return ''

    if isinstance(data, list) and data and isinstance(data[0], dict):
        text = data[0].get('generated_text', '')
        return text.strip() if isinstance(text, str) else ''

    return ''
