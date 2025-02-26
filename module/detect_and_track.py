"""
This module detect and track objects in a video stream using YOLOv8 and DeepSORT.
In the future, we should finetune DeepSORT to achieve better tracking on our objects.
There was an attempt to use YOLOv11 with BOTSort,
but the BOTSort implementation had problems in the repository,
so at the last minute, we did the switch,
in future work, should finetune the trakcer,
and we should also implement saving and loading of the DeepSORT tracker,
so we can restore the last tracking ID of the objects.
Also, we will need to "add heads" to the YOLO model so we can detect the expiration dates
of the products in the video stream.
"""

import time
import os
from datetime import datetime
import threading
from typing import List, Tuple, Dict, Any
import cv2
import numpy as np
from PIL import Image
from deep_sort_realtime.deepsort_tracker import DeepSort
from ultralytics import YOLO

# TODO: DeepSort
# - Implement loading and saving of the DeepSort initialization
#   to restore the last detection tracking ID from the camera.
# - Ensure all XYXY and XYWH formats are correct and passed as needed.

def open_video_stream(rtsp_path: str) -> cv2.VideoCapture:
    """
    Open an RTSP video stream and return the capture object.
    If the stream fails to open, retry several times before giving up.
    """
    cap = cv2.VideoCapture(rtsp_path)
    retry_count = 5
    for i in range(retry_count):
        if cap.isOpened():
            return cap
        print(f"Failed to open stream. Retrying... ({i})")
        time.sleep(i + 1)
    print("Error - unable to open video stream after several retries.")
    return None

def initialize_video_writer(cap: cv2.VideoCapture) -> cv2.VideoWriter:
    """
    initialize the video writer to save the video with the tracking and detection results,
    in case we want to see the tracking and detection results later.
    """
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    thread_id = threading.get_ident()
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    output_path = f"{output_dir}/tracked_vid_{thread_id}_{current_date}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    return cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))


def update_tracker(
    tracker: Any,
    detections: List[np.ndarray],
    frame: np.ndarray,
    last_frame_objects: List[Dict[str, Any]],
    detected_products: List[Dict[str, Any]],
    debug: bool,
    class_list: List[str]
) -> None:
    """
    Update the DeepSORT tracker with the latest detections and track the objects.
    for now we are using DeepSORT tracker.
    """
    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed() or track.time_since_update > 1:
            continue

        # DeepSORT bounding box in tlbr format
        bbox = track.to_tlbr()
        min_x, min_y, max_x, max_y = map(int, bbox)

        class_id = track.get_det_class() if track.get_det_class() is not None else -1  # Use -1 for unknown class
        name= class_list[class_id]
        if debug:
            print(f"DeepSORT Track - ID: {track.track_id}, BBox: [{min_x}, {min_y}, {max_x}, {max_y}], Class: {name}")

        # Visulaize the tracking and detection results
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)  # Green Box
        cv2.putText(frame, f"ID: {track.track_id} {name}", (min_x, min_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        last_frame_objects.append({
                "id": track.track_id,
                "class_id": class_id,
                "bbox": (min_x, min_y, max_x, max_y)
            })




def process_video(
    rtsp_path: str,
    model: YOLO,
    record: bool = False,
    debug: bool = False,
) -> List[Tuple[int, int, Tuple[int, int, int, int], Image.Image]]:
    """
    Process a video stream from an RTSP source, detect and track objects in the video.
    Returns: list of tuples containing the object ID, class ID, bounding box,
    and image of the product.
    """
    detected_products = []  # List to store [Track_id(object id), class_id,bounding_box,img]

    cap = open_video_stream(rtsp_path)
    if cap is None:
        return -1
    if record:
        out = initialize_video_writer(cap)

    class_list = [class_name for _, class_name in sorted(model.names.items())]
    tracker = DeepSort(max_age=80, nn_budget=200, max_iou_distance=0.4)
    last_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            frame = None  # error in reading the frame

            break
        # Initialize a list to store objects for the current frame
        last_frame_objects = []
        last_frame = frame.copy()
        results = model.track(frame, persist=True,)

        detections = []
        if results[0].boxes.data is not None and len(results[0].boxes) > 0:
            boxes = results[0].boxes.xyxy.cpu().numpy()  # Bounding boxes
            confidences = results[0].boxes.conf.cpu().numpy()  # Confidence scores
            class_indices = results[0].boxes.cls.int().cpu().numpy()  # Class indices

            for box, confidence, class_idx in zip(boxes, confidences, class_indices):
                min_x, min_y, max_x, max_y = box
                width, height = max_x - min_x, max_y - min_y
                detections.append([[min_x, min_y, width, height], float(confidence), int(class_idx)])

                if debug:
                    print(f"YOLO Detection: Box: [{min_x}, {min_y}, {max_x}, {max_y}], Confidence: {confidence}, Class: {class_list[class_idx]}")
        else:
            if debug:
                print("No detections in this frame.")

        # Update DeepSORT tracker - need to fine tune the tracker for our objects
        update_tracker(tracker, detections, frame, last_frame_objects, detected_products, debug, class_list)

        if record:
            out.write(frame)

        cv2.imshow("YOLO Object Tracking & Counting", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop if 'q' key is pressed
            break

    if debug:
        print("\nLast Frame Objects:")
        for obj in last_frame_objects:
            print(f"ID: {obj['id']}, Class: {obj['class_id']}")

    if last_frame is not None:
        last_frame_pil = Image.fromarray(cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB))
        # add the Last frame, for drawing later the bounding boxes.
        detected_products.append((-1, -1, (-1, -1, -1, -1) , last_frame_pil))
    if last_frame_objects:
        for obj in last_frame_objects:
            min_x, min_y, max_x, max_y = obj['bbox']
            cropped_product = last_frame[min_y:max_y, min_x:max_x]  # only a single product
            if cropped_product.size == 0:
                print("Warning: cropped_product is empty for object with bbox:", obj['bbox'])
                continue
            detected_products.append(
            (
                obj["id"],
                obj["class_id"],
                obj["bbox"],
                Image.fromarray(cv2.cvtColor(cropped_product, cv2.COLOR_BGR2RGB)),
            )
        )


    # Release resources
    if record:
        out.release()  # Release the VideoWriter
    cap.release()
    cv2.destroyAllWindows()
    return detected_products
