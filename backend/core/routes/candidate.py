from fastapi import APIRouter
from backend.core.models import PersonId


router = APIRouter(
    prefix="/candidate",
    tags=["candidate",],
    responses={404: {"description": "Not found"}},
)


@router.get("/{candidate_id}")
async def get_candidate(candidate_id: PersonId):
    ...
