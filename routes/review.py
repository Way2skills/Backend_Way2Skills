from fastapi import APIRouter, HTTPException
from db import db
from datetime import datetime

router = APIRouter()

@router.get("/")
def get_reviews():
    try:
        docs = db.collection("reviews").stream()
        reviews = []

        for doc in docs:
            data = doc.to_dict()
            created_at = data.get("createdAt")

            if isinstance(created_at, datetime):
                created_at = created_at.isoformat()
            elif isinstance(created_at, str):
                try:
                    created_at = parse_human_date(created_at).isoformat()
                except ValueError:
                    pass

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
    return datetime.strptime(date_str, "%B %d, %Y at %I:%M:%S %p UTC%z")
