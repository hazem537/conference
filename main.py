from fastapi import  FastAPI

from routes import doctor,session,hall

from routes.depen import  models

from routes.depen import database
import os

SessionLocal= database.SessionLocal
engine=database.engine

models.Base.metadata.create_all(bind=engine)

directory = "file_tree"
parent_dir = "C:/AoConferance/"
path = os.path.join(parent_dir, directory)
#"C:/AoConferance/file_tree"
if(not (os.path.exists(path)) ):
  os.mkdir(path)
app = FastAPI()



app.include_router(doctor.router)
app.include_router(session.router)
app.include_router(hall.router)







