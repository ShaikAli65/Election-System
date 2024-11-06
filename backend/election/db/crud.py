from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas import (AuditLogSchema, AuthenticationSchema, BallotSchema, CandidateSchema, ElectionSchema, ElectionResultSchema, VoterSchema)


async def get_authentication_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(AuthenticationSchema).filter_by(user_id=user_id))
    return result.scalars().first()


async def update_authentication(db: AsyncSession, user_id: str, auth_update):
    query = update(AuthenticationSchema).where(AuthenticationSchema.user_id == user_id).values(**auth_update.model_dump())
    await db.execute(query)
    await db.commit()
    return await get_authentication_by_id(db, user_id)


async def delete_authentication(db: AsyncSession, user_id: str):
    query = delete(AuthenticationSchema).where(AuthenticationSchema.user_id == user_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Authentication record deleted successfully"}


async def get_candidate_by_id(db: AsyncSession, candidate_id: str):
    result = await db.execute(select(CandidateSchema).filter_by(candidate_id=candidate_id))
    return result.scalars().first()


async def delete_candidate(db: AsyncSession, candidate_id: str):
    query = delete(CandidateSchema).where(CandidateSchema.candidate_id == candidate_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Candidate deleted successfully"}


async def get_voter_by_id(db: AsyncSession, voter_id: str):
    result = await db.execute(select(VoterSchema).filter_by(voter_id=voter_id))
    return result.scalars().first()



# Election CRUD operations
async def create_election(db: AsyncSession, election):
    new_election = ElectionSchema(**election.model_dump())
    db.add(new_election)
    await db.commit()
    await db.refresh(new_election)
    return new_election



# Ballot CRUD operations
async def create_ballot(db: AsyncSession, ballot):
    new_ballot = BallotSchema(**ballot.model_dump())
    db.add(new_ballot)
    await db.commit()
    await db.refresh(new_ballot)
    return new_ballot


async def get_ballot_by_id(db: AsyncSession, ballot_id: str):
    result = await db.execute(select(BallotSchema).filter_by(ballot_id=ballot_id))
    return result.scalars().first()



# Audit Log CRUD operations
async def create_audit_log(db: AsyncSession, audit_log):
    new_log = AuditLogSchema(**audit_log.model_dump())
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log


async def get_audit_log_by_id(db: AsyncSession, log_id: str):
    result = await db.execute(select(AuditLogSchema).filter_by(log_id=log_id))
    return result.scalars().first()


# Election Result CRUD operations
async def create_election_result(db: AsyncSession, result):
    new_result = ElectionResultSchema(**result.model_dump())
    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)
    return new_result


async def get_election_result_by_id(db: AsyncSession, result_id: str):
    result = await db.execute(select(ElectionResultSchema).filter_by(result_id=result_id))
    return result.scalars().first()


async def delete_election_result(db: AsyncSession, result_id: str):
    query = delete(ElectionResultSchema).where(ElectionResultSchema.result_id == result_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Election result deleted successfully"}
