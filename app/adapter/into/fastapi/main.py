import os

from fastapi import Depends, FastAPI

from .dependencies import get_current_user
from .routes import attachment_route

ENVIRONMENT = os.environ.get("ENVIRONMENT", "")

root_prefix = f"/"

PROTECTED = [Depends(get_current_user)]

app = FastAPI(
    title="attachment-api Service",
    description="attachment-api description",
    version="0.0.1",
    root_path=root_prefix,
)
app.include_router(attachment_route.router, dependencies=PROTECTED)


@app.get("/")
async def version():
    return {"message": "Attachment service"}
