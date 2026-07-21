from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.detection_service import detection_service


router = APIRouter(prefix="/ai", tags=["AI Detection"])


@router.post("/predict")
async def predict(
    image: UploadFile = File(...),
    camera_id: str = Form("CAM-001"),
    location: str = Form("المسجد الحرام"),
):
    try:
        image_bytes = await image.read()

        result = detection_service.predict_image(
            image_bytes=image_bytes,
            camera_id=camera_id,
            location=location,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
    