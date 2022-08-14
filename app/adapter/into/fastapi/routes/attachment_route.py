import logging
from typing import List

from adapter.into.fastapi.dependencies import (
    get_storage_adapter,
    get_current_user
)
from fastapi import APIRouter, Depends, HTTPException
from use_case import get_attachment

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
    current_user=Depends(get_current_user)
) -> List[str]:
    # call create use case
    data: List[str] = get_attachment.get(
        attachment_id,
        storage_adapter=storage_adapter,
        current_user=current_user
    )
    return data
