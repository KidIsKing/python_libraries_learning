from pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str


class LoginRequests(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    message: str = "Login successful"
