from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends

from ..models.person import Voter
from . import parses


class VoterContext:
    voter_id = None


async def get_voter_context(voter: Annotated[Voter, Depends(parses.parse_cookie)]):
    vc = VoterContext()
    vc.voter_id = voter
    return vc
