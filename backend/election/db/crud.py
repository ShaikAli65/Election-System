# crud.py
from sqlalchemy import Date
from sqlalchemy.orm import Session
from .models import Voter, Candidate
from uuid import UUID


# Create a new voter
def create_voter(db: Session, voter_id: UUID, user_id: UUID, voter_registration_number: str, first_name: str,
                 last_name: str, date_of_birth: str, address: str, phone_number: str):
    new_voter = Voter(
        voter_id=voter_id,
        user_id=user_id,
        voter_registration_number=voter_registration_number,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        address=address,
        phone_number=phone_number
    )
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return new_voter


# Read: Get a voter by voter_id
def get_voter_by_id(db: Session, voter_id: UUID):
    return db.query(Voter).filter(Voter.voter_id == voter_id).first()


# Read: Get all voters
def get_all_voters(db: Session):
    return db.query(Voter).all()


# Update: Update a voter's information
def update_voter(db: Session, voter_id: UUID, **kwargs):
    voter = get_voter_by_id(db, voter_id)
    if voter:
        for key, value in kwargs.items():
            setattr(voter, key, value)
        db.commit()
        db.refresh(voter)
    return voter


# Delete: Remove a voter from the database
def delete_voter(db: Session, voter_id: UUID):
    voter = get_voter_by_id(db, voter_id)
    if voter:
        db.delete(voter)
        db.commit()
    return voter
