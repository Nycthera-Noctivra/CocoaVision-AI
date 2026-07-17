from ultralytics import YOLO
import cv2

MODEL_PATH = "model/best.pt"

model = YOLO(MODEL_PATH)


def detect(image):
    results = model.predict(
        image,
        conf=0.5
    )

    annotated = results[0].plot()

    detections = []

    for box in results[0].boxes:

        cls = int(box.cls[0])
        conf = float(box.conf[0])

        detections.append({
            "class": results[0].names[cls],
            "confidence": conf
        })

    return annotated, detections