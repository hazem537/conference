from typing import List
import shutil
from fastapi import Depends,  HTTPException, APIRouter,UploadFile,File
from sqlalchemy.orm import Session

from .depen import database,schemas,crud

SessionLocal =database.SessionLocal  

router = APIRouter()

Doctor = crud.doctor()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/doctors/{doctor_id}", response_model=schemas.Doctor)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = Doctor.get_doctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return db_doctor


@router.get("/doctors/", response_model=List[schemas.Doctor])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = Doctor.get_doctors(db, skip=skip, limit=limit)
    return doctors


@router.get("/doctorsByName/", response_model=schemas.Doctor)
def read_doctor_name(doctor_name: str = "", db: Session = Depends(get_db)):
    db_doctor =Doctor.get_doctor_by_name(db, name=doctor_name)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor



@router.post("/doctors/", response_model=schemas.Doctor)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor =Doctor.get_doctor_by_name(db, name=doctor.name)
    if db_doctor:
        raise HTTPException(status_code=400, detail="Doctor already registered")
    return Doctor.create_doctor(db=db, doctor=doctor)


@router.put("/doctors/{doctor_id}", response_model=schemas.Doctor)
def update_doctor(
    doctor_id: int, doctor: schemas.DoctorCreate, db: Session = Depends(get_db)
):
    db_doctor =Doctor.get_doctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor is not founded")
    return Doctor.update_doctor(db=db, doctor_id=doctor_id, doctor=doctor)


@router.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor =Doctor.get_doctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor is not founded")
    return Doctor.delete_doctor(db=db, doctor_id=doctor_id)

@router.post("/doctor/upload-file/")
def create_upload_file(file: UploadFile = File(...)):
    with open(f'filles/{file.filename}','wb') as buffer:
       shutil.copyfileobj(file.file,buffer)
    return{"filename":"is good"}   
    

   

