from firebase_admin import firestore

from app.core.firebase import get_db


class FirestoreService:
    def __init__(self):
        self.db = get_db()

    def create_incident(
        self,
        violation_type: str,
        confidence: float,
        class_index: int,
        camera_id: str,
        location: str,
    ) -> dict:
        incident_ref = self.db.collection("incidents").document()

        incident_data = {
            "id": incident_ref.id,
            "violationType": violation_type,
            "confidence": confidence,
            "classIndex": class_index,
            "cameraId": camera_id,
            "location": location,
            "status": "new",
            "assignedUser": None,
            "timestamp": firestore.SERVER_TIMESTAMP,
        }

        incident_ref.set(incident_data)

        return {
            **incident_data,
            "timestamp": "server_timestamp",
        }

    def create_alert(
        self,
        incident_id: str,
        confidence: float,
    ) -> dict:
        alert_ref = self.db.collection("alerts").document()

        if confidence >= 0.90:
            priority = "high"
        elif confidence >= 0.60:
            priority = "medium"
        else:
            priority = "low"

        alert_data = {
            "id": alert_ref.id,
            "incidentId": incident_id,
            "priority": priority,
            "assignedTo": None,
            "status": "active",
            "createdAt": firestore.SERVER_TIMESTAMP,
        }

        alert_ref.set(alert_data)

        return {
            **alert_data,
            "createdAt": "server_timestamp",
        }


firestore_service = FirestoreService()