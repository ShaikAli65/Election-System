from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field

PersonId = str


class User(BaseModel, extra='allow'):
    """User Model"""
    user_id: UUID
    user_name: str
    email_id: EmailStr


class VoterInDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    has_voted:bool = False
    election_id: UUID


class CandidateFromAdmin(BaseModel):
    """Candidate Model"""
    candidate_id: UUID = Field(default_factory=uuid4)
    word_from_candidate: str = ""
    email_id: EmailStr = "q@a.com"
    candidate_name: str = ""


class CandidateParsed(CandidateFromAdmin):
    manifesto_file_path: str = ""
    total_votes: int = 0
    nomination_date: datetime = Field(default_factory=datetime.now)
    election_id: UUID = None


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
    user_id: str = Field(alias='sub')
    expires: int = Field(alias='exp')
    token: str = Field(alias='jti')
