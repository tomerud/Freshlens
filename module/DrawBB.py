import cv2
from datetime import datetime
import numpy as np
from typing import List, Tuple
from PIL import Image

def DrawOnImage(detections: List[
    Tuple[int, int, Tuple[int, int, int, int], np.ndarray] | 
    Tuple[int, int, Tuple[int, int, int, int], str]]) -> Image.Image:

    image = detections[0][3]  # Image of the whole shelf
    image = np.array(image)
    
    
    today = datetime.today() 
    
    for detection in detections[1:]: 
        x_min, y_min, x_max, y_max = detection[2]  # Bounding box coordinates in (x_min, y_min, x_max, y_max) format
        exp_date = detection[3]  # Expiry date (Index 3 in detection, instead of the product image)

        # Parse the expiry date string into a datetime object
        exp_date = datetime.strptime(exp_date, "%Y-%m-%d")  # Assuming date format is YYYY-MM-DD
        
        # Calculate the difference in days
        days_diff = (exp_date - today).days
        
        # Set box color based on days until expiration - BGR
        if days_diff < 0:
            color = (255, 0, 0)
        elif 0 <= days_diff <= 3:
            color = (255, 180,0 )
        else:
            color = (0, 255, 0)
        
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
    
    return Image.fromarray(image)
    #return image - in case of problems, return as nparray


