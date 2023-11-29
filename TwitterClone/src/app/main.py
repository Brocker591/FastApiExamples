import uvicorn
from fastapi import FastAPI
from app.db_and_models.session import create_db_and_tables, drop_tables
from app.routers.users import router as user_router
from app.routers.posts import router as post_router
from app.routers.likes import router as like_router
from app.routers.followers import router as follower_router

from dotenv import load_dotenv, find_dotenv

from contextlib import asynccontextmanager

load_dotenv(find_dotenv())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    on_startup()
    yield
    # shutdown
    on_shutdown()


app = FastAPI(
    lifespan=lifespan,
    title="Twitter clone app",
    version="1.0.0"
)


app.include_router(user_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(follower_router)


# @app.on_event("startup")
def on_startup():
    create_db_and_tables()


# @app.on_event("shutdown")
def on_shutdown():
    drop_tables()


#if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=4445)
