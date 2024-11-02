from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field
from pydantic.v1 import FilePath

PersonId = str


class User(BaseModel, extra='allow'):
    """User Model"""
    user_id: UUID
    user_name: str
    email_id: EmailStr


class Voter(User):
    ...


class CandidateFromAdmin(BaseModel):
    """Candidate Model"""
    candidate_description: str
    email_id: EmailStr
    candidate_name: str
    candidate_name: UUID = Field(default_factory=uuid4)


class CandidateInPoll(BaseModel):
    candidate_id: UUID
    manifesto_file_path: FilePath
    election_id: UUID
    total_votes: int = 0
    nomination_date: datetime


class CandidateInDB(CandidateFromAdmin, CandidateInPoll):
    """"""


class UserLoggedInCookie(BaseModel):
    access_token: str

    def __iter__(self):
        return iter(self.model_dump().items())

    def __eq__(self, other):
        return self.access_token == other.access_token


class UserCredentials(BaseModel, extra='allow'):
    name: str
    email: EmailStr
    authorized_party: str = Field(alias='azp')
    user_id: UUID = Field(alias='sub')
    expires: int = Field(alias='exp')
    token: str = Field(alias='jti')
