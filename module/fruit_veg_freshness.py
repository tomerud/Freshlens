"""
Fruit and Vegetable Freshness Module

This module estimate the expiration dates of fruits and vegetables
based on their freshness and confidence scores from YOLO model.
"""

from datetime import datetime, timedelta
from ultralytics import YOLO
from PIL import Image
from pre_proccess import resize_with_letterbox

# TODO:
# 1. **Resize**
#    - make sure Resizing to the size trained on

# 2. **calculating the exp date based on scale**
#    - expand the number of fruits and veg
#    - fix the base shelf life of the products
#    - cls = int(box.cls[0])  Class ID (0 for Fresh, 1 for Rotten - might need to fix)

# 3. expiration date formating:
#    - make sure yyyy-mm-dd
#    - tomer : is it datetime or str?

def estimate_expiration(fruit: str, freshness_label: str, confidence: float) -> datetime:
    """
    Estimate the expiration date based on its freshness and confidence score.
    Return: The estimated expiration date.
    """
    # Base shelf lives (in days) for the fruit when fresh. These numbers are approximate.
    shelf_life = {
        "banana": 5,   # bananas typically ripen and over-ripen quickly
        "apple": 30,   # apples can last quite a while
        "orange": 14,  # oranges fall in between
    }

    # If the fruit is classified as Rotten, we assume it has already expired.
    # We choose to say it expired x days ago depending on how 'rotten' it is.
    if freshness_label == "Rotten":
        # Subtract extra days based on confidence:
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
        # For fresh fruits, we start with a base shelf life.
        base_life = shelf_life.get(fruit, 7)  # Default to 7 days if fruit is not listed.

        # Adjust shelf life based on confidence
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

# Example usage:
if __name__ == "__main__":
    model = YOLO('path_to_model')  # fill with new path
    product_img = Image.open('path_to_image.jpg')  # fill with new path

    fruit_type = "apple"  # Could be "banana" or "orange"
    try:
        expiration_date = fresh_rotten(model, product_img, fruit_type)
        if expiration_date != -1:
            print(f"Estimated expiration date: {expiration_date.strftime('%Y-%m-%d')}")
        else:
            print("Error: No valid prediction.")
    except ValueError as e:
        print(e)
