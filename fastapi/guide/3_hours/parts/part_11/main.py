"""ASYNC и фронтенд.
API курса валют - https://github.com/fawazahmed0/exchange-api.
TODO: frontend + формирование отчёта с выгрузкой в csv."""


from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operation_router
from app.api.v1.users import router as users_router
from app.database import Base, engine


app = FastAPI()

app.include_router(wallet_router, prefix="/api/v1", tags=["wallet"])
app.include_router(operation_router, prefix="/api/v1", tags=["operation"])
app.include_router(users_router, prefix="/api/v1", tags=["user"])

# app.mount("/static", StaticFiles(directory="app/static", name="static"))

Base.metadata.create_all(bind=engine)  # При старте приложения в базе данных будут созданы сущности
