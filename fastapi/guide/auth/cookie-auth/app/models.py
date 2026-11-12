from pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    username: str
    message: str = "Login successful"
