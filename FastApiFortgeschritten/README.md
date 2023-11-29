#Middleware

```python
from fastapi import FastAPI, BackgroundTasks, Request

@app.middleware("http")
async def performance_middle(request: Request, call_next):
    start_time = time.perf_counter_ns()
    response = await call_next(request)
    end_time = time.perf_counter_ns()
    print(f"Dauer in Sekunden: {end_time-start_time} {request.url.path}")
    return response
```
Bei der Middleware muss angegeben bei welchem Aufruf Typ sie ausgelöst werden soll. Auserdem muss im Import die Klasse Request mit importiert werden. der erste Parameter ist der Request selbst, die zweite ist die call_nect methode, die den Request von der Middleware aus weiterleitet.

Aus diesem Grund muss response = await call_next(request) verwendet werden. Alles was über diesem Ausdruck an Code ausgeführt wird, wird vor dem eigentlichen Request ausgeführt und alles was danach an Code ausgeführt wird. wir nach dem Request ausgeführt. Jedoch noch bevor returnt wird. Am Ende muss das Object response auch returnt werden
