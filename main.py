from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import register, admin, review

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://way2skills.netlify.app/",
        "https://www.way2skills.com",
        "https://way2skills.com",
    ],
   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return {"PING": "PONG"}

app.include_router(register.router, prefix="/api/v1/register", tags=["Register"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(review.router, prefix="/api/v1/reviews", tags=["Reviews"])
