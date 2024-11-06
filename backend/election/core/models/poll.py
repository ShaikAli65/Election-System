import uuid
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, FilePath

from election.core.models.user import CandidateParsed, PersonId as _PId
from election.db.schemas import ElectionStatusEnum

PollId = UUID
ResultId = str
PortFolioId = _PId


class PortFolio(BaseModel):
    portfolio_path: FilePath = None
    poll_id: PollId
    candidate_id: _PId


class CandidateInPoll(CandidateParsed):
    """this class structure defines how Candidate appeares inside a poll"""
    model_config = ConfigDict(from_attributes=True)


class PollResult(BaseModel):
    poll_id: PollId
    result_id: ResultId
    winner: CandidateInPoll
    total_votes: int


class PollMetaData(BaseModel):
    election_id: PollId = Field(default_factory=uuid.uuid4)
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    validation_regex: str


class Poll(PollMetaData):
    candidates: list[CandidateInPoll]


class PollInDb(PollMetaData):
    model_config = ConfigDict(from_attributes=True)

    election_status: str = ElectionStatusEnum.UPCOMING
    total_voters: int = 0
    total_candidates: int = 0


class PollShareable(Poll):
    """A poll that is sent to a normal user"""
    model_config = ConfigDict(from_attributes=True)

    election_status: str
    is_joined: bool


class PollView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    election_id: UUID
    title: str
    election_status: str
    start_date: datetime
    end_date: datetime


@dataclass(slots=True)
class BallotEntry:
    voter_id:UUID
    election_id:UUID
    candidate_id:UUID
    voting_time: datetime

