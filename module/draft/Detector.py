from ultralytics import YOLO
import logging

class YoloDetector:
    def __init__(self, model_path: str, confidence: float):
        try:
            self.model = YOLO(model_path)  # Load the trained model
            self.classList = self.model.names  # Get class names from the model
            self.confidence = confidence
        except Exception as e:
            raise ValueError(f"Failed to load the model from {model_path}: {e}")

    def detect(self, image) -> list:
        try:
            results = self.model.predict(image, conf=self.confidence)
            if not results or len(results) == 0:
                logging.warning("No results found.")
                return []
            result = results[0]
            return self.make_detections(result)
        except Exception as e:
            raise RuntimeError(f"Detection failed: {e}")

    def make_detections(self, result) -> list:
        boxes = result.boxes
        detections = []
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy.cpu().numpy().astype(int)
            class_number = int(box.cls.cpu().numpy()[0])
            class_name = self.classList[class_number]
            conf = float(box.conf.cpu().numpy()[0])

            detections.append({
                "bounding_box": [x1, y1, x2 - x1, y2 - y1],
                "class_id": class_number,
                "class_name": class_name,
                "confidence": conf
            })
        return detections
