"""Подключение базы данных."""


from fastapi import FastAPI
from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operation_router
from database import Base, engine


app = FastAPI()

app.include_router(wallet_router, prefix="/api/v1", tags=["wallet"])
app.include_router(operation_router, prefix="/api/v1", tags=["operation"])

Base.metadata.create_all(bind=engine)  # При старте приложения в базе данных будут созданы сущности
