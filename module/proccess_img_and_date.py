"""
Immage Preprocessing Module

This module handle image and dates preprocessing tasks, like:
- Resizing images and bb while maintaining aspect ratio.
- Identifying the best candidate date boxes based on intersection / distance.
- Formatting date canidates and choosing the best one.
"""

from collections import Counter
from datetime import datetime
import re
from typing import List, Tuple
import numpy as np
from PIL import Image
from ultralytics.engine.results import Boxes  # for type hinting

# TODO:
# 1. Should add a rotation of date boxes here or at ClosedProductsOCR
# 2. Check about xyxy and xywh

def resize_with_letterbox(image: Image, target_size: int = 768) -> Tuple[Image.Image, float, int, int]:
    """
    Resize an image to the target size with letterboxing to maintain aspect ratio.
    Return:
    Letterboxed image,scaling factor,
    left padding, top padding.
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
    Return: Adjusted original image coordinates in xyxy format.
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
    Return: Intersection area.
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
    Returns: (center_x, center_y)
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
    Return: Best matching date boxes.
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

def parse_expiration_date(ocr_text):
    current_year = datetime.now().year
    min_year = current_year % 100  # Last two digits of the current year
    full_century = current_year - min_year  # Century base (e.g., 2000)

    if re.match(r'^\d{4}-\d{2}-\d{2}$', ocr_text):
        return ocr_text  # Return as-is if already correct

    # Extract all numbers from the string
    numbers = re.findall(r'\d+', ocr_text)
    numbers = [int(n) for n in numbers if int(n) > 0]  # Remove invalid zeros

    # Handle the case where only day and month are provided
    if len(numbers) == 2:
        day, month = sorted(numbers, reverse=True)  # Assume higher number is the day
        if 1 <= month <= 12 and 1 <= day <= 31:
            try:
                return datetime(current_year, month, day).strftime("%Y-%m-%d")
            except ValueError:
                return None # Invalid date

    if len(numbers) == 2 and numbers[1] >= 1000:  # Case: "4 2026"
        month, year = numbers
        if 1 <= month <= 12:
            try:
                return datetime(year, month, 1).strftime("%Y-%m-%d")
            except ValueError:
                return None # Invalid date

    if len(numbers) < 3:
        return None  # Not enough numbers to form a valid full date

    # Identify the best candidate for the year
    candidates = []
    for i, num in enumerate(numbers):
        if num >= 1000:  # Full year (e.g., 2024)
            candidates.append((num, i))
        elif num >= min_year:  # Two-digit year (e.g., 25 meaning 2025)
            candidates.append((full_century + num, i))

    # If multiple candidates, prefer the last occurring valid year
    if candidates:
        year, year_idx = sorted(candidates, key=lambda x: x[1])[-1]
        numbers.pop(year_idx)
    else:
        # If no valid year found, assume the last number is the year
        year = full_century + numbers.pop() if numbers[-1] < 100 else numbers.pop()
        year_idx = len(numbers)  # Treat as if it was at the last position

    # If fewer than two numbers remain, return None
    if len(numbers) < 2:
        return None

    # Find the month (number **closest** to the year in the input sequence)
    month_idx = min(range(len(numbers)), key=lambda i: abs(i - (year_idx - 1)))
    month = numbers.pop(month_idx)

    # If there are still numbers, use the closest to month as day
    if numbers:
        day_idx = min(range(len(numbers)), key=lambda i: abs(i - month_idx))
        day = numbers.pop(day_idx)
    else:
        return None  # Not enough numbers for a valid date

    if not (1 <= month <= 12 and 1 <= day <= 31):
        return None  # Invalid date

    # Reject impossible dates like "30 2"
    try:
        return datetime(year, month, day).strftime("%Y-%m-%d")
    except ValueError:
        return None  # Invalid date

def select_best_expiration_date(ocr_candidates):
    parsed_dates = {}
    modification_scores = {}

    for ocr_text in ocr_candidates:
        parsed = parse_expiration_date(ocr_text)
        if parsed:
            if parsed not in parsed_dates:
                parsed_dates[parsed] = 0
            parsed_dates[parsed] += 1  # Count occurrences

            # Compute modification score (lower is better)
            modification_scores[parsed] = modification_scores.get(parsed, 0) + compute_modification_score(ocr_text, parsed)

    if not parsed_dates:
        return None  # No valid dates

    # Select the most frequent valid date
    most_common = Counter(parsed_dates).most_common()
    top_freq = most_common[0][1]
    top_candidates = [date for date, freq in most_common if freq == top_freq]

    if len(top_candidates) == 1:
        return top_candidates[0]  # Only one top result

    # If there are multiple valid results, pick the one with the least modifications
    return min(top_candidates, key=lambda date: modification_scores[date])

def compute_modification_score(original_text, parsed_date):
    """Calculates modification severity from OCR output to final parsed date."""
    original_numbers = re.findall(r'\d+', original_text)
    parsed_numbers = re.findall(r'\d+', parsed_date)

    # If direct match (ignoring separators), score is 0
    if "".join(original_numbers) == "".join(parsed_numbers):
        return 0

    score = 0
    i, j = 0, 0
    original_year = datetime.now().year
    parsed_year = None

    while i < len(original_numbers) and j < len(parsed_numbers):
        orig, parsed = original_numbers[i], parsed_numbers[j]

        if orig == parsed:
            i += 1
            j += 1
            continue

        # Minor separator change (e.g., "3/1/2025" -> "2025-01-03")
        if len(orig) == len(parsed):
            score += 1  # Small penalty for format change

        # Two-digit year expanded (e.g., "25" -> "2025")
        elif len(orig) == 2 and parsed.startswith(orig):
            score += 5  # Moderate penalty for year assumption

        # Larger transformations (e.g., missing digits, swapped order)
        else:
            score += 3  # Bigger penalty

        # Capture the years to calculate the closest one later
        if len(orig) == 4 and orig.isdigit():
            original_year = int(orig)
        if len(parsed) == 4 and parsed.isdigit():
            parsed_year = int(parsed)

        i += 1
        j += 1

    # Handle year difference: Prefer the **closest** year
    if original_year and parsed_year and original_year != parsed_year:
        year_diff = abs(original_year - parsed_year)

        # Small penalty for a 1-year difference, but a larger penalty for bigger gaps
        score += year_diff * 2

    # Additional numbers in the original or parsed result
    score += abs(len(original_numbers) - len(parsed_numbers)) * 2  # Moderate penalty per extra/missing number

    return score
