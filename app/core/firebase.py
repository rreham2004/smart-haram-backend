import firebase_admin
from firebase_admin import credentials, firestore

from app.core.settings import settings


def initialize_firebase():
    if firebase_admin._apps:
        return

    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)


def get_db():
    initialize_firebase()
    return firestore.client()