from pydantic import BaseModel


class RelatedCasesRequest(BaseModel):
    file_name: str
    summary: str
