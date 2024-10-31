import logging
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.params import Depends
from starlette.responses import JSONResponse, RedirectResponse

from ..models.person import Candidate
from ..models.poll import Poll, PollId
from backend.election.db import fakedata
from backend.election.utils.parses import parse_poll

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


router = APIRouter(
    prefix="/admin",
    tags=["admin", ],
    responses={404: {"description": "Not found"}},
)


@router.get("/polls/{pollid}")
async def get_poll(pollid: PollId, request: Request):
    redirect_url = request.url_for('poll', poll_id=pollid)
    return RedirectResponse(url=redirect_url)


@router.post("/createPoll")
async def create_poll(poll: Poll = Depends(parse_poll)):
    """
    :param poll:
    :return:
    """
    print(poll)
    return JSONResponse({"poll_id": poll.poll_id,})


@router.post("/updatePoll")
async def update_poll():
    ...


@router.post("/addCandidate")
async def add_candiates(candidate: Annotated[Candidate, Form()]):
    print("recieved a candidate", candidate)
    return candidate.model_dump()


@router.get("/getCandidates")
async def get_candidates():
    _l = []
    for candidate in fakedata.candidates.values():
        _l.append(candidate)

    return JSONResponse(_l)


@router.delete("/deletePoll")
async def delete_poll():
    ...
