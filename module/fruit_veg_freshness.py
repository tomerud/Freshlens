"""
Fruit and Vegetable Freshness Module

This module estimate the expiration dates of fruits and vegetables
based on their freshness and confidence scores from YOLO model.
"""

from datetime import datetime, timedelta
from ultralytics import YOLO
from PIL import Image
from .proccess_img_and_date import resize_with_letterbox

# TODO:

# 2. **calculating the exp date based on scale**
#    - expand the number of fruits and veg
#    - fix the base shelf life of the products
#    - cls = int(box.cls[0])  Class ID (0 for Fresh, 1 for Rotten)


def estimate_expiration(fruit: str, freshness_label: str, confidence: float
) -> datetime:
    """
    Estimate the expiration date based on its freshness and confidence score.
    Return: The estimated expiration date.
    """
    # Base shelf lives. These numbers are approximate based on internet.
    shelf_life = {
        'Apple': 26,
        'Banana': 7,
        'Carrot': 20,
        'Orange': 12,
        'Tomato': 9
    }
    # If the fruit is classified as Rotten, we assume it has already expired.
    # We choose to say it expired x days ago depending on how 'rotten' it is.
    if freshness_label == "Rotten":
        if confidence < 0.8:
            days_past = 2
        elif confidence < 0.9:
            days_past = 3
        elif confidence < 0.95:
            days_past = 4
        else:
            days_past = 5

        expiration_date = datetime.today() - timedelta(days=days_past)
    else:
        base_life = shelf_life.get(fruit)
        if confidence >= 0.9:
            multiplier = 1.0
        elif confidence >= 0.8:
            multiplier = 0.9
        elif confidence >= 0.7:
            multiplier = 0.8
        else:
            multiplier = 0.7

        estimated_days = int(base_life * multiplier)
        expiration_date = datetime.today() + timedelta(days=estimated_days)

    return expiration_date

def fresh_rotten(model: YOLO, produce: Image.Image, identifier_type: str):
    """
    Detect whether a produce item is fresh or rotten.
    Return:The estimated expiration date or -1 if detection fails.
    """
    # Preprocess the image
    resized_img, _, _, _ = resize_with_letterbox(produce, target_size=768)

    results = model.predict(resized_img)

    if results and results[0].boxes:
        box = results[0].boxes[0]
        cls = int(box.cls[0])   # Class ID (0 for Fresh, 1 for Rotten)
        conf = float(box.conf[0])

        label = "Fresh" if cls == 0 else "Rotten"

        expiration_date = estimate_expiration(identifier_type, label, conf)

        return expiration_date
    return None  # Error: detection failed
