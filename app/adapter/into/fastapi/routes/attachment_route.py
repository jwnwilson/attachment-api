import logging
from typing import List

from adapter.into.fastapi.dependencies import get_current_user, get_storage_adapter
from fastapi import APIRouter, Depends, HTTPException
from hex_lib.ports.storage import UploadUrlData
from ports.attachment import Attachment, UploadData
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
) -> UploadData:
    """
    Request an upload url for a file.

    Upload file using a multipart/form-data POST request to the upload_url.
    Set "Content-Type", "multipart/form-data" header
    Set fields in data payload
    Send file in data payload with key "file"
    """
    # call create use case
    upload_url_data: UploadUrlData = save_attachment_uc.save(
        attachment.name, storage_adapter=storage_adapter
    )
    attachment_id = upload_url_data.fields["key"].split("/")[-1]
    upload_data: UploadData = UploadData(
        upload_url=upload_url_data.upload_url,
        fields=upload_url_data.fields,
        attachment_id=attachment_id,
    )

    return upload_data
