import os
import json
from firebase_admin import credentials, firestore, initialize_app, _apps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials JSON string from .env
firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("FIREBASE_CREDENTIALS not found in .env")

# Parse JSON string into a Python dict
try:
    firebase_config = json.loads(firebase_json)
except json.JSONDecodeError as e:
    raise ValueError(f"Invalid FIREBASE_CREDENTIALS JSON format: {e}")

# Initialize Firebase only if not already initialized
if not _apps:
    cred = credentials.Certificate(firebase_config)
    initialize_app(cred)

# Initialize Firestore client
db = firestore.client()
