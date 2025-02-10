"""
Immage Preprocessing Module

This module provides functions for image preprocessing tasks, including:
- Resizing images with letterboxing - maintaining aspect ratio.
- Adjusting bounding boxes after resizing.
- Calculating intersection areas
- Calculatig distances between bounding boxes.
- Identifying the best candidate date boxes based on intersection / proximity.

Functions:
    - resize_with_letterbox: Resizes an image with letterboxing.
    - adjust_boxes: Adjusts bounding boxes after resizing.
    - intersection_area: Intersection area between two boxes.
    - calculate_center: Computes the center coordinates of a bounding box.
    - euclidean_distance: Computes the Euclidean distance between two points(centers).
    - best_candidate_date: Finds the most relevant date boxes based on intersections / proximity.
"""

from typing import List, Tuple
from ultralytics.engine.results import Boxes  # for type hinting
from PIL import Image
import numpy as np

# TODO:
# 1. Should add a rotation of date boxes here or at ClosedProductsOCR
# 2. Check about xyxy and xywh

def resize_with_letterbox(image: Image, target_size: int = 768) -> Tuple[Image.Image, float, int, int]:
    """
    Resize an image to the target size with letterboxing to maintain aspect ratio.

    Args:
        image (Image): The input PIL image.
        target_size (int, optional): The target size for resizing. Defaults to 768.

    Returns:
        Tuple[Image.Image, float, int, int]: Letterboxed image, scaling factor, left padding,
        top padding.
    """
    original_width, original_height = image.size
    scale = target_size / max(original_width, original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    letterbox_image = Image.new("RGB", (target_size, target_size), (0, 0, 0))
    pad_left = (target_size - new_width) // 2
    pad_top = (target_size - new_height) // 2
    letterbox_image.paste(resized_img, (pad_left, pad_top))

    return (
        letterbox_image,
        scale,
        pad_left,
        pad_top,
    )

def adjust_boxes(boxes: List[Boxes], scale: float, pad_left: int, pad_top: int) -> List[Tuple[float, float, float, float]]:
    """
    Adjust bounding boxes from letterboxed image to original image coordinates.

    Args:
        boxes (List[Boxes]): List of bounding boxes.
        scale (float): Scaling factor.
        pad_left (int): Left padding.
        pad_top (int): Top padding.

    Returns:
        List[Tuple[float, float, float, float]]: Adjusted original image coordinates in
        xyxy format.
    """
    adjusted_boxes = []
    for box in boxes:
        x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
        adjusted_boxes.append((
            (x_min - pad_left) / scale,
            (y_min - pad_top) / scale,
            (x_max - pad_left) / scale,
            (y_max - pad_top) / scale
        ))
    return adjusted_boxes

def intersection_area(box1: Boxes, box2: Boxes) -> float:
    """
    Calculate the intersection area of two bounding boxes.

    Args:
        box1 (Boxes): First bounding box.
        box2 (Boxes): Second bounding box.

    Returns:
        float: Intersection area.
    """
    x_min1, y_min1, x_max1, y_max1 = box1.xyxy[0].tolist()
    x_min2, y_min2, x_max2, y_max2 = box2.xyxy[0].tolist()

    inter_x_min = max(x_min1, x_min2)
    inter_y_min = max(y_min1, y_min2)
    inter_x_max = min(x_max1, x_max2)
    inter_y_max = min(y_max1, y_max2)

    if inter_x_min < inter_x_max and inter_y_min < inter_y_max:
        return (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
    return 0.0

def calculate_center(box: Boxes) -> Tuple[float, float]:
    """
    Calculate the center of a bounding box.

    Args:
        box (Boxes): Bounding box.

    Returns:
        Tuple[float, float]: (center_x, center_y)
    """
    return tuple(box.xywh[0].tolist()[:2])

def euclidean_distance(center1: Tuple[float, float], center2: Tuple[float, float]) -> float:
    """
    Calculate the Euclidean distance between two points.

    Args:
        center1 (Tuple[float, float]): First center point.
        center2 (Tuple[float, float]): Second center point.

    Returns:
        float: Euclidean distance.
    """
    return np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)

def best_candidate_date(date_boxes: List[Boxes], due_boxes: List[Boxes]) -> List[Boxes]:
    """
    Find the date boxes with the largest intersection with due boxes.
    If the intersection is 0 for all boxes, find the closest ones.

    Args:
        date_boxes (List[Boxes]): List of detected date boxes.
        due_boxes (List[Boxes]): List of detected 'due' class boxes.

    Returns:
        List[Boxes]: Best matching date boxes.
    """
    best_matches = []
    max_intersection = 0
    best_distance = float('inf')

    for date_box in date_boxes:
        for due_box in due_boxes:
            intersection = intersection_area(date_box, due_box)

            if intersection > max_intersection:
                best_matches = [date_box]
                max_intersection = intersection
                best_distance = float('inf')
            elif max_intersection != 0 and intersection == max_intersection:
                best_matches.append(date_box)
            elif max_intersection == 0:
                date_center = calculate_center(date_box)
                due_center = calculate_center(due_box)
                distance = euclidean_distance(date_center, due_center)

                if distance < best_distance:
                    best_matches = [date_box]
                    best_distance = distance
                elif distance == best_distance:
                    best_matches.append(date_box)

    return best_matches
