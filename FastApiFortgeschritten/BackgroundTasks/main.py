from fastapi import FastAPI, BackgroundTasks
import uvicorn

app = FastAPI()


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