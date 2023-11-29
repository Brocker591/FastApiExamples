from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user



#Erstellt alle Models auf der Datenbank
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


#Importiert alle Routen aus dem Router-Objekt, welches in den entsprechenden Post und User Dateien generiert wurde
app.include_router(post.router)
app.include_router(user.router)



@app.get("/")
def root():
    return{"message": "Hello world"}




