from typing import Annotated

from fastapi.params import Depends

from core.models.person import Voter
from db.database import AsyncDB, db_session_factory
from repository.voter import VoterRepository
from utils import parses


class VoterContext:
    def __init__(self, voter: Voter, repository: VoterRepository):
        self.voter = voter
        self.repository = repository


async def get_voter_context(voter: Annotated[Voter, Depends(parses.parse_cookie)]):
    async_db = AsyncDB(db_session_factory)
    repository = VoterRepository(async_db)
    vc = VoterContext(voter,repository)
    return vc
