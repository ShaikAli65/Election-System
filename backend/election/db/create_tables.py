# create_tables.py
from .database import Base, _engine
from .models import Voter, Candidate, Authentication, Election, Ballot, AuditLog, ElectionResult # Create all tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=_engine)
    print('Tables created Successfully...')
