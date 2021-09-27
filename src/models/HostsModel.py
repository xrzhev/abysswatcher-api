from pydantic import BaseModel, HttpUrl
from typing import List

class RegisterHost(BaseModel):
    name: str
    url:  HttpUrl
    ports: List[int]
