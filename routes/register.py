from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from pydantic import EmailStr
from datetime import date
from db import db
import base64
from modals import RegistrationResponse
from typing import List

router = APIRouter()
collection_name = "course_registrations"

@router.post("/", response_model=dict)
async def register_user(
    name: str = Form(...),
    phone_no: str = Form(...),
    email: EmailStr = Form(...),
    date_str: str = Form(...),
    course: str = Form(...),
    duration: str = Form(default="30 DAYS"),
    transactionId: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        registration_date = date.fromisoformat(date_str)
        file_data = await file.read()
        base64_encoded = base64.b64encode(file_data).decode("utf-8")

        doc_ref = db.collection(collection_name).document()
        doc_ref.set({
            "name": name,
            "phone_no": phone_no,
            "email": email,
            "date": registration_date.isoformat(),
            "course": course,
            "duration": duration,
            "transactionId": transactionId,
            "file_base64": base64_encoded
        })
        return {"message": "Registration successful", "id": doc_ref.id}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/registrations", response_model=List[RegistrationResponse])
def get_registrations():
    try:
        docs = db.collection(collection_name).stream()
        return [RegistrationResponse(id=doc.id, **doc.to_dict()) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{record_id}")
def delete_registration(record_id: str):
    try:
        doc_ref = db.collection(collection_name).document(record_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Record not found")
        doc_ref.delete()
        return {"message": "Record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
