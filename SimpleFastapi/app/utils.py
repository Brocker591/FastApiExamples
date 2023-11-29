#Python file das alle Hash-Funktionen übernehmen soll

from passlib.context import CryptContext

#Wird benötigt um das Password der User Klasse mit einem Hashwert zu belegen
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)