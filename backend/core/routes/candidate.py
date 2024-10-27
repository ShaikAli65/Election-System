from fastapi import APIRouter
from backend.core.models import PersonId, PollId
from backend.core.operations import db

router = APIRouter(
    prefix="/candidate",
    tags=["candidate",],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_candidate(poll_id: PollId, candidate_id: PersonId):
    candidate = db.get_candidate(candidate_id)
    return candidate

