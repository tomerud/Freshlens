from datetime import datetime
from typing import List, Tuple
import cv2
import numpy as np
from PIL import Image


def draw_on_image(
    detections: List[
        Tuple[int, int, Tuple[int, int, int, int], np.ndarray]
        | Tuple[int, int, Tuple[int, int, int, int], str]
    ]
) -> Image.Image:
    """
    Draw bounding boxes on the image based on expiry date.

    Args:
        detections (List[Tuple[int, int, Tuple[int, int, int, int], np.ndarray | str]]): 
            A list of detections where each detection contains:
            - An identifier (int)
            - A confidence score (int)
            - Bounding box coordinates (x_min, y_min, x_max, y_max)
            - Either an image (np.ndarray) or an expiration date (str)

    Returns:
        Image.Image: The modified image with drawn bounding boxes.
    """
    image = detections[0][3]  # Image of the whole shelf
    image = np.array(image)
    today = datetime.today()

    for detection in detections[1:]:  # Skip if no detections
        x_min, y_min, x_max, y_max = detection[2]  # Bounding box coordinates
        exp_date = detection[3]  # Expiry date as string

        exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
        days_diff = (exp_date - today).days

        # Set box color based on days until expiration (BGR format)
        if days_diff < 0:
            color = (255, 0, 0)  # Expired (Red)
        elif 0 <= days_diff <= 3:
            color = (255, 180, 0)  # Expiring soon (Orange)
        else:
            color = (0, 255, 0)  # Fresh (Green)

        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

    return Image.fromarray(image)
