"""
Pydantic models:
Used throughout the modules
make sure to not include any other modules outside this directory
Look into db.schemas for sqlalchemy schemas
"""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, List


# Base Schema
class BaseSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


# Authentication Schemas
class AuthenticationBase(BaseSchema):
    user_name: str
    email_id: EmailStr
    user_role: str
    account_status: str


class AuthenticationCreate(AuthenticationBase):
    password_hash: str
    salt: str


class AuthenticationUpdate(BaseSchema):
    user_name: Optional[str] = None
    email_id: Optional[EmailStr] = None
    user_role: Optional[str] = None
    account_status: Optional[str] = None


# Candidate Schemas
class CandidateBase(BaseSchema):
    user_id: UUID
    election_id: UUID
    party_name: str
    manifesto: str
    constituency: str
    is_approved: bool


class CandidateCreate(CandidateBase):
    nomination_date: datetime


class CandidateUpdate(BaseSchema):
    party_name: Optional[str] = None
    manifesto: Optional[str] = None
    constituency: Optional[str] = None
    is_approved: Optional[bool] = None


# Voter Schemas
class VoterBase(BaseSchema):
    user_id: UUID
    voter_registration_number: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    phone_number: str
    has_voted: bool
    is_eligible: bool
    voting_district: str


class VoterCreate(VoterBase):
    pass  # All fields are required for creating a voter


class VoterUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    has_voted: Optional[bool] = None
    is_eligible: Optional[bool] = None


# Election Schemas
class ElectionBase(BaseSchema):
    election_name: str
    election_type: str
    election_start_date: datetime
    election_end_date: datetime
    is_active: bool
    total_voters: int
    total_candidates: int
    election_status: str


class ElectionCreate(ElectionBase):
    pass  # All fields are required for creating an election


class ElectionUpdate(BaseSchema):
    election_name: Optional[str] = None
    election_type: Optional[str] = None
    election_start_date: Optional[datetime] = None
    election_end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


# Ballot Schemas
class BallotBase(BaseModel):
    voter_id: UUID
    election_id: UUID
    candidate_id: UUID
    voting_time: datetime


class BallotCreate(BallotBase):
    pass  # All fields are required for creating a ballot


class BallotUpdate(BaseModel):
    candidate_id: Optional[UUID] = None


# Admin Schemas
class AdminBase(BaseSchema):
    user_id: UUID
    role: str
    permissions: str
    assigned_elections: List[UUID]


class AdminCreate(AdminBase):
    pass  # All fields are required for creating an admin


class AdminUpdate(BaseSchema):
    role: Optional[str] = None
    permissions: Optional[str] = None
    assigned_elections: Optional[List[UUID]] = None


# Audit Log Schemas
class AuditLogBase(BaseSchema):
    user_id: UUID
    action: str
    details: str


class AuditLogCreate(AuditLogBase):
    pass


# Voter Eligibility Log Schemas
class VoterEligibilityLogBase(BaseModel):
    voter_id: UUID
    changed_by: UUID
    is_eligible: bool
    change_reason: str


class VoterEligibilityLogCreate(VoterEligibilityLogBase):
    pass


# Election Result Schemas
class ElectionResultBase(BaseModel):
    election_id: UUID
    candidate_id: UUID
    votes: int


class ElectionResultCreate(ElectionResultBase):
    pass
