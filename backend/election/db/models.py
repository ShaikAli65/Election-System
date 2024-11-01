# models.py
from sqlalchemy import Column, String, Boolean, Text, Integer, TIMESTAMP, UUID, Enum, ForeignKey, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from .database import Base


class Voter(Base):
    __tablename__ = "voters"

    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"),primary_key = True, unique=True, nullable=False)
    has_voted = Column(Boolean, default=False)
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id"))


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id = Column(PGUUID(as_uuid=True),ForeignKey("authentication.user_id") ,primary_key=True)
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id") ,nullable=False)
    candidate_description = Column(Text)
    manifesto_file_path = Column(String(255))
    total_votes = Column(Integer, default=0)
    nomination_date = Column(TIMESTAMP, server_default=func.now())



class AccountStatusEnum(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class Authentication(Base):
    __tablename__ = "authentication"

    user_id = Column(PGUUID(as_uuid=True), primary_key=True)  # UUID type for primary key
    user_name = Column(String(255), unique=True, nullable=False)
    email_id = Column(String(255), unique=True, nullable=False)


class ElectionStatusEnum(str, Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class Ballot(Base):
    __tablename__ = "ballots"

    ballot_id = Column(PGUUID(as_uuid=True), primary_key=True)
    voter_id = Column(PGUUID(as_uuid=True), ForeignKey("voters.user_id"), nullable=False)
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id"), nullable=False)
    candidate_id = Column(PGUUID(as_uuid=True), ForeignKey("candidates.candidate_id"), nullable=False)
    voting_time = Column(TIMESTAMP, server_default=func.now())


class Election(Base):
    __tablename__ = "elections"

    election_id = Column(PGUUID(as_uuid=True), primary_key=True)
    election_name = Column(String(255), nullable=False)
    election_start_date = Column(TIMESTAMP, nullable=False)
    election_end_date = Column(TIMESTAMP, nullable=False)
    total_voters = Column(Integer, default=0)
    total_candidates = Column(Integer, default=0)
    election_status = Column(Enum(ElectionStatusEnum), default="upcoming", nullable=False)




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


class ElectionResult(Base):
    result_id = Column(PGUUID(as_uuid=True), primary_key=True)
    election_id = Column(PGUUID(as_uuid=True),ForeignKey("elections.election_id"), nullable=False)
    candidate_id = Column(PGUUID(as_uuid=True),ForeignKey("candidates.candidate_id"), nullable=False)
    total_votes = Column(Integer, default=0)
    result_status = Column(Enum(resultStatusEnum))

