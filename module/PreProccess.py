from typing import List, Tuple
from ultralytics.engine.results import Boxes # for type hinting
from PIL import Image
import numpy as np

#TODO:
# 1. should add a rotation of date boxes here or at ClosedProductsOCR

def resize_with_letterbox(image: Image, target_size: int = 768) -> Tuple[Image.Image, float, int, int]:
#   Resizes an image to the target size with letterboxing to maintain aspect ratio.
#   Returns: Letterboxed image., Scaling factor, Padding added to the left, Padding added to the top.
    
    original_width, original_height = image.size
    scale = target_size / max(original_width, original_height)

    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    letterbox_image = Image.new("RGB", (target_size, target_size), (0, 0, 0))
    pad_left = (target_size - new_width) // 2
    pad_top = (target_size - new_height) // 2
    letterbox_image.paste(resized_img, (pad_left, pad_top))
    return letterbox_image, scale, pad_left, pad_top

def adjust_boxes(boxes: List[Boxes], scale: float, pad_left: int, pad_top: int) -> List[Tuple[float, float, float, float]]:
#   Adjust bounding boxes from letterboxed image to original image coordinates.
#   Returns: Adjusted original image coordinates in xyxy format.

    adjusted_boxes = []
    for box in boxes:
        x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
        # Adjust each coordinate
        x_min = (x_min - pad_left) / scale
        y_min = (y_min - pad_top) / scale
        x_max = (x_max - pad_left) / scale
        y_max = (y_max - pad_top) / scale
        adjusted_boxes.append((x_min, y_min, x_max, y_max))
    return adjusted_boxes

def intersection_area(box1: Boxes, box2: Boxes) -> float:
#   Calculate the intersection area of two bounding boxes.
#   Returns: Intersection area

    x_min1, y_min1, x_max1, y_max1 = box1.xyxy[0].tolist()

    x_min2, y_min2, x_max2, y_max2 = box2.xyxy[0].tolist()

    # Calculate the intersection area
    inter_x_min = max(x_min1, x_min2)
    inter_y_min = max(y_min1, y_min2)
    inter_x_max = min(x_max1, x_max2)
    inter_y_max = min(y_max1, y_max2)

    # Check if there is an intersection
    if inter_x_min < inter_x_max and inter_y_min < inter_y_max:
        intersection_width = inter_x_max - inter_x_min
        intersection_height = inter_y_max - inter_y_min
        return intersection_width * intersection_height
    else:
        return 0.0  # No intersection

def calculate_center(box: Boxes) -> Tuple[float, float]:
#   Calculate the center of a bounding box.
#   Returns: (center_x, center_y)

    center_x = box.xywh[0].tolist()[0]
    center_y = box.xywh[0].tolist()[1]
    return (center_x, center_y)


def euclidean_distance(center1: Tuple[float, float], center2: Tuple[float, float]) -> float:
#   Calculate the Euclidean distance between two points (center points of boxes).
#   Returns: Euclidean distance

    return np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)

def Best_Canidate_Date(date_boxes: List[Boxes], due_boxes: List[Boxes]) -> List[Boxes]:
#   Find the date boxes with the largest intersection with due boxes. If the intersection is 0 for all boxes, find the closest boxes.
#   We assume, in case there were multiple dates detected (very possible assumption, since there are multiple dates canidates on image),
#   that the detection that is closest to "due" class ('due', 'expired by', 'by') is the actual expiry date,
#   Returns: A list of the best matching date boxes.
    
    best_matches = []
    best_matches_distance = []
    max_intersection = 0
    best_distance = float('inf')

    for date_box in date_boxes:
        for due_box in due_boxes:
            # Calculate intersection area
            intersection = intersection_area(date_box, due_box)

            if intersection > max_intersection:
                # Update the best match if we find a better intersection
                best_matches = [date_box]  # Start a new list with the best match
                max_intersection = intersection
                best_distance = float('inf')  # Reset distance since intersection is found

            elif max_intersection != 0 and intersection == max_intersection:
                # If intersection is the same as the best, add to the matches
                best_matches.append(date_box)

            elif max_intersection == 0: # if so far, we havent found date with bounding box intersecting due, we will check distance and keep the ones closest.
                # in case we already have found one the is intersecting, we will skip this part

                date_center = calculate_center(date_box)
                due_center = calculate_center(due_box)
                distance = euclidean_distance(date_center, due_center)

                if distance < best_distance:
                    # Update if we find a closer box
                    best_matches = [date_box]  # Start a new list with the best match based on distance
                    best_distance = distance
                elif distance == best_distance:
                    # If the distance is the same, add to the matches
                    best_matches.append(date_box)

    return best_matches