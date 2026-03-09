import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from backend.config.settings import get_settings

settings = get_settings()

def initialize_firebase():
    """Initializes Firebase Admin SDK."""
    if not firebase_admin._apps:
        # Check if service account file exists
        if settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        else:
            # Fallback for cloud environments (ADC)
            firebase_admin.initialize_app()
    
    return firestore.client()

# Initialize firestore client globally
db = initialize_firebase()
