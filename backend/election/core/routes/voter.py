import traceback
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.params import Depends, Form
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse
from starlette.status import HTTP_202_ACCEPTED

from election.core.contexts.admin import adminContext
from election.core.contexts.auth import AuthContext, sign_in_user
from election.core.contexts.email import send_email
from election.core.contexts.user import userContext
from election.core.models.poll import CandidateInPoll, PollId, PollShareable, PollShareableView
from election.core.models.user import PersonId
from election.db.database import AsyncDB, db_session_factory
from election.repository.candidate import CandidateRepository
from election.repository.poll import PollRepository

router = APIRouter(
    prefix="/voter",
    tags=["voter", ],
    responses={404: {"description": "Not found"}},
)


@router.post("/signin")
async def signin_user(auth_context: Annotated[AuthContext, Depends(sign_in_user)]) -> JSONResponse:
    reply_cookie = await auth_context.generate_cookie()
    resp = JSONResponse(reply_cookie.model_dump(), status.HTTP_202_ACCEPTED)

    if reply_cookie:
        print(reply_cookie.model_dump())
        for k, v in reply_cookie:
            resp.set_cookie(k, v, domain='election.zapto.org', samesite="none")

    return resp


@router.post("/joinrequest/{pollid}")
async def join_poll(pollid: UUID, user_context: userContext):
    try:
        await user_context.join_poll(pollid)
    except ValueError:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="already registered")
    return JSONResponse(content={"status": f"joined poll {pollid}"})


@router.get("/getPolls")
async def get_polls(_admin_context: adminContext, _: userContext):
    views = []
    async for poll_view in _admin_context.get_poll_views():
        dumped = poll_view.model_dump()
        views.append(dumped)
    print(views)
    return views


@router.post("/castVote")
async def cast_vote(
        poll_id: Annotated[PollId, Form()],
        candidate_id: Annotated[PersonId, Form()],
        user_context: userContext,
        background_tasks: BackgroundTasks,
):
    try:
        await user_context.cast_vote(poll_id, candidate_id)
    except ReferenceError as re:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(re))
    except IntegrityError as ie:
        traceback.print_exc(limit=10)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie))
    recipient = user_context.user.email_id

    # body = "You have voted to a poll"
    # background_tasks.add_task(send_email, recipient, "casting a vote", body)

    return JSONResponse(content={"status": "voted successfully casted"}, status_code=HTTP_202_ACCEPTED)


@router.get("/poll/{poll_id}", name='poll')
async def get_poll(poll_id: PollId, user_context: userContext):
    poll_repo = PollRepository(AsyncDB(db_session_factory))
    poll_in_db = await poll_repo.read(poll_id)
    can_repo = CandidateRepository(AsyncDB(db_session_factory))

    candidates = await can_repo.get_candidates_in_election(poll_id)
    what = await user_context.check_join_status(poll_id)
    p = PollShareable(
        election_id=poll_in_db.election_id,
        title=poll_in_db.title,
        description=poll_in_db.description,
        start_date=poll_in_db.start_date,
        end_date=poll_in_db.end_date,
        validation_regex=poll_in_db.validation_regex,
        election_status=poll_in_db.election_status,
        candidates=[CandidateInPoll.model_validate(x) for x in candidates],
        is_joined=what,
    )
    return p
