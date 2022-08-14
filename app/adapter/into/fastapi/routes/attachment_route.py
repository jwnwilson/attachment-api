import logging
from typing import List

from adapter.into.fastapi.dependencies import (
    get_db_adapater,
    get_task_storage_adapter,
    get_template_storage_adapter,
)
from fastapi import APIRouter, Depends, HTTPException
from use_case import list_uc

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/attachment",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_attachments(
    template_storage_adapter=Depends(get_template_storage_adapter),
    task_storage_adapter=Depends(get_task_storage_adapter),
    db_adapter=Depends(get_db_adapater),
) -> List[str]:
    # call create use case
    data: List[str] = list_uc.list(
        db_adapter,
        task_storage_adapter=task_storage_adapter,
        template_storage_adapter=template_storage_adapter,
    )
    return data
