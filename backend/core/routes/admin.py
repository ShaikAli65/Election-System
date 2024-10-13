from typing import Annotated, Any

from fastapi import APIRouter, Request
from starlette.datastructures import FormData
from starlette.responses import JSONResponse, RedirectResponse, Response

from backend.core.models import Admin, Candidate, PersonId, Poll, PollId
from backend.core.operations import db

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

router = APIRouter(
    prefix="/admin",
    tags=["admin",],
    responses={404: {"description": "Not found"}},
)


@router.get("/polls/{poll_id}")
async def get_poll(poll_id: PollId, request: Request):
    redirect_url = request.url_for('poll', poll_id=poll_id)
    return RedirectResponse(url=redirect_url)


@router.post("/create_poll")
async def create_poll(poll: Poll):
    db.create_poll(poll)


@router.post("/update_poll")
async def update_poll():
    ...


@router.post("/add_candidate")
async def add_candiates(candidate_data: Annotated[Any, FormData]):
    ...


@router.get("/getcandidates")
async def get_candidates():
    l = []
    for candidate in db.candidates.values():
        l.append(candidate)

    return JSONResponse(l)


@router.delete("/delete_poll")
async def delete_poll():
    ...
