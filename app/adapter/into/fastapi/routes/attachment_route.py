import logging
from typing import List

from adapter.into.fastapi.dependencies import get_current_user, get_storage_adapter
from fastapi import APIRouter, Depends, HTTPException
from ports.attachment import Attachment
from use_case import get_attachment as get_attachment_uc
from use_case import save_attachment as save_attachment_uc

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/attachment",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/{attachment_id}")
async def get_attachment(
    attachment_id: str,
    storage_adapter=Depends(get_storage_adapter),
    current_user=Depends(get_current_user),
) -> dict:
    download_url = get_attachment_uc.get(attachment_id, storage_adapter=storage_adapter)
    data: dict = {"download_url": download_url}
    return data


@router.post("/")
async def save_attachment(
    attachment: Attachment,
    storage_adapter=Depends(get_storage_adapter),
    current_user=Depends(get_current_user),
) -> dict:
    # call create use case
    upload_url: str = save_attachment_uc.save(
        attachment.name, storage_adapter=storage_adapter
    )
    data: dict = {"upload_url": upload_url}
    return data
