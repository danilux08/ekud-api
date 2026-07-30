from pydantic import BaseModel

class SearchData(BaseModel):
    query: str
