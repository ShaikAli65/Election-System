# models.py
from sqlalchemy import Column, String, Boolean, Text, Integer, TIMESTAMP, UUID, Enum, ForeignKey, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from .database import Base


class Voter(Base):
    __tablename__ = "voters"

    voter_id = Column(PGUUID(as_uuid=True), primary_key=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), unique=True, nullable=False)
    voter_registration_number = Column(String(100), unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(Text, nullable=False)
    phone_number = Column(String(20), unique=True)
    has_voted = Column(Boolean, default=False)
    voting_time = Column(TIMESTAMP)
    election_id = Column(PGUUID(as_uuid=True))
    is_eligible = Column(Boolean, default=True)
    registration_date = Column(TIMESTAMP, server_default=func.now())
    voting_district = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id = Column(PGUUID(as_uuid=True), primary_key=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), unique=True, nullable=False)
    election_id = Column(PGUUID(as_uuid=True), nullable=False)
    party_name = Column(String(100))
    manifesto = Column(Text)
    manifesto_file_path = Column(String(255))
    total_votes = Column(Integer, default=0)
    constituency = Column(String(100))
    nomination_date = Column(TIMESTAMP, server_default=func.now())
    is_approved = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class UserRoleEnum(str, Enum):
    VOTER = "voter"
    CANDIDATE = "candidate"
    ADMIN = "admin"


class AccountStatusEnum(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class Authentication(Base):
    __tablename__ = "authentication"

    user_id = Column(PGUUID(as_uuid=True), primary_key=True)  # UUID type for primary key
    user_name = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(32), nullable=False)
    user_role = Column(Enum(UserRoleEnum), nullable=False)  # Enum for user role
    account_status = Column(Enum(AccountStatusEnum), nullable=False)  # Enum for account status
    email_id = Column(String(255), unique=True, nullable=False)
    last_login = Column(TIMESTAMP)
    account_creation_time = Column(TIMESTAMP, server_default=func.now())
    session_token = Column(String(255))
    session_expiration_time = Column(TIMESTAMP)


class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(PGUUID(as_uuid=True), primary_key=True)  # UUID type for primary key
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), unique=True, nullable=False)
    role = Column(String(100), nullable=False)  # Role or level of the admin
    permissions = Column(Text)  # JSON or text defining admin permissions
    assigned_elections = Column(ARRAY(PGUUID(as_uuid=True)))  # Array of UUIDs for elections
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class ElectionStatusEnum(str, Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class Election(Base):
    __tablename__ = "elections"

    election_id = Column(PGUUID(as_uuid=True), primary_key=True)
    election_name = Column(String(255), nullable=False)
    election_type = Column(String(100))
    election_start_date = Column(TIMESTAMP, nullable=False)
    election_end_date = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
    total_voters = Column(Integer, default=0)
    total_candidates = Column(Integer, default=0)
    election_status = Column(Enum(ElectionStatusEnum), default="upcoming", nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Ballot(Base):
    __tablename__ = "ballots"

    ballot_id = Column(PGUUID(as_uuid=True), primary_key=True)
    voter_id = Column(PGUUID(as_uuid=True), ForeignKey("voters.voter_id"), nullable=False)
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id"), nullable=False)
    candidate_id = Column(PGUUID(as_uuid=True), ForeignKey("candidates.candidate_id"), nullable=False)
    voting_time = Column(TIMESTAMP, server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_log"

    log_id = Column(PGUUID(as_uuid=True), primary_key=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), nullable=False)
    action = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    details = Column(Text)  # Optional field for additional details


class resultStatusEnum(str, Enum):
    winner = "winner"
    loser = "loser"
    tie = "tie"


class election_results(Base):
    result_id = Column(PGUUID(as_uuid=True), primary_key=True)
    election_id = Column(PGUUID(as_uuid=True), nullable=False)
    candidate_id = Column(PGUUID(as_uuid=True), nullable=False)
    total_votes = Column(Integer, default=0)
    result_status = Column(Enum(resultStatusEnum))


class VoterEligibilityLog(Base):
    __tablename__ = "voter_eligibility_log"

    log_id = Column(PGUUID(as_uuid=True), primary_key=True)
    voter_id = Column(PGUUID(as_uuid=True), ForeignKey("voters.voter_id"), nullable=False)
    changed_by = Column(PGUUID(as_uuid=True), ForeignKey("admin.admin_id"))
    is_eligible = Column(Boolean, nullable=False)
    change_reason = Column(Text)
    change_time = Column(TIMESTAMP, server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(PGUUID(as_uuid=True), primary_key=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, server_default=func.now())
    read_status = Column(Boolean, default=False)
