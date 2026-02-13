import httpx

from config import COURTBASE_API_KEY, COURTBASE_BASE_URL


def get_related_cases(file_name: str, summary: str) -> list[dict]:
    # PLACEHOLDER FLOW: tries real Courtbase call, otherwise returns mock cases below.
    raw_cases = fetch_courtbase_related_cases(file_name=file_name, summary=summary)

    if raw_cases:
        return [normalize_case(item, f'case-{idx + 1}') for idx, item in enumerate(raw_cases)]

    # PLACEHOLDER DATA: static examples for UI development only.
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
    # CHANGE THIS: align keys exactly to real Courtbase response once contract is finalized.
    return {
        'id': str(item.get('id', default_id)),
        'case_name': str(item.get('case_name') or item.get('caseName') or 'Unknown Case'),
        'citation': str(item.get('citation', 'Citation unavailable')),
        'reason': str(item.get('reason', 'Potential relevance based on document context.')),
    }


def fetch_courtbase_related_cases(file_name: str, summary: str) -> list[dict]:
    # PLACEHOLDER API CONTRACT: endpoint/path/payload are assumptions.
    # CHANGE THIS: update endpoint, auth style, and payload to real Courtbase docs.
    if not COURTBASE_API_KEY:
        # PLACEHOLDER BEHAVIOR: missing key means caller receives mock cases.
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
        # PLACEHOLDER BEHAVIOR: swallow errors and return empty for mock fallback.
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and isinstance(data.get('cases'), list):
        return data['cases']

    return []
