from typing import Annotated, Any

from fastapi import APIRouter, Cookie

from backend.core.models import PersonId, Voter
from backend.core.operations import db

router = APIRouter(
    prefix="/voter",
    tags=["voter",],
    responses={404: {"description": "Not found"}},
)


@router.get("/{voter_id}")
async def get_voter(voter_id: PersonId, cookie: Annotated[str, Cookie()]) -> Voter:
    print("&"*60)
    print(cookie)
    return db.voters[voter_id]


@router.put("/{voter_id}/joinrequest/{pollid}")
async def join_poll():
    ...

#
# @router.get("/signup/")
# async def
