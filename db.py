import os
import json
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials JSON string from .env
firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("FIREBASE_CREDENTIALS not found in .env")

# Parse JSON string into a Python dict
firebase_config = json.loads(firebase_json)

# Write the parsed dict to a temporary file
with open("firebase_config.json", "w") as f:
    json.dump(firebase_config, f)

# Use the file to initialize Firebase Admin SDK
cred = credentials.Certificate("firebase_config.json")
initialize_app(cred)

# Initialize Firestore client
db = firestore.client()
