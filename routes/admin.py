from fastapi import APIRouter, HTTPException
from modals import LoginRequest
from auth import create_access_token
import os

router = APIRouter()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@router.post("/login")
async def admin_login(request: LoginRequest):
    if request.email == ADMIN_EMAIL and request.password == ADMIN_PASSWORD:
        token = create_access_token({"sub": request.email})
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid email or password")
