from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models import (Authentication, Candidate, Voter, Election,
                    Ballot, Admin, AuditLog, VoterEligibilityLog,
                    Notification, ElectionResult)
from schemas import (AuthenticationCreate, AuthenticationUpdate,
                     CandidateCreate, CandidateUpdate,
                     VoterCreate, VoterUpdate,
                     ElectionCreate, ElectionUpdate,
                     BallotCreate, BallotUpdate,
                     AdminCreate, AdminUpdate,
                     AuditLogCreate, AuditLogUpdate,
                     VoterEligibilityLogCreate, VoterEligibilityLogUpdate,
                     NotificationCreate, NotificationUpdate,
                     ElectionResultCreate, ElectionResultUpdate)

# Authentication CRUD operations
async def create_authentication(db: AsyncSession, auth: AuthenticationCreate):
    new_auth = Authentication(**auth.model_dump())
    db.add(new_auth)
    await db.commit()
    await db.refresh(new_auth)
    return new_auth

async def get_authentication_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(Authentication).filter_by(user_id=user_id))
    return result.scalars().first()

async def update_authentication(db: AsyncSession, user_id: str, auth_update: AuthenticationUpdate):
    query = update(Authentication).where(Authentication.user_id == user_id).values(**auth_update.model_dump())
    await db.execute(query)
    await db.commit()
    return await get_authentication_by_id(db, user_id)

async def delete_authentication(db: AsyncSession, user_id: str):
    query = delete(Authentication).where(Authentication.user_id == user_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Authentication record deleted successfully"}

# Candidate CRUD operations
async def create_candidate(db: AsyncSession, candidate: CandidateCreate):
    new_candidate = Candidate(**candidate.model_dump())
    db.add(new_candidate)
    await db.commit()
    await db.refresh(new_candidate)
    return new_candidate

async def get_candidate_by_id(db: AsyncSession, candidate_id: str):
    result = await db.execute(select(Candidate).filter_by(candidate_id=candidate_id))
    return result.scalars().first()

async def update_candidate(db: AsyncSession, candidate_id: str, candidate_update: CandidateUpdate):
    query = update(Candidate).where(Candidate.candidate_id == candidate_id).values(**candidate_update.model_dump())
    await db.execute(query)
    await db.commit()
    return await get_candidate_by_id(db, candidate_id)

async def delete_candidate(db: AsyncSession, candidate_id: str):
    query = delete(Candidate).where(Candidate.candidate_id == candidate_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Candidate deleted successfully"}

# Voter CRUD operations
async def create_voter(db: AsyncSession, voter: VoterCreate):
    new_voter = Voter(**voter.model_dump())
    db.add(new_voter)
    await db.commit()
    await db.refresh(new_voter)
    return new_voter

async def get_voter_by_id(db: AsyncSession, voter_id: str):
    result = await db.execute(select(Voter).filter_by(voter_id=voter_id))
    return result.scalars().first()

async def update_voter(db: AsyncSession, voter_id: str, voter_update: VoterUpdate):
    query = update(Voter).where(Voter.voter_id == voter_id).values(**voter_update.model_dump())
    await db.execute(query)
    await db.commit()
    return await get_voter_by_id(db, voter_id)

async def delete_voter(db: AsyncSession, voter_id: str):
    query = delete(Voter).where(Voter.voter_id == voter_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Voter deleted successfully"}

# Election CRUD operations
async def create_election(db: AsyncSession, election: ElectionCreate):
    new_election = Election(**election.model_dump())
    db.add(new_election)
    await db.commit()
    await db.refresh(new_election)
    return new_election

async def get_election_by_id(db: AsyncSession, election_id: str):
    result = await db.execute(select(Election).filter_by(election_id=election_id))
    return result.scalars().first()

async def update_election(db: AsyncSession, election_id: str, election_update: ElectionUpdate):
    query = update(Election).where(Election.election_id == election_id).values(**election_update.model_dump())
    await db.execute(query)
    await db.commit()
    return await get_election_by_id(db, election_id)

async def delete_election(db: AsyncSession, election_id: str):
    query = delete(Election).where(Election.election_id == election_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Election deleted successfully"}

# Ballot CRUD operations
async def create_ballot(db: AsyncSession, ballot: BallotCreate):
    new_ballot = Ballot(**ballot.model_dump())
    db.add(new_ballot)
    await db.commit()
    await db.refresh(new_ballot)
    return new_ballot

async def get_ballot_by_id(db: AsyncSession, ballot_id: str):
    result = await db.execute(select(Ballot).filter_by(ballot_id=ballot_id))
    return result.scalars().first()

async def delete_ballot(db: AsyncSession, ballot_id: str):
    query = delete(Ballot).where(Ballot.ballot_id == ballot_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Ballot deleted successfully"}

# Admin CRUD operations
async def create_admin(db: AsyncSession, admin: AdminCreate):
    new_admin = Admin(**admin.model_dump())
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return new_admin

async def get_admin_by_id(db: AsyncSession, admin_id: str):
    result = await db.execute(select(Admin).filter_by(admin_id=admin_id))
    return result.scalars().first()

async def update_admin(db: AsyncSession, admin_id: str, admin_update: AdminUpdate):
    query = update(Admin).where(Admin.admin_id == admin_id).values(**admin_update.model_dump())
    await db.execute(query)
    await db.commit()
    return await get_admin_by_id(db, admin_id)

async def delete_admin(db: AsyncSession, admin_id: str):
    query = delete(Admin).where(Admin.admin_id == admin_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Admin deleted successfully"}

# Audit Log CRUD operations
async def create_audit_log(db: AsyncSession, audit_log: AuditLogCreate):
    new_log = AuditLog(**audit_log.model_dump())
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

async def get_audit_log_by_id(db: AsyncSession, log_id: str):
    result = await db.execute(select(AuditLog).filter_by(log_id=log_id))
    return result.scalars().first()

# Voter Eligibility Log CRUD operations
async def create_voter_eligibility_log(db: AsyncSession, log: VoterEligibilityLogCreate):
    new_log = VoterEligibilityLog(**log.model_dump())
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

# Notification CRUD operations
async def create_notification(db: AsyncSession, notification: NotificationCreate):
    new_notification = Notification(**notification.model_dump())
    db.add(new_notification)
    await db.commit()
    await db.refresh(new_notification)
    return new_notification

async def get_notification_by_id(db: AsyncSession, notification_id: str):
    result = await db.execute(select(Notification).filter_by(notification_id=notification_id))
    return result.scalars().first()

async def delete_notification(db: AsyncSession, notification_id: str):
    query = delete(Notification).where(Notification.notification_id == notification_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Notification deleted successfully"}

# Election Result CRUD operations
async def create_election_result(db: AsyncSession, result: ElectionResultCreate):
    new_result = ElectionResult(**result.model_dump())
    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)
    return new_result

async def get_election_result_by_id(db: AsyncSession, result_id: str):
    result = await db.execute(select(ElectionResult).filter_by(result_id=result_id))
    return result.scalars().first()

async def delete_election_result(db: AsyncSession, result_id: str):
    query = delete(ElectionResult).where(ElectionResult.result_id == result_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Election result deleted successfully"}
