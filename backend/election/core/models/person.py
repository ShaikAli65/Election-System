from pydantic import BaseModel, EmailStr, Field

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


class UserLoginForm(BaseModel):
    username: str
    password: str


class UserLoggedInCookie(BaseModel):
    voter_id: str

    def __iter__(self):
        return iter(('voter_id', self.voter_id))


class VoterSignedUp:
    ...
