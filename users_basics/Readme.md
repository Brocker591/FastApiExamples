# Zur geschuetzterEndpunktBeispiel main.py

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Session, create_engine, UniqueConstraint
from typing import Optional
from pydantic import validator
import bcrypt
import datetime
from jose import jwt

engine = create_engine("sqlite:///users.db")


app = FastAPI()

SECRET_KEY = "very-secret-key"
```
Kopf der App der Secret Key ist hier der Client Key


```python

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

```
Das Objekt oauth2_scheme wird benötigt, um einen Endpunkt mit einem Bearer Token abzusichern. Wenn kein Token verhanden ist, ist man nicht authorisiert für diesen Endpunkt. Hierbei wird in die Klammer der Wert tokenUrl angegeben. Das ist in diesem Fall der Entpunkt bei dem man sein Bearer Token erhalten kann. In dieser Datei befindet sich der Endpunkt /login/ dieser gibt ein Bearer Token zurück.




```python
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class UserBase(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str
    age: int


class UserCreate(UserBase):
    repeat_password: str

    @validator("repeat_password")
    def repeat_password_must_match(cls, v, values):

        if v != values["password"]:
            raise ValueError("Password must match")
        return v

class UserTable(UserBase, table=True):

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),UniqueConstraint("username"))


    id: Optional[int] = Field(default=None, primary_key=True)


def get_session():
    with Session(engine) as session:
        yield session

```
Erstellte Models mit pydantic und sqlmodel anschließend wird eine SQL Session erstellt, die mit Dependensy Injection in einen Endpunkt geladen werden kann.


```python
@app.get("/users/", dependencies=[Depends(oauth2_scheme)])
def get_all_users(session: Session = Depends(get_session)):
    users = session.query(UserTable).all()
    return users
```
Wie oben beschrieben muss mit dem Object oauth2_scheme ein Endpunkt geschützt werden, hierzu muss es als Dependency geladen werden. Bei diesem Endpunkt wird jedoch das Object in der Verarbeitung nicht benötigt, aus diesem Grund kann es in den Decorator (@app.get) reingeschrieben werden


```python
@app.get("/current_user/")
def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, key=SECRET_KEY)
    email = payload.get("email")
    current_user = session.query(UserTable).filter(UserTable.email == email).first()
    return current_user
```
Wie der Endpunkt /users/ hier wird auch der Endpunkt über den Token geschützt, nur hier muss auch das Token ausgelesen werden, da nach der Email der User in der Datenbank gesucht wird. Deswegen wird hier das Object oauth2_scheme in den Methodenaufrufer geschrieben, damit es in der Methode verwendet werden kann

```python
@app.post("/register/", status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = UserTable.from_orm(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return { "id": new_user.id, "message":"User erfolgreich registiert"}

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    db_user = session.query(UserTable).filter(UserTable.username == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if not bcrypt.checkpw(form_data.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    jwt_data = {
        "email": db_user.email,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=30)
    }

    access_token = jwt.encode(jwt_data, key=SECRET_KEY, algorithm="HS256")

    return {"access_token": access_token, "token_type": "bearer"}
```
Im Endpunkt /register/ wird bcrypt beim Password angewendet um einen Hashwert zu generieren und bei Login wird es nochmal angewendet, um damit zu prüfen, ob das Password korrekt ist.


```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```