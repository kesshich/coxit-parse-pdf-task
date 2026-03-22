from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    id: str
    filename: str
    result: str

