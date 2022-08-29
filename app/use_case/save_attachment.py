import uuid
from typing import List

from hex_lib.ports.storage import StorageAdapter, UploadUrlData

from app.domain.attachment import AttachmentEntity


def save(attachment_name: str, storage_adapter: StorageAdapter) -> UploadUrlData:
    # create attachment
    entity = AttachmentEntity(storage_adapter=storage_adapter)
    attachment_path = str(uuid.uuid4()) + "-" + attachment_name
    attachment_data: UploadUrlData = entity.save(attachment_path)
    return attachment_data
