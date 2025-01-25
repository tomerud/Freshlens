from typing import List, Tuple, Dict
import easyocr
from ultralytics.engine.results import Boxes # for type hinting
import matplotlib.pyplot as plt
from PIL import Image
import torch
from ultralytics import YOLO
import cv2
import numpy as np
import math
from PreProccess import resize_with_letterbox, adjust_boxes , Best_Canidate_Date

#TODO:
# 1. **Rotation**:
#    - Add rotation to pictures as detexct (unless under 10? in ordedr to improve results): both sides rotate

# 2. **Validate Date**:
#    - Add Validation to date results

# 3. **test**
#   - remove the test


def extract_text_from_boxes(image: Image, boxes: List[Tuple[float, float, float, float]]) -> List[Dict[str, object]]:
#   Extract text using EasyOCR from regions defined by bounding boxes.
#   Returns: List of OCR results including text and bounding box coordinates.

    ocr_results = []
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader with English language support

    for i, box in enumerate(boxes):
        x_min, y_min, x_max, y_max = map(int, box)  # Convert coordinates to integers

        # Crop the image using the bounding box
        cropped_img = image.crop((x_min, y_min, x_max, y_max))
        # Convert cropped image to grayscale
        cropped_img_gray = np.array(cropped_img.convert('L'))

        # Calculate the angle of rotation of the bounding box
        angle = math.atan2(y_max - y_min, x_max - x_min) * (180 / math.pi)

        if angle == 0:
            print("The box is aligned horizontally.")
        else:
            print(f"The box is rotated by {angle} degrees.")
        print("--------------------------------------")

        # perform morphological operations to clean up (with a smaller kernel) - might need to remove
        kernel = np.ones((3, 3), np.uint8)
        morph_img = cv2.morphologyEx(cropped_img_gray, cv2.MORPH_CLOSE, kernel)

        # Perform OCR using EasyOCR on the processed image
        text_results = reader.readtext(morph_img, detail=0)  # `detail=0` returns just the text
        text = " ".join(text_results)  # Combine results into a single string if multiple words are detected

        ocr_results.append({"box": (x_min, y_min, x_max, y_max), "text": text})

        # Print detection details
        print(f"Detection {i+1}: Text extracted = {text.strip()}")

        # Display the cropped image and the extracted text
        plt.imshow(morph_img, cmap='gray')
        plt.title(f"Detection {i+1}: {text.strip()}")
        plt.axis('off')
        plt.show()

    return ocr_results


def ProductsExpDates(model: YOLO, original_img: Image, product: Dict[int, str]) -> Tuple[str, int, str]:
#   handle the logic of getting Products Exp dates
#   Returns: Expiry date, Id of the object (product), name of class (what product class) 

    #preprocess the image
    resized_img, scale, pad_left, pad_top = resize_with_letterbox(original_img, target_size=768)

    # Predict using YOLO
    results = model.predict(resized_img)
    boxes = results[0].boxes


    date_boxes = [box for box in boxes if model.names[int(box.cls)] == "date"]
    if not date_boxes:
      return False
    due_boxes = [box for box in boxes if model.names[int(box.cls)] == "due"]

    if due_boxes:
      date_boxes = Best_Canidate_Date(date_boxes,due_boxes) # reutrn 1 or more boxes
    adjusted_boxes = adjust_boxes(date_boxes, scale, pad_left, pad_top)

    # Pass the original image and adjusted boxes to Tesseract OCR
    ocr_results = extract_text_from_boxes(original_img, adjusted_boxes)

    # add filtering based on OCR results, what is the best canidate for expiry date
    #
    #
    #
    #
    #
    #
    #


    plt.imshow(original_img)
    plt.axis('off')
    for box in adjusted_boxes:
        x_min, y_min, x_max, y_max = map(int, box)
        plt.gca().add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                          edgecolor='red', facecolor='none', linewidth=2))
    plt.show()

if __name__ == "__main__":
    # Path to the YOLO model and image
    model_path = "Models/DateDetection.pt"
    image_path = "assets/cheese.jpg"
    original_img = Image.open(image_path)
    rotated_img = original_img.rotate(90, expand=True)

    d={2,"orange"}
    # Load the YOLO model
    model = YOLO(model_path)
    model.eval()
    ProductsExpDates(model,rotated_img,d)