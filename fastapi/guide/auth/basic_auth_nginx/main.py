from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_current_user
from app.config import settings
from app.models import ErrorMessage


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Nginx Basic Auth Example"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/public")
def public_route():
    return {"message": "This is a public route", "data": "public information"}


@app.get(
    "/protected",
    summary="Protected route (requires authentication)",
    description="This endpoint requires Basic Authentication to access",
    responses={
        200: {"description": "Successful response"},
        401: {
            "model": ErrorMessage,
            "description": "Unauthorized: Invalid credentials"
        }
    }
)
def protected_route(username: str = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "data": "secret information",
        "authenticated_user": username
    }
