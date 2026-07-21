from pathlib import Path

import cv2
import numpy as np
from tensorflow.keras.models import load_model

from app.core.settings import settings


class HaramDetectionModel:
    def __init__(self):
        self.model_path = Path(settings.MODEL_PATH)
        self.input_size = settings.MODEL_INPUT_SIZE

        self.class_names = [
            "Eating",
            "Visual Distortion",
            "Sleeping",
            
        ]

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at path: {self.model_path}"
            )

        self.model = load_model(str(self.model_path))

    def preprocess_image(self, image_bytes: bytes):
        np_array = np.frombuffer(image_bytes, np.uint8)

        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Invalid image file. Please upload a valid image.")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.resize(
            image,
            (self.input_size, self.input_size),
        )

        image = image.astype("float32") / 255.0

        image = np.expand_dims(image, axis=0)

        return image

    def predict(self, image_bytes: bytes):
        processed_image = self.preprocess_image(image_bytes)

        predictions = self.model.predict(processed_image, verbose=0)
        predictions = predictions[0]

        class_index = int(np.argmax(predictions))
        confidence = float(predictions[class_index])
        class_name = self.class_names[class_index]

        return {
            "violationType": class_name,
            "confidence": round(confidence, 4),
            "classIndex": class_index,
        }


model_service = HaramDetectionModel()
