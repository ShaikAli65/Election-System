import enum

from pydantic import BaseModel, EmailStr, FilePath, FutureDate

PollId = str
ResultId = str
PersonId = str
PortFolioId = PersonId


class Person(BaseModel):
    id: PersonId
    name: str
    email: EmailStr
    age: int
    gender: str


class Admin(Person):
    """Admin Model"""


class Voter(Person):
    """Voter Model"""


class Candidate(Person):
    """Candidate Model"""
    port_folio: FilePath
    poll_id: PollId
    vote_count: int


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


class PortFolio:
    ...


class PollResult(BaseModel):
    poll_id: PollId
    result_id: ResultId
    winner: Candidate
    total_votes: int


class Poll(BaseModel):
    id: PollId
    title: str
    type: str
    start_date: FutureDate
    end_date: FutureDate
    status: PollStatus = PollStatus.SCHEDULED
    result: PollResult = None
    candidates: list[Candidate]
