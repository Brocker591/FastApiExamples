from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

engine = create_engine("sqlite:///users.db")
Base = declarative_base()

app = FastAPI()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)

class UserModel(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    age: int


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#new_user = User(firstname="John", lastname="Doe", email="jondoe@example.com", password="123456", age=30)

#session.add(new_user)
#session.commit()

#all_users = session.query(User).all()

#for user in all_users:
#    print(user.id, user.firstname, user.lastname)


@app.post("/register/", status_code=201)
def create_user(user: UserModel):
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    return { "id": new_user.id, "message":"User erfolgreich registiert"}