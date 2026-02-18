from pydantic import BaseModel


class RelatedCasesRequest(BaseModel):
    # change this only if courtseeker errors
    file_name: str
    summary: str
