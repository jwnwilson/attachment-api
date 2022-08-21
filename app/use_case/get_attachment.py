from typing import List

from hex_lib.ports.user import UserData
from hex_lib.ports.storage import StorageAdapter
from app.domain.attachment import AttachmentEntity


def get(
    attachment_id: str,
    storage_adapter: StorageAdapter,
) -> str:
    """[summary]

    Args:
        html (str): [description]
        file_path (str): [description]

    Returns:
        [type]: [description]
    """
    # create pdf
    entity = AttachmentEntity(
        storage_adapter=storage_adapter,
    )
    url = entity.get(attachment_id)
    return url


def save(
    attachment_id: str,
    storage_adapter: StorageAdapter,
) -> str:
    entity = AttachmentEntity(
        storage_adapter=storage_adapter,
    )
    upload_url: str = entity.save(attachment_id)
    return upload_url
