from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()

router1 = APIRouter(tags=["Auth"])
router2 = APIRouter(tags=["Tweets"])


@router1.get("/hello/")
def hello_world():
    return { "Message": "hello world"}

@router1.get("/hello2/")
def hello_world2():
    return { "Message": "hello world2"}

@router2.get("/hello3/")
def hello_world3():
    return { "Message": "hello world3"}

@router2.get("/hello4/")
def hello_world4():
    return { "Message": "hello world4"}


app.include_router(router1)
app.include_router(router2)





if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4445)