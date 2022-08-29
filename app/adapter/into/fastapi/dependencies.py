import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from hex_lib.adapter.out.storage.s3 import S3Adapter
from hex_lib.ports.storage import StorageAdapter
from hex_lib.ports.user import UserData
from starlette.requests import Request

ENVIRONMENT = os.environ["ENVIRONMENT"]

security = HTTPBearer()


def get_current_user(
    request: Request, credentials: HTTPBasicCredentials = Depends(security)
) -> UserData:
    # attempt to get user id from authorizer logic
    user_id = (
        request.scope.get("aws.event", {})
        .get("requestContext", {})
        .get("authorizer", {})
        .get("user_id")
    )
    if not user_id:
        raise HTTPException(status_code=403, detail="User not found")
    return UserData(user_id=user_id)


def get_storage_adapter(
    user_data: UserData = Depends(get_current_user),
) -> StorageAdapter:
    bucket_name = f"jwnwilson-attachments-{ENVIRONMENT}"
    return S3Adapter(
        {"bucket": bucket_name}, user=user_data, upload_prefix="attachment-api"
    )
