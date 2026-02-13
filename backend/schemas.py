from pydantic import BaseModel


class RelatedCasesRequest(BaseModel):
    # CURRENT USE: minimal fields needed by the placeholder related-cases endpoint.
    # CHANGE THIS: add filters like jurisdiction/date/topic when you expand Courtbase queries.
    file_name: str
    summary: str
