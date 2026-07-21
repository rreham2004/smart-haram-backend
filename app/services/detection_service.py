from app.ai.model_service import model_service
from app.services.firestore_service import firestore_service


class DetectionService:
    def predict_image(
        self,
        image_bytes: bytes,
        camera_id: str,
        location: str,
    ) -> dict:
        prediction = model_service.predict(image_bytes)

        violation_type = prediction["violationType"]
        confidence = prediction["confidence"]
        class_index = prediction["classIndex"]

        incident = firestore_service.create_incident(
            violation_type=violation_type,
            confidence=confidence,
            class_index=class_index,
            camera_id=camera_id,
            location=location,
        )

        alert = firestore_service.create_alert(
            incident_id=incident["id"],
            confidence=confidence,
        )

        result = {
            "violationType": violation_type,
            "confidence": confidence,
            "classIndex": class_index,
            "cameraId": camera_id,
            "location": location,
            "incidentId": incident["id"],
            "alertId": alert["id"],
            "status": "saved_to_firestore",
        }

        return result


detection_service = DetectionService()