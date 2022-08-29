import logging
from typing import List

from hex_lib.ports.storage import StorageAdapter, UploadUrlData

logger = logging.getLogger(__name__)


class BaseEntity:
    def __init__(
        self,
        storage_adapter: StorageAdapter,
    ):
        self.storage_adapter = storage_adapter


class AttachmentEntity(BaseEntity):
    def get(self, attachment_id: str) -> str:
        """Get data by id"""
        url: str = self.storage_adapter.get_public_url(attachment_id)
        return url

    def save(self, attachment_id: str) -> UploadUrlData:
        url_data: UploadUrlData = self.storage_adapter.upload_url(attachment_id)
        return url_data
