from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    price: str
    company: Optional[str]