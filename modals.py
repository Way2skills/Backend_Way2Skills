from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from fastapi import UploadFile

class RegistrationRequest(BaseModel):
    name: str
    phone_no: str
    email: EmailStr
    date: date  # ✅ Automatically converts string to date
    course: str
    duration: Optional[str] = "30 DAYS"
    transactionId: str
    file: UploadFile

# ✅ Pydantic Model for Response
class RegistrationResponse(BaseModel):
    id: str
    name: str
    phone_no: str
    email: EmailStr
    date: date
    course: str
    duration: Optional[str]
    transactionId: str
    file_base64: str
