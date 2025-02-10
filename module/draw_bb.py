"""
DrawBB Module

This module  draw bounding boxes on images based on
product expiration dates. The bounding box color indicates whether the product
is fresh (green), expiring soon (orange), or expired (red).
"""

from datetime import datetime
from typing import List, Tuple
import cv2
import numpy as np
from PIL import Image

def draw_on_image(
    detections: List[
        Tuple[int, int, Tuple[int, int, int, int], np.ndarray] |
        Tuple[int, int, Tuple[int, int, int, int], str]
    ]
) -> Image.Image:
    """
    Draws bounding boxes on an image based on expiration dates.
    """

    image = detections[0][3]  # Image of the whole shelf
    image = np.array(image)
    today = datetime.today()

    for detection in detections[1:]:
        x_min, y_min, x_max, y_max = detection[2]
        exp_date = detection[3]

        exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
        days_diff = (exp_date - today).days

        # Set box color based on expiration
        if days_diff < 0:
            color = (255, 0, 0)  # Expired (Red)
        elif 0 <= days_diff <= 3:
            color = (255, 180, 0)  # Expiring soon (Orange)
        else:
            color = (0, 255, 0)  # Fresh (Green)

        cv2.rectangle(# pylint: disable=E1101
            image, (x_min, y_min), (x_max, y_max), color, 2
        )

    return Image.fromarray(image)
