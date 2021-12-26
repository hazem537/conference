from typing import List
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session

from .depen import database,schemas,crud

SessionLocal =database.SessionLocal  

router = APIRouter()
Ses = crud.session()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sessions/{session_id}", response_model=schemas.Session)
def read_session(session_id: int, db: Session = Depends(get_db)):
    db_session = Ses.get_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="session not found")
    return db_session


@router.get("/sessions/", response_model=List[schemas.Session])
def read_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sessions = Ses.get_sessions(db, skip=skip, limit=limit)
    return sessions

@router.post("/sessions/", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    return Ses.create_session(db=db, session=session)

@router.put("/sessions/{session_id}", response_model=schemas.Session)
def update_session(session_id: int, session: schemas.SessionCreate, db: Session = Depends(get_db)):
    db_session = Ses.get_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="session is not founded")
    return Ses.update_session(db=db, session_id=session_id, session=session)

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    db_session = Ses.get_session(db,session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="session is not founded")
    return Ses.delete_session(db=db, session_id=session_id)    




