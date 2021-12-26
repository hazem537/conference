from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import column


from .import database 
Base = database.Base


class Doctor(Base):
    __tablename__ = "Doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject=Column(String )
    path=Column(String)
    file = Column(String)
    session_id = Column(Integer, ForeignKey("Sessions.id"))
    Session= relationship("Session", back_populates="doctors")


class Session(Base):
    __tablename__ = "Sessions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    time = Column(String)
    doctors = relationship("Doctor", cascade="all,delete", back_populates="Session")
    hall_id = Column(Integer, ForeignKey("halls.id"))
    hall = relationship("Hall", back_populates="sessions")



class Hall(Base):
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    from_date = Column(String)
    to_date = Column(String)
    sessions = relationship("Session", cascade="all,delete", back_populates="hall")
  

