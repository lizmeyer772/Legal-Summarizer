import httpx

from config import HF_API_TOKEN, HF_CHAT_COMPLETIONS_URL, HF_MODEL_ID

# add chunking maybe, how?
def generate_summary(file_name: str, document_text: str) -> str:
    # need to update these prompts
    prompt = f"""
You are an attorney assistant. Analyze the legal document titled "{file_name}".

Return ONLY Markdown in this exact structure and order.
Do not add any intro or outro text.
Use short bullet points only, no long paragraphs.

## Executive Summary
- 3 to 5 bullets, each <= 20 words.

## Parties and Posture
- Identify plaintiff(s), defendant(s), and procedural posture.
- 3 to 5 bullets, each <= 20 words.

## Key Obligations
- Contractual or legal duties by party.
- 3 to 7 bullets, each <= 20 words.

## Deadlines and Time-Sensitive Items
- Dates, deadlines, notice periods, limitations windows, hearing dates.
- 3 to 7 bullets, each <= 20 words.
- If no clear deadline exists, include: - Not specified in provided text.

## Legal Risks and Exposure
- Claims, defenses, liability exposure, sanctions risk, compliance risk.
- 3 to 7 bullets, each <= 20 words.

## Missing Facts / Clarifying Questions
- Questions counsel should ask next.
- 5 to 8 bullets, each <= 20 words.

Rules:
- Be factual and neutral.
- Do not invent facts.
- If uncertain, say "Unclear from provided text."
- Preserve important names, dates, dollar amounts, and citations exactly as written.

DOCUMENT:
{document_text[:12000]}
""".strip()

    llm_text = call_huggingface(prompt)
    if llm_text:
        return llm_text

    return (
        f'Mock summary for "{file_name}": This legal document appears to define key duties, '
        'timelines, and potential legal exposure requiring attorney review.'
    )


def generate_attorney_next_steps(file_name: str, summary: str) -> str:
    # need to update these prompts
    prompt = (
        f'You are supporting an attorney reviewing {file_name}.\\n\\n'
        'Given this summary, provide next legal steps and clarifying questions.\\n\\n'
        f'SUMMARY:\\n{summary}'
    )

    llm_text = call_huggingface(prompt)
    if llm_text:
        return llm_text

    return (
        'Mock next steps: confirm filing deadlines, verify governing law and venue, '
        'and prepare follow-up questions for the client on disputed obligations.'
    )


def call_huggingface(prompt: str) -> str:

    if not HF_API_TOKEN:
        return ''

    headers = {
        'Authorization': f'Bearer {HF_API_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': HF_MODEL_ID,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 500,
        'temperature': 0.2,
    }

    try:
        with httpx.Client(timeout=45.0) as client:
            response = client.post(HF_CHAT_COMPLETIONS_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        print(f'Hugging Face request failed: {exc}')
        return ''

    if isinstance(data, dict):
        choices = data.get('choices', [])
        if isinstance(choices, list) and choices and isinstance(choices[0], dict):
            message = choices[0].get('message', {})
            if isinstance(message, dict):
                text = message.get('content', '')
                return text.strip() if isinstance(text, str) else ''

    return ''
