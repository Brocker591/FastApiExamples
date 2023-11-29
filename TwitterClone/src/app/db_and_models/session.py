from sqlmodel import Session, SQLModel
import os


from app.db_and_models.enigne import engine

async def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_tables():
    os.remove("twitterclone.db")
    