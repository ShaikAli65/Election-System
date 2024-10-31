import enum

from pydantic import BaseModel, FilePath, FutureDate

from .person import PersonId as _PId


PollId = str
ResultId = str
PortFolioId = _PId


class PortFolio(BaseModel):
    portfolio_path: FilePath = None
    poll_id: PollId
    candidate_id: _PId


class CandidateInPoll(BaseModel):
    candidate_id: _PId
    portfolio: PortFolio = None
    vote_count: int = 0


class PollStatus(enum.Enum):
    """
    POLL STATUS CODES:
    SCHEDULED: 0
    ACTIVE: 1
    EXPIRED: 3
    CANCELLED: 4
    """
    SCHEDULED = 0
    ACTIVE = 1
    EXPIRED = 3
    CANCELLED = 4


class PollResult(BaseModel):
    poll_id: PollId
    result_id: ResultId
    winner: CandidateInPoll
    total_votes: int


class Poll(BaseModel):
    poll_id: PollId = None
    title: str
    type: str
    start_date: FutureDate
    end_date: FutureDate
    candidates: list[CandidateInPoll]
    validation_regex: str


class PollInDb(Poll):
    status: PollStatus = PollStatus.SCHEDULED
    result: PollResult = None
