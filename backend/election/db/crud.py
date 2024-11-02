from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas import (AuditLog, Authentication, Ballot, Candidate, Election, ElectionResult, Voter)


# Authentication CRUD operations
async def create_authentication(db: AsyncSession, auth):
    new_auth = Authentication(**auth.model_dump())
    db.add(new_auth)
    await db.commit()
    await db.refresh(new_auth)
    return new_auth


async def get_authentication_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(Authentication).filter_by(user_id=user_id))
    return result.scalars().first()


async def update_authentication(db: AsyncSession, user_id: str, auth_update):
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
async def create_candidate(db: AsyncSession, candidate):
    new_candidate = Candidate(**candidate.model_dump())
    db.add(new_candidate)
    await db.commit()
    await db.refresh(new_candidate)
    return new_candidate


async def get_candidate_by_id(db: AsyncSession, candidate_id: str):
    result = await db.execute(select(Candidate).filter_by(candidate_id=candidate_id))
    return result.scalars().first()


async def update_candidate(db: AsyncSession, candidate_id: str, candidate_update):
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
async def create_voter(db: AsyncSession, voter):
    new_voter = Voter(**voter.model_dump())
    db.add(new_voter)
    await db.commit()
    await db.refresh(new_voter)
    return new_voter


async def get_voter_by_id(db: AsyncSession, voter_id: str):
    result = await db.execute(select(Voter).filter_by(voter_id=voter_id))
    return result.scalars().first()


async def update_voter(db: AsyncSession, voter_id: str, voter_update):
    query = update(Voter).where(Voter.user_id == voter_id).values(**voter_update.model_dump())
    await db.execute(query)
    await db.commit()
    return await get_voter_by_id(db, voter_id)


async def delete_voter(db: AsyncSession, voter_id: str):
    query = delete(Voter).where(Voter.user_id == voter_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Voter deleted successfully"}


# Election CRUD operations
async def create_election(db: AsyncSession, election):
    new_election = Election(**election.model_dump())
    db.add(new_election)
    await db.commit()
    await db.refresh(new_election)
    return new_election


async def get_election_by_id(db: AsyncSession, election_id: str):
    result = await db.execute(select(Election).filter_by(election_id=election_id))
    return result.scalars().first()


async def update_election(db: AsyncSession, election_id: str, election_update):
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
async def create_ballot(db: AsyncSession, ballot):
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


# Audit Log CRUD operations
async def create_audit_log(db: AsyncSession, audit_log):
    new_log = AuditLog(**audit_log.model_dump())
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log


async def get_audit_log_by_id(db: AsyncSession, log_id: str):
    result = await db.execute(select(AuditLog).filter_by(log_id=log_id))
    return result.scalars().first()


# Election Result CRUD operations
async def create_election_result(db: AsyncSession, result):
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
