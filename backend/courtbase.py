import httpx

from config import COURTBASE_API_KEY, COURTBASE_BASE_URL


def get_related_cases(file_name: str, summary: str) -> list[dict]:
    # FLOW TODAY:
    # 1) Try Courtbase API call.
    # 2) If call returns no data, return mock cases for UI testing.
    raw_cases = fetch_courtbase_related_cases(file_name=file_name, summary=summary)

    if raw_cases:
        return [normalize_case(item, f'case-{idx + 1}') for idx, item in enumerate(raw_cases)]

    # PLACEHOLDER DATA:
    # - Delete/replace this list after real Courtbase integration is working.
    return [
        {
            'id': 'case-1',
            'case_name': 'Sample v. Example Corp.',
            'citation': '123 F.3d 456 (9th Cir. 2018)',
            'reason': 'Mock match based on contract interpretation and notice requirements.',
        },
        {
            'id': 'case-2',
            'case_name': 'Doe v. Placeholder LLC',
            'citation': '789 U.S. 101 (2021)',
            'reason': 'Mock match based on procedural posture and disputed obligations.',
        },
    ]


def normalize_case(item: dict, default_id: str) -> dict:
    # EXACTLY WHAT TO CHANGE WHEN YOU HAVE REAL COURTBASE RESPONSES:
    # 1) Print one real API response item.
    # 2) Update key mapping below so each field maps correctly.
    # 3) Keep output keys exactly as: id, case_name, citation, reason
    #    because frontend expects these keys.
    return {
        'id': str(item.get('id', default_id)),
        'case_name': str(item.get('case_name') or item.get('caseName') or 'Unknown Case'),
        'citation': str(item.get('citation', 'Citation unavailable')),
        'reason': str(item.get('reason', 'Potential relevance based on document context.')),
    }


def fetch_courtbase_related_cases(file_name: str, summary: str) -> list[dict]:
    # PLACEHOLDER CONTRACT (likely needs changes):
    # - URL path `/related-cases` is assumed.
    # - Payload keys `fileName` and `summary` are assumed.
    #
    # EXACTLY WHAT TO CHANGE USING COURTBASE DOCS:
    # 1) Replace URL path if docs specify a different endpoint.
    # 2) Replace payload keys/shape with the exact required request body.
    # 3) Replace auth header if Courtbase requires a different format.
    if not COURTBASE_API_KEY:
        # No key set -> caller falls back to mock cases.
        return []

    url = f'{COURTBASE_BASE_URL}/related-cases'
    headers = {
        'Authorization': f'Bearer {COURTBASE_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {'fileName': file_name, 'summary': summary}

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception:
        # Current behavior: fail quietly and let caller return mock cases.
        # Recommended later: log response error details for debugging.
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and isinstance(data.get('cases'), list):
        return data['cases']

    return []
