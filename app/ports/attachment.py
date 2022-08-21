from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Attachment(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None