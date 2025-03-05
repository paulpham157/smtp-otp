from fastapi import FastAPI
from src.api.v1 import endpoints

app = FastAPI(
    title="Email OTP Service",
    description="Service to extract OTP from Gmail messages",
    version="1.0.0",
)

app.include_router(endpoints.router, prefix="/api/v1", tags=["email"])
