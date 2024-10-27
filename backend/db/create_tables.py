# create_tables.py
from .database import Base, engine
from .models import Voter, Candidate, Authentication, Admin, Election, Ballot, AuditLog, election_results, VoterEligibilityLog, Notification

# Create all tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print('Tables created Successfully...')
