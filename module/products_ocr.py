"""
products_ocr Module

This module detect expiration dates using a YOLO model,
and preprocess the expiration dates canidates
and extract the date using EasyOCR.
"""

import math


import numpy as np
import easyocr
from PIL import Image
from ultralytics import YOLO
from typing import List, Tuple

from module.proccess_img_and_date import (
    resize_with_letterbox,
    adjust_boxes,
    best_candidate_date,
    select_best_expiration_date,
    preprocess_image,
)


#TODO:
# 1. **process_image**:
#    - Consider other operations to improve OCR results.


def extract_text_from_boxes(image: Image, boxes: List[Tuple[float, float, float, float]]) -> str:
    """
    Extract text using EasyOCR from dates bounding boxes.
    returns: List of OCR results including text and bounding box coordinates.
    """

    ocr_results = []
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader with English language support

    for _, box in enumerate(boxes):
        x_min, y_min, x_max, y_max = map(int, box)  # Convert coordinates to integers

        # Crop the image using the bounding box
        cropped_img = image.crop((x_min, y_min, x_max, y_max))
        morph_img = preprocess_image(cropped_img)

        # Convert back to PIL Image for rotation
        morph_pil = Image.fromarray(morph_img)

        # Calculate the angle of rotation of the bounding box
        angle = math.atan2(y_max - y_min, x_max - x_min) * (180 / math.pi)
        if angle>10: # up to 10 degrees, ocr results are good
            rotated_imgs=[morph_pil.rotate(angle, expand=True), 
                          morph_pil.rotate(-angle, expand=True)]
        else:
            rotated_imgs=[morph_pil]

        for img in rotated_imgs:
            img_array = np.array(img.convert('RGB'))
            # Perform OCR using EasyOCR on the processed image
            text_results = reader.readtext(img_array, detail=0)
            text = " ".join(text_results)

            ocr_results.append(text)

    return ocr_results


def products_exp_dates(model: YOLO, product: Image.Image) -> str:
    """
    Handle the logic of getting Products Exp dates
    we will detect the dates canidates using YOLO model
    and then we will extract the text from the canidates
    Returns:  Expiry date
    """

    resized_img, scale, pad_left, pad_top = resize_with_letterbox(product, target_size=768)
    results = model.predict(resized_img)
    boxes = results[0].boxes

    date_boxes = [box for box in boxes if model.names[int(box.cls)] == "date"]
    if not date_boxes:
        return False
    due_boxes = [box for box in boxes if model.names[int(box.cls)] == "due"]

    if due_boxes:
        date_boxes = best_candidate_date(date_boxes,due_boxes) # reutrn 1 or more boxes
    adjusted_boxes = adjust_boxes(date_boxes, scale, pad_left, pad_top)


    ocr_results = extract_text_from_boxes(product, adjusted_boxes)
    date = select_best_expiration_date(ocr_results) # format dates and return best canidate
    return date
