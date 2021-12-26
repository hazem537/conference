from typing import Optional
from pydantic import BaseModel
import datetime

#doctor

class DoctorBase(BaseModel):
    name: str
    file: Optional[str] = None
    subject:str
    session_id: int


class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase):
    id: int
    path:str
    class Config:
        orm_mode = True



# session 
class SessionBase(BaseModel):
    name: str
    time: str
    hall_id:int


class SessionCreate(SessionBase):
    pass


class Session(SessionBase):
    id:int
    Doctors: list[Doctor] =[]

    class Config:
        orm_mode = True

# hall
class HallBase(BaseModel):
    name: str
    from_date: str
    to_date: str
  
   
class HallCreate(HallBase):
    pass

class Hall(HallBase):
    id: int
    sessions: list[Session] =[]
   
    class Config:
        orm_mode = True


