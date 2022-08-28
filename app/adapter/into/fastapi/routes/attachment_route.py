import logging
from typing import List

from adapter.into.fastapi.dependencies import get_current_user, get_storage_adapter
from fastapi import APIRouter, Depends, HTTPException
from use_case import get_attachment as get_attachment_uc
from use_case import save_attachment as save_attachment_uc

from .....ports.attachment import Attachment

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
) -> str:
    # call create use case
    attachment_entity = get_attachment_uc.get(
        storage_adapter=storage_adapter, current_user=current_user
    )
    data: dict = attachment_entity.get(
        attachment_id,
    )
    return data


@router.post("/")
async def save_attachment(
    attachment: Attachment,
    storage_adapter=Depends(get_storage_adapter),
    current_user=Depends(get_current_user),
) -> dict:
    # call create use case
    data: dict = save_attachment_uc.save(
        attachment.name, storage_adapter=storage_adapter, current_user=current_user
    )
    return data
