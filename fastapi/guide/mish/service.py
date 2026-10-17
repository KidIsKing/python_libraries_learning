"""Для запуска переход в директорию с файлом и в терминале пишем: uvicorn service:app"""


# import random
import joblib
from fastapi import FastAPI
from pydantic import BaseModel


class ClientData(BaseModel):
    age: int
    salary: int
    education: bool
    work: bool
    car: bool


app = FastAPI()
model = joblib.load("model.pkl")

# Приложение, которое рандомно выдаёт да или нет, не основываясь на данных
# @app.get("/score")
# def score():
#     approved = random.choice([True, False])
#     return {"approved": approved}

# Приложение, которое выдаёт да или нет, основываясь на данных (зарплата), переданных в запросе
# @app.post("/score")  # Для передачи тела запроса пользуемся postman или переходим на сваггер - /docs
# def score(data: ClientData):
#     approved = data.salary > 50
#     return {"approved": approved}


@app.post("/score")
def score(data: ClientData):
    # Важно передать аргументы в порядке, который был при  обучении модели
    features = [data.age, data.salary, data.education, data.work, data.car]
    approved = not model.predict([features])[0].item()
    return {"approved": approved}
