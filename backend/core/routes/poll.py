from fastapi import APIRouter, Response, UploadFile
from starlette.responses import RedirectResponse

from backend.core.models import Poll, PollId
from backend.core.operations import db

router = APIRouter(
    prefix="/poll",
    tags=["poll",],
    responses={404: {"description": "Not found"}},
)


@router.get("/{poll_id}", name='poll')
async def get_poll(poll_id: PollId) -> Poll:
    return db.polls[poll_id]


@router.post("/{poll_id}/upload")
async def upload_porfolio(file: UploadFile):
    print("hitting upload file", file)

# @router.web
