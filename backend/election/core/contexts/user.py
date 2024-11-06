from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

import sqlalchemy
from fastapi.params import Depends

from election.core.contexts.auth import Authenticator
from election.core.models.poll import BallotEntry
from election.core.models.user import User, VoterInDb
from election.db.database import AsyncDB, db_session_factory
from election.repository.ballot import BallotRepository
from election.repository.poll import PollRepository
from election.repository.user import UserRepository
from election.repository.voter import VoterRepository
from election.utils.useables import get_unique_id


class UserContext:
    def __init__(self, user: User, urepo: UserRepository, vrepo: VoterRepository):
        self.user = user
        self.urepository = urepo
        self.vrepository = vrepo

    def __repr__(self):
        return f"<UserContext({self.user}, {self.urepository})>"

    async def join_poll(self, poll_id: UUID):
        await self._check_authorization(poll_id)

        try:
            voter_in_db = VoterInDb(user_id=self.user.user_id, election_id=poll_id)
            await self.vrepository.create(voter_in_db)
        except sqlalchemy.exc.IntegrityError as e:
            raise ValueError() from e

    async def _check_authorization(self, poll_id):
        ...

    async def _check_duplicacy(self, poll_id):
        what = await self.vrepository.read((self.user.user_id, poll_id))
        if what is None:
            raise ReferenceError("no registered log found, rejecting request")
        if what.has_voted is True:
            raise ReferenceError("found voter entry as voted=True, cannot proceed")

    async def cast_vote(self, poll_id: UUID, candidate_id: UUID):
        await self._check_duplicacy(poll_id)
        await self._check_authorization(poll_id)

        ballot_repo = BallotRepository(self.urepository.database)
        e_repo = PollRepository(self.urepository.database)

        what = await ballot_repo.read((poll_id, self.user.user_id))
        if what:
            raise ReferenceError("found a ballot entry of user, cancelling request")

        b_entry = BallotEntry(self.user.user_id, poll_id, candidate_id, datetime.now())
        await ballot_repo.entry_vote(b_entry)

        await self.vrepository.mark_voted(self.user.user_id, poll_id)

        await e_repo.increment_total_voters(poll_id)

    async def check_join_status(self, poll_id):
        _t = await self.vrepository.read((self.user.user_id, poll_id))
        return _t is not None


async def get_user_context(authenticator: Authenticator):
    async_db = AsyncDB(db_session_factory)
    urepository = UserRepository(async_db)
    vrepository = VoterRepository(async_db)
    vc = UserContext(authenticator.user, urepository, vrepository)
    return vc


userContext = Annotated[UserContext, Depends(get_user_context)]
