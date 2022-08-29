from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Attachment(BaseModel):
    name: str


class UploadData(BaseModel):
    attachment_id: str
    upload_url: str
    fields: dict
