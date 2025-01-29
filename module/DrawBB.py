import cv2
from datetime import datetime

def DrawBB(detections):
    image = detections[0][3]  # Image of the whole shelf
    
    today = datetime.today() 
    
    for detection in detections[1:]: 
        x_min, y_min, x_max, y_max = detection[2]  # Bounding box coordinates in (x_min, y_min, x_max, y_max) format
        exp_date = detection[2]  # Expiry date (Index 2 in detection)

        # Parse the expiry date string into a datetime object
        exp_date = datetime.strptime(exp_date, "%Y-%m-%d")  # Assuming date format is YYYY-MM-DD
        
        # Calculate the difference in days
        days_diff = (exp_date - today).days
        
        # Set box color based on days until expiration
        if days_diff < 0:
            color = (0, 0, 255)  # Red if expired
        elif 0 <= days_diff <= 3:
            color = (0, 165, 255)  # Orange if within 1-3 days
        else:
            color = (0, 255, 0)  # Green if more than 3 days from expiration
        
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
    
    return image
