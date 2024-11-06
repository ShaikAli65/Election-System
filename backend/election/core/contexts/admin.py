from collections import Counter
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from election.core.models.poll import CandidateInPoll, Poll, PollInDb, PollView
from election.db.database import AsyncDB, DictDB, db_session_factory
from election.db.schemas import CandidateSchema, ElectionResultSchema, ElectionSchema
from election.repository.auth import AuthRepository
from election.repository.ballot import BallotRepository
from election.repository.candidate import CandidateRepository
from election.repository.poll import PollRepository
from election.repository.result import ResultRepository
from election.repository.user import UserRepository
from election.repository.voter import VoterRepository
from election.utils.useables import get_unique_id


class AdminContext:

    def __init__(self, auth, voter, user, candidate, poll, ballot_repo, result_repo):
        self.auth_repo: AuthRepository = auth
        self.voter_repo: VoterRepository = voter
        self.user_repo: UserRepository = user
        self.candidate_repo: CandidateRepository = candidate
        self.poll_repo: PollRepository = poll
        self.ballot_repo: BallotRepository = ballot_repo
        self.result_repo: ResultRepository = result_repo

    async def add_candidate(self, candidate: CandidateInPoll):
        dumped_can = candidate.model_dump()
        schemed_can = CandidateSchema(**dumped_can)
        await self.candidate_repo.create(schemed_can)

    async def get_poll_views(self):
        view = ['election_id', 'title', 'election_status', 'start_date', 'end_date']
        async with self.candidate_repo.database() as db:
            db: AsyncSession
            stmt = select(
                ElectionSchema.election_id,
                ElectionSchema.title,
                ElectionSchema.election_status,
                ElectionSchema.start_date,
                ElectionSchema.end_date,
            )
            results = await db.execute(stmt)
            for result in results:
                data = {v: r for v, r in zip(view, result)}
                poll_view = PollView.model_validate(data)
                yield poll_view

    async def create_poll(self, poll: Poll):
        poll_in_db = PollInDb(**poll.model_dump(exclude={'candidates'}))
        schemed_election = ElectionSchema(
            **poll_in_db.model_dump(exclude={'total_candidates', }),
            total_candidates=len(poll.candidates),
        )

        await self.poll_repo.create(schemed_election)
        for candidate in poll.candidates:
            await self.add_candidate(candidate)

    async def prepare_results(self, election_id):
        """
        Prepare and store election results by tallying votes for each candidate.
        :param election_id: The ID of the election to process.
        :return: None
        """
        try:
            # Retrieve all votes in the election
            election_rows = await self.ballot_repo.read_election(election_id)
            candidates_in_election = await self.candidate_repo.get_candidates_in_election(election_id)

            # Initialize the vote count per candidate using a Counter
            candidate_vote_counts = Counter(election_row.candidate_id for election_row in election_rows)

            # Prepare result entries and update total votes for each candidate
            async with self.candidate_repo.database() as async_database:
                async_database: AsyncSession
                for candidate in candidates_in_election:
                    total_votes = candidate_vote_counts.get(candidate.candidate_id, 0)

                    # Create the result entry
                    result_entry = ElectionResultSchema(
                        result_id=get_unique_id(),
                        election_id=election_id,
                        candidate_id=candidate.candidate_id,
                        total_votes=total_votes,
                    )
                    await self.result_repo.create(result_entry)

                    # Update candidate's total votes in the database
                    stmt = (
                        update(CandidateSchema)
                        .where(CandidateSchema.candidate_id == candidate.candidate_id)
                        .values(total_votes=total_votes)
                        .execution_options(synchronize_session="fetch")
                    )
                    await async_database.execute(stmt)
                await async_database.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    async def create_time_graph_result(self, poll_id):

        pass

    async def get_results(self, poll_id):
        result_rows = await self.result_repo.read(poll_id)
        for result in result_rows:
            yield result


_admin: AdminContext | None = None


def admin_init():
    global _admin
    async_db = AsyncDB(db_session_factory)
    auth = AuthRepository(DictDB())
    voter = VoterRepository(async_db)
    poll = PollRepository(async_db)
    user = UserRepository(async_db)
    candidate = CandidateRepository(async_db)
    ballot = BallotRepository(async_db)
    result = ResultRepository(async_db)

    repos = auth, voter, user, candidate, poll, ballot, result
    _admin = AdminContext(*repos)


def get_admin_context() -> AdminContext:
    global _admin
    return _admin


adminContext = Annotated[AdminContext, Depends(get_admin_context)]
