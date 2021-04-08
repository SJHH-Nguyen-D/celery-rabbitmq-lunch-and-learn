from fastapi import FastAPI
from pydantic import BaseModel

from worker import add#, get_user_score

app = FastAPI()

class Numbers(BaseModel):
    x: float
    y: float

class UserDemo(BaseModel):
    crim: float
    zn: float
    indus: float
    chas: float
    nox: float
    rm: float
    age: float
    dis: float
    rad: float
    tax: float
    ptratio: float
    b: float
    lstat: float


@app.post("/add")
def enqueue_add(n: Numbers):
    # using the celery delay method to enqueue the task with the given parameters
    res = add.delay(n.x, n.y)
    res.get() 

@app.post("/user_score")
def enqueue_get_user_score(u: UserDemo):
    get_user_score.delay(**u.dict())
