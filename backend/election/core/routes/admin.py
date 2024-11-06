import logging
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.params import Depends

from election.core.contexts.admin import AdminContext, adminContext, get_admin_context
from election.core.models.poll import CandidateInPoll, Poll, PollId, PollShareableView
from election.db.database import AsyncDB, db_session_factory
from election.db.statemanager import add_new_timed_trigger
from election.repository.candidate import CandidateRepository
from election.repository.poll import PollRepository
from election.utils.parses import parse_poll

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

router = APIRouter(
    prefix="/admin",
    tags=["admin", ],
    responses={404: {"description": "Not found"}},
)


@router.get("/polls/{poll_id}")
async def get_poll(poll_id: PollId):
    poll_repo = PollRepository(AsyncDB(db_session_factory))
    poll_in_db = await poll_repo.read(poll_id)
    can_repo = CandidateRepository(AsyncDB(db_session_factory))

    candidates = await can_repo.get_candidates_in_election(poll_id)
    p = PollShareableView(
        election_id=poll_in_db.election_id,
        title=poll_in_db.title,
        description=poll_in_db.description,
        start_date=poll_in_db.start_date,
        end_date=poll_in_db.end_date,
        validation_regex=poll_in_db.validation_regex,
        election_status=poll_in_db.election_status,
        candidates=[CandidateInPoll.model_validate(x) for x in candidates],
    )
    return p


@router.post("/createPoll")
async def create_poll(poll: Poll = Depends(parse_poll), _admin_context: AdminContext = Depends(get_admin_context)) -> UUID:
    """
    :param _admin_context:
    :param poll:
    :return:
    """
    # print(poll.model_dump())
    await _admin_context.create_poll(poll)
    await add_new_timed_trigger(poll, _admin_context)
    print(poll)
    return poll.election_id


@router.post("/updatePoll")
async def update_poll(poll: Request):
    form = await poll.form()
    print(form)


@router.get("/getPolls")
async def get_polls(_admin_context: adminContext):
    views = []
    async for poll_view in _admin_context.get_poll_views():
        dumped = poll_view.model_dump()
        views.append(dumped)
    print(views)
    return views


@router.delete("/deletePoll")
async def delete_poll():
    ...
