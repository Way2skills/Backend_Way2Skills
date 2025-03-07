import os
import json
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv


load_dotenv()

firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("FIREBASE_CREDENTIALS not found in .env")

firebase_config = json.loads(firebase_json)
cred = credentials.Certificate(firebase_config)
initialize_app(cred)

db = firestore.client()
