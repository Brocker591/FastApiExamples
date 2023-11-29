from fastapi import FastAPI, BackgroundTasks, Request
import uvicorn
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout
)


app = FastAPI()

@app.middleware("http")
async def performance_middle(request: Request, call_next):
    start_time = time.perf_counter_ns()
    response = await call_next(request)
    end_time = time.perf_counter_ns()
    logging.info(f"Dauer in Sekunden: {end_time-start_time} für {request.url.path}")
    return response


def send_mail(email: str, message: str):
    with open("log.txt", mode="w") as email_file:
        content = f"Nachricht für {email}: {message}"
        email_file.write(content)


@app.get("/nachricht/{email}")
async def sende_nachricht(email: str, background_task: BackgroundTasks):
    background_task.add_task(send_mail, email, message="Bestellung aufgegeben")
    return { "message": f"Email ist an {email} verschickt worden"}







if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4445)