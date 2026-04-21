import httpx
import re

from config import HF_API_TOKEN, HF_CHAT_COMPLETIONS_URL, HF_MODEL_ID

# add chunking maybe, how?
def generate_summary(file_name: str, document_text: str) -> str:
    # need to update these prompts
    prompt = f"""
You are assisting counsel who has received this legal document for review.
Assume the reader is analyzing the document after it was filed or served, not drafting it.
Focus on what the receiving attorney needs to understand quickly.
Analyze the legal document titled "{file_name}".

Return ONLY Markdown in this exact structure and order.
Use section headings that begin with exactly "## ".
Do not use "#", "###", or any other heading level.
Do not add any heading not listed below.
Do not add any intro or outro text.
Do not add a section called "Facts," "Facts that are explicitly present," or anything similar.
Begin immediately with "## Executive Summary".
Use short bullet points only, no long paragraphs.
State only facts that are explicitly present in the document.
Do not convert stated facts into questions.
Use "Unclear from provided text." only when the document truly does not answer the point.
Prefer concrete document-specific facts over generic commentary.
Keep the analysis flexible across civil, criminal, regulatory, or administrative matters.
Avoid repeating the same fact in multiple sections.
Adjust the level of detail to the complexity of the document.
For simple cases, summarize only the core facts and claims.
For more complex cases, include the key specific products, agreements, incidents, actors, counts, assets, or events needed to understand the dispute.
Do not oversimplify a multi-claim or multi-issue case into generic labels.

## Executive Summary
- 3 to 5 bullets, each <= 20 words.
- Do not repeat the same label or phrasing across consecutive bullets.
- Summarize the core conduct, dispute, or event described in the document.
- Do not restate the case caption, party labels, or filing label in this section.

## Parties and Posture
- Identify the named parties, their roles, and the procedural posture.
- State posture as the type/status of filing or proceeding, not jurisdiction.
- Examples: civil complaint filed, criminal complaint filed, motion to dismiss pending, order granting injunction.
- 3 to 5 bullets, each <= 20 words.
- When plaintiff/defendant roles exist, format them as `Plaintiff: Name` and `Defendant: Name`.
- Do not use parenthetical labels like `(plaintiff)` or `(defendant)`.

## Context / Background
- State important factual background that helps interpret the document.
- Include status, role, condition, or situational context explicitly stated in the document.
- Examples: disability status, organizational role, prior investigation, relationship background, custody status.
- 3 to 6 bullets, each <= 20 words.
- If no meaningful background context appears, include: - Not specified in provided text.
- Exclude background facts that are not materially helpful to understanding the case.
- Do not repeat facts already stated in Executive Summary, Parties and Posture, or Main Claims / Charges.
- Do not include trivial corroboration details, repetitive witness statements, or investigative minutiae unless central to the case.
- Prefer background that explains who the person is, why the dispute arose, or what event led to the filing.
- In complex cases, name the principal products, agreements, incidents, policies, assets, or groups that drive the dispute.

## Main Claims / Charges
- Identify only the actual causes of action, counts, or charges stated in the document.
- 3 to 7 bullets, each <= 20 words.
- If the document has numbered claims, counts, or causes of action, follow that structure.
- Do not present sub-theories as separate claims if they are part of one claim or count.
- For each bullet, include the specific statute, code section, rule, or citation when the document provides it.
- Do not omit a citation if the document states one.
- Format each bullet like: Claim name (citation).
- Prefer the claim or count heading used in the document over your own paraphrase.
- For civil complaints, list each cause of action first before listing any supporting theories.
- For criminal complaints, list each charged count first before any supporting allegations.
- If a claim cites a U.S.C., state code, regulation, or rule, include that citation in the same bullet.
- Do not prefix bullets with labels like "First Claim," "Second Claim," or "Count 1" unless that numbering is itself legally necessary.
- State the actual claim or charge name directly.
- Do not include explanations, summaries, theories, elements, or supporting allegations in this section.
- Do not collapse multiple distinct pleaded claims into one generic category.

## Deadlines and Time-Sensitive Items
- Dates, deadlines, notice periods, limitations windows, hearing dates.
- 3 to 7 bullets, each <= 20 words.
- If no clear deadline exists, include: - Not specified in provided text.
- Do not treat historical filing dates as deadlines unless the document makes them time-sensitive.
- Do not infer response deadlines or obligations not stated in the document.

## Missing Facts
- Only include facts genuinely missing, ambiguous, or internally inconsistent in the provided text.
- State the missing fact directly, not as a question.
- Use 0 to 3 bullets, each <= 20 words.
- If no major facts are missing, include exactly one bullet: - No major missing facts identified from provided text.
- Do not include that fallback bullet if any missing facts are listed.
- Do not label a fact as missing if the document answers it at a general or charging level.
- Prefer narrow missing facts over broad statements like "extent of involvement" unless the document truly omits that information.
- Prefer missing facts tied to a named party, claim, date, event, witness, or cited evidence.
- Avoid broad theory questions about an organization or case unless the document makes that issue central.
- Do not include facts that are merely useful for investigation but not actually missing from the document.
- Do not include speculative background items like prior convictions, associates, or unrelated history unless the document makes them material.

Rules:
- Be factual and neutral.
- Do not invent facts.
- If the document answers a question, state the answer instead of asking the question.
- Use the Context / Background section for important explanatory facts that are clearly stated.
- If uncertain, say "Unclear from provided text."
- Preserve important names, dates, dollar amounts, and citations exactly as written.
- Do not infer strategy, deadlines, or evidence beyond what the document itself supports.
- Do not repeat party names, dates, claims, or allegations across sections unless necessary.
- Keep the summary focused on what the document says, not what counsel may later want to learn.

DOCUMENT:
{document_text[:12000]}
""".strip()

    llm_text = call_huggingface(prompt)
    if llm_text:
        return normalize_summary_markdown(llm_text)

    return (
        f'Mock summary for "{file_name}": This legal document appears to define key duties, '
        'timelines, and potential legal exposure requiring attorney review.'
    )


def generate_attorney_next_steps(file_name: str, summary: str) -> str:
    # need to update these prompts
    prompt = f"""
You are assisting counsel who has received this legal document for review.
Assume the reader is analyzing the document after it was filed or served, not drafting it.
Frame recommendations from the perspective of the receiving attorney, usually defense or responding counsel.
Do not recommend actions that belong to the filing party, prosecutor, or court unless the summary specifically says receiving counsel must respond.
Review the legal document summary for "{file_name}".

Return ONLY Markdown in this exact structure and order.
Do not add any intro or outro text.
Use short bullet points only, no long paragraphs.
Use section headings that begin with exactly "## ".
Do not use "#", "###", or any other heading level.
Do not add a top-level heading like "Summary".
Prefer document-specific recommendations over generic litigation tasks.
Each bullet must describe a concrete action an attorney or investigator can actually take.
Prefer action verbs like obtain, review, subpoena, interview, confirm, compare, preserve, or request.
Name the specific record, witness, filing, agency, or fact to pursue when the summary supports it.
Avoid vague phrases like "obtain information," "look into," or "review for completeness."
Keep recommendations flexible across civil, criminal, regulatory, or administrative matters.
Only include an action if the summary provides a concrete factual basis for it.
Use triggered actions: fact in summary -> specific next step.
Do not include standard litigation boilerplate unless the summary clearly supports it.

## Evidence / Record Requests
- Specific documents, records, witness statements, or agency materials counsel should obtain.
- Only request evidence or documents tied to issues mentioned in the summary.
- Use 2 to 4 bullets, each <= 20 words.
- Do not request broad background materials unless the summary specifically points to them.
- Name the exact category of record when possible.
- Bad example: obtain information about relationship with Bateman.
- Good example: obtain messages, call logs, or witness statements linking defendants to Bateman.
- Prefer records tied to named parties, alleged events, dates, communications, contracts, filings, or cited sources.
- Focus on concrete items counsel could realistically request, preserve, inspect, or subpoena next.
- Always include this section.

## Witness Interviews / Depositions
- Include this section only if the summary identifies named people whose knowledge appears material.
- Examples of triggers: repeated complaints to management, named supervisors, named coworkers, identified investigators, central first-hand plaintiff narrative.
- Use 1 to 3 bullets, each <= 20 words.
- Name the specific witness or deponent and the reason they matter.
- Omit this section entirely if no concrete witness or deposition action is supported by the summary.

## Key Questions to Resolve
- Include only factual questions that would materially change counsel's immediate evaluation of the document.
- Only ask about facts genuinely missing, ambiguous, or inconsistent in the summary.
- Do not ask about facts already stated in the summary.
- Use 0 to 2 bullets, each <= 20 words.
- Ask who/what/when/where questions tied to a named party, event, date, witness, or document gap.
- Omit this section entirely if no concrete question is needed next.
- If omitted, do not replace it with another heading.

## Issues to Watch
- Deadlines, exposure, custody issues, compliance issues, or other facts requiring close follow-up.
- Only include follow-up items supported by the provided summary.
- Use 0 to 2 bullets, each <= 20 words.
- Do not include generic docket management or speculative penalty items unless supported by the summary.
- Focus on developments that could change case posture or evidence preservation needs.
- Keep this section concrete and tied to the summary, not general case-management advice.
- Omit this section entirely if there is no specific follow-up issue identified in the summary.
- Do not restate relief requested, generic compliance concerns, or broad litigation risk.
- If omitted, do not replace it with another heading.

Rules:
- Be factual and neutral.
- Do not invent facts.
- Base all recommendations only on the provided summary.
- If the summary does not support a recommendation, omit it.
- Prefer fewer, more specific bullets over vague filler.
- Write for the attorney receiving the document, not the attorney who drafted or filed it.
- If uncertain, say "Unclear from provided summary."
- Preserve important names, dates, dollar amounts, and citations exactly as written.
- Avoid repeating the same recommendation in multiple sections.
- Keep the overall next-steps output short and practical.
- Do not include generic review tasks; prioritize triggered witness actions, record requests, concrete questions, and specific issues to watch.

SUMMARY:
{summary[:8000]}
""".strip()

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


def normalize_summary_markdown(text: str) -> str:
    lines = text.splitlines()
    normalized_lines = []
    in_main_claims = False

    claim_prefix_pattern = re.compile(
        r'^(\s*[-*]\s*)(?:(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+claim|count\s+\d+|claim\s+\d+)\s*:\s*',
        re.IGNORECASE,
    )

    for line in lines:
        if line.startswith('## '):
            in_main_claims = line.strip() == '## Main Claims / Charges'
            normalized_lines.append(line)
            continue

        if in_main_claims and re.match(r'^\s*[-*]\s+', line):
            line = claim_prefix_pattern.sub(r'\1', line)

        normalized_lines.append(line)

    return '\n'.join(normalized_lines).strip()
