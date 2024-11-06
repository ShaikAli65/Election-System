# schemas.py

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import ENUM, UUID as PGUUID
from sqlalchemy.sql import func

from .database import Base


class VoterSchema(Base):
    __tablename__ = "voters"

    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), primary_key=True,)
    has_voted = Column(Boolean, default=False)
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id"), primary_key=True)


class CandidateSchema(Base):

    __tablename__ = "candidates"

    candidate_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), primary_key=True)
    word_from_candidate = Column(Text)
    manifesto_file_path = Column(String(255))
    total_votes = Column(Integer, default=0)
    nomination_date = Column(TIMESTAMP, server_default=func.now())
    email_id = Column(Text)
    candidate_name = Column(String(255))
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id"), nullable=False)

    def __repr__(self):
        return f"<CandidateSchema(cid={self.candidate_id}, cname={self.candidate_name}, eid={self.election_id})>"
    # election = relationship('Election', back_populates='candidates')


class AccountStatusEnum(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class AuthenticationSchema(Base):
    __tablename__ = "authentication"

    user_id = Column(PGUUID(as_uuid=True), primary_key=True)  # UUID type for primary key
    user_name = Column(String(255), unique=True, nullable=False)
    email_id = Column(String(255), unique=True, nullable=False)


class ElectionStatusEnum(str, Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class BallotSchema(Base):
    __tablename__ = "ballots"

    voter_id = Column(PGUUID(as_uuid=True), ForeignKey("voters.user_id"), nullable=False, primary_key=True)
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id"), nullable=False, primary_key=True)
    candidate_id = Column(PGUUID(as_uuid=True), ForeignKey("candidates.candidate_id"), nullable=False)
    voting_time = Column(TIMESTAMP, server_default=func.now())

    def __str__(self):
        return f"<BallotSchema(eid={self.election_id}, cid={self.candidate_id}, vid={self.voter_id}, t={self.voting_time})>"


class ElectionSchema(Base):
    __tablename__ = "elections"
    election_id = Column(PGUUID(as_uuid=True), primary_key=True)
    title = Column(String(255), nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    total_voters = Column(Integer, default=0)
    total_candidates = Column(Integer, default=0)
    election_status = Column(ENUM(ElectionStatusEnum.UPCOMING, ElectionStatusEnum.ONGOING, ElectionStatusEnum.COMPLETED, name='election_status'), default=ElectionStatusEnum.UPCOMING, nullable=False)
    description = Column(String(1024), nullable=False)
    validation_regex = Column(String(255))



class AuditLogSchema(Base):
    __tablename__ = "audit_log"

    log_id = Column(PGUUID(as_uuid=True), primary_key=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("authentication.user_id"), nullable=False)
    action = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    details = Column(Text)  # Optional field for additional details


class ElectionResultSchema(Base):
    __tablename__ = "election_results"

    result_id = Column(PGUUID(as_uuid=True), primary_key=True)
    election_id = Column(PGUUID(as_uuid=True), ForeignKey("elections.election_id"), nullable=False)
    candidate_id = Column(PGUUID(as_uuid=True), ForeignKey("candidates.candidate_id"), nullable=False)
    total_votes = Column(Integer, default=0)
