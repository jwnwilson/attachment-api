import uuid
from typing import List

from hex_lib.ports.storage import StorageAdapter
from hex_lib.ports.user import UserData

from app.domain.attachment import AttachmentEntity


def save(attachment_name: str, storage_adapter: StorageAdapter) -> str:
    # create attachment
    entity = AttachmentEntity(storage_adapter=storage_adapter)
    attachment_path = str(uuid.uuid4()) + "-" + attachment_name
    attachment_url: str = entity.save(attachment_path)
    return attachment_url
