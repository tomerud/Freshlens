"""
Expiration Date Detection Module

This module manage the pipeline of sending products to the correct function,
which will be able to detect the expiration date for the spesific product
"""

from typing import Tuple, List, Any
from ultralytics import YOLO
from ClosedProductsOCR import ProductsExpDates
from fruit_veg_freshness import fresh_rotten
from Kmeans import kmeans_expdate

# TODO:
# 1. **class in detection**
#    - Take from Elya.
# 2. **logic of func**
#    - decide the correct logic
# 3. **Changing / reuturn**
#    - might be better to detections[i][3]
#    - Change the type hinting - first element is the photo the rest are str

def find_exp_date(detections: List[Tuple[int, int, Any]], class_list: List[str]) -> List[Tuple[int, int, Tuple[int, int, int, int], str]]:
    """
    Determines right function to pass the object to.
    Return: updated list with expiration dates for each detected object.
    """
    if len(detections) == 1:  # No objects detected, only shelf
        return detections

    model_date_path = "Models/DateDetection.pt"
    model_date_detect = YOLO(model_date_path)
    model_date_detect.eval()

    model_freshness_path = "Models/FreshnessDetection.pt"
    model_freshness_detect = YOLO(model_freshness_path)
    model_freshness_detect.eval()

    full_exp = (0, 5)  # Fruits and vegetables (tomatoes, bananas)

    for i in range(1, len(detections)):  # Skip first detection (fridge frame)
        if detections[i][1] in full_exp:  # Fully implemented expiration date detection
            exp_date = kmeans_expdate(detections[i])
        elif 0 <= detections[i][1] <= 10:
            class_id = detections[i][1]
            identifier = class_list[class_id]
            exp_date = fresh_rotten(model_freshness_detect, detections[i][3], identifier)
        else:
            exp_date = ProductsExpDates(model_date_detect, detections[i][3])
        detections[i] = (detections[0], detections[1], detections[2], exp_date)

    return detections  # Ensure consistency with return statements
