from typing import List
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session

from .depen import database,schemas,crud
SessionLocal =database.SessionLocal  

router = APIRouter()

Hall = crud.hall() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/halls/{hall_id}", response_model=schemas.Hall)
def read_hall(hall_id: int, db: Session = Depends(get_db)):
    db_hall = Hall.get_hall(db, hall_id=hall_id)
    if db_hall is None:
        raise HTTPException(status_code=404, detail="hall not found")
    return db_hall


@router.get("/halls/", response_model=List[schemas.Hall])
def read_halls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    halls = Hall.get_halls(db, skip=skip, limit=limit)
    return halls


@router.post("/halls/", response_model=schemas.Hall)
def create_hall(hall: schemas.HallCreate, db: Session = Depends(get_db)):
    return Hall.create_hall(db=db, hall=hall)



@router.put("/halls/{hall_id}", response_model=schemas.Hall)
def update_hall(hall_id: int, hall: schemas.HallCreate, db: Session = Depends(get_db)):
    db_hall = Hall.get_hall(db, hall_id=hall_id)
    if db_hall is None:
        raise HTTPException(status_code=404, detail="hall is not founded")
    return Hall.update_hall(db=db, hall_id=hall_id, hall=hall)


@router.delete("/halls/{hall_id}")
def delete_hall(hall_id: int, db: Session = Depends(get_db)):
    db_hall = Hall.get_hall(db,hall_id=hall_id)
    if db_hall is None:
        raise HTTPException(status_code=404, detail="hall is not founded")
    return Hall.delete_hall(db=db, hall_id=hall_id)    






