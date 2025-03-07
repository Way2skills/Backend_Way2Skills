from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

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

class LoginRequest(BaseModel):
    email: str
    password: str
