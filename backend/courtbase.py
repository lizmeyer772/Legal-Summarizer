import httpx

from config import COURTBASE_API_KEY, COURTBASE_BASE_URL


async def get_related_cases(file_name: str, summary: str) -> list[dict]:
    raw_cases = await fetch_courtbase_related_cases(file_name=file_name, summary=summary)

    if raw_cases:
        return [normalize_case(item, f'case-{idx + 1}') for idx, item in enumerate(raw_cases)]

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
    return {
        'id': str(item.get('id', default_id)),
        'case_name': str(item.get('case_name') or item.get('caseName') or 'Unknown Case'),
        'citation': str(item.get('citation', 'Citation unavailable')),
        'reason': str(item.get('reason', 'Potential relevance based on document context.')),
    }


async def fetch_courtbase_related_cases(file_name: str, summary: str) -> list[dict]:
    # TODO: Replace endpoint path and payload fields with the real Courtbase API contract.
    if not COURTBASE_API_KEY:
        return []

    url = f'{COURTBASE_BASE_URL}/related-cases'
    headers = {
        'Authorization': f'Bearer {COURTBASE_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {'fileName': file_name, 'summary': summary}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception:
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and isinstance(data.get('cases'), list):
        return data['cases']

    return []
