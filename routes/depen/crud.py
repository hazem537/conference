from fastapi.datastructures import UploadFile
from sqlalchemy.orm import Session

from . import models,schemas
import os
import shutil
#"C:/AoConferance/file_tree"
parent="C:/AoConferance/file_tree"
# doctor

class doctor():

    def get_doctor(self,db: Session, doctor_id: int):
      return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


    def get_doctor_by_name(self,db: Session, name: str):
      return db.query(models.Doctor).filter(models.Doctor.name == name).first()  


    def get_doctors(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Doctor).offset(skip).limit(limit).all()

        

    def create_doctor(self,db: Session, doctor: schemas.DoctorCreate):
        nsession = session()
        asession = nsession.get_session(db,doctor.session_id)
        nhall=hall()
        ahall=nhall.get_hall(db,asession.hall_id)
        path=os.path.join(parent,ahall.name,asession.name,doctor.name)
        os.mkdir(path)
        db_doctor =models.Doctor(name= doctor.name , path = path ,file=doctor.file , subject = doctor.subject ,session_id= doctor.session_id )
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor

    def update_doctor(self,db: Session, doctor_id: int, doctor: schemas.DoctorCreate):
        db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if db_doctor:
            db_doctor.name = doctor.name
            db_doctor.file_path = doctor.file_path
            db.commit()
            db.refresh(db_doctor)
        return db_doctor


    def delete_doctor(self,db: Session, doctor_id: int):
       
        db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        nsession = session()
        asession = nsession.get_session(db,db_doctor.session_id)
        nhall=hall()
        ahall=nhall.get_hall(db,asession.hall_id)
        path=os.path.join(parent,ahall.name,asession.name,db_doctor.name)
        shutil.rmtree(path)
        if db_doctor:
            db.delete(db_doctor)
            db.commit()
        return None
 
#session

class session():

    def get_session(self,db: Session, session_id: int):
        return db.query(models.Session).filter(models.Session.id == session_id).first()

    def get_session_by_name(self,db: Session, name: str):
        return db.query(models.Session).filter(models.Session.name == name).first()    

    def get_sessions(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Session).offset(skip).limit(limit).all()

    def create_session(self,db: Session, session: schemas.SessionCreate):
        nhall=hall()
        ahall=nhall.get_hall(db,session.hall_id)
        path=os.path.join(parent,ahall.name,session.name)
        os.mkdir(path)
        db_session = models.Session(name=session.name, time=session.time, hall_id=session.hall_id)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    def update_session(self,db: Session, session_id: int, session: schemas.SessionCreate):
        db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
        if db_session:
            db_session.name = session.name
            db_session.time = session.time
            db.commit()
            db.refresh(db_session)
        return db_session  

    def delete_session(self,db: Session, session_id: int):
        db_session = (db.query(models.Session).filter(models.Session.id == session_id).first() )
        nhall=hall()
        ahall=nhall.get_hall(db,db_session.hall_id)
        path=os.path.join(parent,ahall.name,db_session.name)
        shutil.rmtree(path)
        if db_session:
            db.delete(db_session)
            db.commit()
        return None         

#hall

class hall():
    
    def get_hall(self,db: Session, hall_id: int):
        return db.query(models.Hall).filter(models.Hall.id == hall_id).first()

    def get_halls(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Hall).offset(skip).limit(limit).all()    

    def create_hall(self,db: Session, hall: schemas.HallCreate):
        path=os.path.join(parent,hall.name)
        os.mkdir(path)
        db_hall = models.Hall(name=hall.name, from_date=hall.from_date,to_date=hall.to_date)
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)
        return db_hall

    def update_hall(self,db: Session, hall_id: int, hall: schemas.HallCreate):
        db_hall = (db.query(models.Hall).filter(models.Hall.id == hall_id).first())
        if db_hall:
                db_hall.name = hall.name
                db_hall.from_date = hall.from_date
                db_hall.to_date = hall.to_date
                db.commit()
                db.refresh(db_hall)
        return db_hall

    def delete_hall(self,db: Session, hall_id: int):
      
        db_hall = ( db.query(models.Hall).filter(models.Hall.id == hall_id).first()   )
        path=os.path.join(parent,db_hall.name)
        shutil.rmtree(path)
        if db_hall:
            db.delete(db_hall)
            db.commit()
        return None

