import enum

from pydantic import BaseModel, EmailStr, Field, FilePath, FutureDate

PollId = str
ResultId = str
PersonId = str
PortFolioId = PersonId


class Person(BaseModel):
    id: PersonId = Field(..., pattern=r"^[a-fA-F0-9\-]+$")
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


class PortFolio(BaseModel):
    portfolio_path: FilePath = None
    poll_id: PollId
    candidate_id: PersonId


class CandidateInPoll(BaseModel):
    candidate_id: PersonId
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


class PollInDb(Poll):
    status: PollStatus = PollStatus.SCHEDULED
    result: PollResult = None


class UserLoginForm(BaseModel):
    username: str
    password: str
