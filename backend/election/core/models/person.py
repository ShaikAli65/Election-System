from pydantic import BaseModel, ConfigDict, EmailStr, Field

PersonId = str


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


class UserLoggedInCookie(BaseModel):
    voter_id: str

    def __iter__(self):
        return iter(('voter_id', self.voter_id))


class VoterSignedUp:
    ...


class UserCredentials(BaseModel):
    model_config = ConfigDict(extra='allow')

    name: str
    email: EmailStr
    aud: str = Field(pattern=r'^\d+-[a-z0-9]+-[a-z0-9]+\.apps\.googleusercontent\.com$')
    user_id: str = Field(alias='sub')
    expires: int = Field(alias='exp')
    token: str = Field(alias='jti')
