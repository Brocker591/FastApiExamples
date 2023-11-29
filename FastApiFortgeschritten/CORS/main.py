from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

origins= {
    "https://example.com",
    "http://localhost:63342"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/hello/")
def hello_world():
    return { "Message": "hello world"}







if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4445)