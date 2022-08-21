from typing import List

from hex_lib.ports.user import UserData
from hex_lib.ports.storage import StorageAdapter
from app.domain.attachment import AttachmentEntity


def save(
    attachment_data: dict,
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
    task_data: List[str] = entity.save(attachment_data)
    return task_data
