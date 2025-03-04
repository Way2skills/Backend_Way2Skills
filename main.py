from fastapi import FastAPI, HTTPException, Form, File, UploadFile, Depends
from firebase_admin import credentials, firestore, initialize_app
from datetime import date, datetime
import base64
from pydantic import  EmailStr
from typing import  List
from fastapi.middleware.cors import CORSMiddleware
from modals import RegistrationResponse
from dotenv import load_dotenv
import os
import json

load_dotenv()

firebase_json = os.getenv("FIREBASE_CREDENTIALS")

# Initialize Firebase
if firebase_json:
    firebase_config = json.loads(firebase_json)
    cred = credentials.Certificate(firebase_config)
    initialize_app(cred)
db = firestore.client()
collection_name = "course_registrations"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://way2skills.netlify.app/","https://www.way2skills.com/", "https://way2skills.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return {"PING": "PONG"}

@app.post("/register/", response_model=dict)
async def register_user(
    name: str = Form(...),
    phone_no: str = Form(...),
    email: EmailStr = Form(...),
    date_str: str = Form(...),  # Accept date as string
    course: str = Form(...),
    duration: str = Form(default="30 DAYS"),
    transactionId: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Convert date string to date object
        registration_date = date.fromisoformat(date_str)

        # Convert file to Base64
        file_data = await file.read()
        base64_encoded = base64.b64encode(file_data).decode("utf-8")

        # Save registration data to Firestore
        doc_ref = db.collection(collection_name).document()
        doc_ref.set({
            "name": name,
            "phone_no": phone_no,
            "email": email,
            "date": registration_date.isoformat(),  # Store date as ISO format string
            "course": course,
            "duration": duration,
            "transactionId": transactionId,
            "file_base64": base64_encoded  # Store image as Base64 string
        })

        return {"message": "Registration successful", "id": doc_ref.id}

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/registrations/", response_model=List[RegistrationResponse])
def get_registrations():
    try:
        docs = db.collection(collection_name).stream()
        registrations = [
            RegistrationResponse(id=doc.id, **doc.to_dict()) for doc in docs
        ]  # Pydantic model ensures response consistency
        return registrations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reviews/")
def get_reviews():
    try:
        docs = db.collection(reviews_collection).stream()

        reviews = []
        for doc in docs:
            data = doc.to_dict()

            created_at = data.get("createdAt")

            # Handle createdAt directly (convert to string if needed)
            if isinstance(created_at, datetime):
                created_at = created_at.isoformat()
            elif isinstance(created_at, str):
                # Optional: Try parsing back if you trust string input
                try:
                    created_at = parse_human_date(created_at).isoformat()
                except ValueError:
                    pass  # Keep original string if parsing fails (fallback)

            reviews.append({
                "comment": data.get("comment"),
                "createdAt": created_at,
                "name": data.get("name"),
                "rating": data.get("rating")
            })

        return reviews

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def parse_human_date(date_str: str) -> datetime:
    """ Convert 'February 25, 2025 at 11:50:31 AM UTC+5:30' into datetime object """
    try:
        return datetime.strptime(date_str, "%B %d, %Y at %I:%M:%S %p UTC%z")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")

