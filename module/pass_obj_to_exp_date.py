"""
Expiration Date Detection Module

This module manage the pipeline of sending products to the correct function,
which will be able to detect the expiration date for the spesific product
"""

from typing import Tuple, List, Union
from ultralytics import YOLO
from .products_ocr import products_exp_dates
from .fruit_veg_freshness import fresh_rotten
from PIL import Image

# TODO:
# 1. **class in detection**
#    - Take from Elya.


def find_exp_date(
    detections: List[Tuple[int,int,Tuple[int, int, int, int], Image.Image]], class_list: List[str]
)-> List[Union[
        Tuple[int, int, Tuple[int, int, int, int], Image.Image],  # Shelf
        Tuple[int, int, str]  # products
    ]]:
    """
    Determines right function to pass the object to, depending on type.
    Return: updated list with expiration dates for each detected object.
    """
    if len(detections) == 1:  # No objects detected, only shelf
        return detections

    model_date_path = "models/DateDetection.pt"
    model_date_detect = YOLO(model_date_path)
    model_date_detect.eval()

    model_freshness_path = "models/freshness_detection.pt"
    model_freshness_detect = YOLO(model_freshness_path)
    model_freshness_detect.eval()

    for i in range(1, len(detections)):  # Skip first detection (fridge frame)
        # for now, cheese is the only closed product we have in dataset
        if  detections[i][1] == 5:  
            product_img=detections[i][3]
            exp_date = products_exp_dates(model_date_detect, product_img)
        else:
            class_id = detections[i][1]
            identifier = class_list[class_id]
            exp_date = fresh_rotten(model_freshness_detect, detections[i][3], identifier)
        detections[i] = (detections[i][0], detections[i][1], exp_date)

    return detections  #id,class,exp_date
