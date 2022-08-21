from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Attachment(BaseModel):
    name: str
