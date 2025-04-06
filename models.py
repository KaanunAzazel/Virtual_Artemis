from pydantic import BaseModel
from typing import List

class TagRequest(BaseModel):
    tags: List[str]

class LiveData(BaseModel):
    user_name: str
    title: str
    viewers: int
    tags: List[str]
