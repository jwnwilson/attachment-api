from typing import List
import uuid

from hex_lib.ports.user import UserData
from hex_lib.ports.storage import StorageAdapter
from app.domain.attachment import AttachmentEntity


def save(
    attachment_name: str,
    storage_adapter: StorageAdapter,
    current_user: UserData
) -> List[str]:
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
        current_user=current_user,
    )
    attachment_path = str(uuid.uuid4()) + '-' + attachment_name
    task_data: List[str] = entity.save(attachment_path)
    return task_data
