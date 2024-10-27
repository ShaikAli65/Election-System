# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .crud import get_voter_by_id

app = FastAPI()

@app.get("/voters/{voter_id}")
def read_voter(voter_id: str, db: Session = Depends(get_db)):
    voter = get_voter_by_id(db, voter_id)
    if not voter:
        raise HTTPException(status_code=404, detail="Voter not found")
    return voter
