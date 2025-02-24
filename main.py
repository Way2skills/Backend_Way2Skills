from fastapi import FastAPI, HTTPException, Form, File, UploadFile, Depends
from firebase_admin import credentials, firestore, initialize_app
from datetime import date
import base64
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from modals import RegistrationRequest, RegistrationResponse

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
initialize_app(cred)
db = firestore.client()
collection_name = "course_registrations"

app = FastAPI()


origins = [
    "http://localhost:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register/", response_model=dict)
async def register_user(
    name: str = Form(...),
    phone_no: str = Form(...),
    email: EmailStr = Form(...),
    date: date = Form(...),  # ✅ Auto-converts from string
    course: str = Form(...),
    duration: str = Form(default="30 DAYS"),
    transactionId: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Convert file to Base64
        file_data = await file.read()
        base64_encoded = base64.b64encode(file_data).decode("utf-8")

        # Save registration data to Firestore
        doc_ref = db.collection(collection_name).document()
        doc_ref.set({
            "name": name,
            "phone_no": phone_no,
            "email": email,
            "date": date.isoformat(),  # ✅ Auto-converts date to ISO format
            "course": course,
            "duration": duration,
            "transactionId": transactionId,
            "file_base64": base64_encoded  # ✅ Store image as Base64 string
        })

        return {"message": "Registration successful", "id": doc_ref.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/registrations/", response_model=List[RegistrationResponse])
def get_registrations():
    try:
        docs = db.collection(collection_name).stream()
        registrations = [
            RegistrationResponse(id=doc.id, **doc.to_dict()) for doc in docs
        ]  # ✅ Pydantic model ensures response consistency
        return registrations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
