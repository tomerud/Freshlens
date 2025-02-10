import cv2
from ultralytics import YOLO
from typing import List, Tuple
from deep_sort_realtime.deepsort_tracker import DeepSort
import time
from PIL import Image
import numpy as np
import threading
from datetime import datetime
# TODO:

# 1. **Debugging and Visualization**:
#    - Remove or conditionally disable debug print statements (`YOLO Detection` and `DeepSORT Track` printouts) after testing.

# 2. **DeepSort**:
#    - Add loading and saving of the deepsort intalization, so can restore last detection tracking ID from the camera
#    - Make sure all the xyxy and xywh format are rights and passed as needed


if __name__ == "__main__":
    def Process_video(rtsp_path:str, model: YOLO,Record:bool=False) -> List[Tuple[int,int,Tuple[int, int, int, int],Image.Image]]: #Record is for presentation and debugging purpose only
        #   Recive Video by RTSP, detect and track objects in the video
        #   Returns:Id of the object (product), id of class, bounding boxes of the product and Image of product 

        Detected_products = []  # List to store Track_id(object id), class_id,bounding_box,img]
        # Open video capture
        cap = cv2.VideoCapture(rtsp_path)
        retry_count = 5
        for i in range(retry_count):
            cap = cv2.VideoCapture(rtsp_path)
            if cap.isOpened():
                break
            print(f"Failed to open stream. Retrying... ({i}")
            time.sleep(i+1)  # Sleep before retrying
        else:
            print("Error - unable to open video stream after several retries.")
            return -1 

        
        # List of class names
        class_list = [class_name for _, class_name in sorted(model.names.items())]

        # Initialize DeepSORT tracker
        tracker = DeepSort(max_age=80, nn_budget=200, max_iou_distance=0.4)
        last_frame=None

        if Record:
            # Get frame dimensions
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            thread_id = threading.get_ident()  # Get the thread ID
            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
            output_path = f"output/tracked_vid_{thread_id}_{current_date}.mp4"  # Combine thread ID and date for unique identification
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        #try read stream
        while cap.isOpened():
            ret, frame = cap.read()
            retry_count = 3
            for i in range(retry_count):
                ret, frame = cap.read()
                if ret:
                    break
                print(f"Failed to read frame. Retrying... ({i}")
                time.sleep(1)  # Sleep before retrying
            else:
                print("Error - unable to read frame after several retries.")
                continue  # Skip this frame and continue processing the next one

                
            # Initialize a list to store objects for the current frame
            last_frame_objects = []
            Last_frame = frame.copy()            # Run YOLO detection on the frame
            results = model.track(frame, persist=True, classes=[1, 2, 3, 5, 6, 7])  # YOLO class indices

            detections = []
            if results[0].boxes.data is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()  # Bounding boxes
                confidences = results[0].boxes.conf.cpu().numpy()  # Confidence scores
                class_indices = results[0].boxes.cls.int().cpu().numpy()  # Class indices

                for box, confidence, class_idx in zip(boxes, confidences, class_indices):
                    x1, y1, x2, y2 = box # can access boxes,xywh, can be replaced
                    w, h = x2 - x1, y2 - y1  # Convert to (x, y, w, h) format for DeepSORT
                    detections.append([[x1, y1, w, h], float(confidence), int(class_idx)])

                    # Debug YOLO detections - remove after tests
                    print(f"YOLO Detection: Box: [{x1}, {y1}, {x2}, {y2}], Confidence: {confidence}, Class: {class_list[class_idx]}")
            else:
                print("No detections in this frame.")

            # Update DeepSORT tracker
            tracks = tracker.update_tracks(detections, frame=frame)

            for track in tracks:
                if not track.is_confirmed() or track.time_since_update > 1:
                    continue

                # DeepSORT bounding box in tlbr format
                bbox = track.to_tlbr()
                x1, y1, x2, y2 = map(int, bbox)

                # Retrieve the class index (class ID) instead of the name
                class_id = track.get_det_class() if track.get_det_class() is not None else -1  # Use -1 for unknown class

                # Debug output for DeepSORT tracks - remove after test
                print(f"DeepSORT Track - ID: {track.track_id}, BBox: [{x1}, {y1}, {x2}, {y2}], Class: {class_id}")

                # Draw DeepSORT bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green Box
                cv2.putText(frame, f"ID: {track.track_id} {class_id}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                # Add to last frame objects
                last_frame_objects.append({
                        "id": track.track_id,
                        "class_id": class_id,
                        "bbox": (x1, y1, x2, y2)
                    })
            if Record:
                out.write(frame)
                
            # Show the frame 
            cv2.imshow("YOLO Object Tracking & Counting", frame)
            
            # Exit loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        print("\nLast Frame Objects:") # remove after debug
        for obj in last_frame_objects:
            print(f"ID: {obj['id']}, Class: {obj['class_id']}")
        if Last_frame is not None:
            last_frame_pil = Image.fromarray(cv2.cvtColor(Last_frame, cv2.COLOR_BGR2RGB))
            Detected_products.append((-1,-1,-1 ,last_frame_pil))  # add the Last frame, for drawing later the bounding boxes.
        if last_frame_objects:
            for obj in last_frame_objects:
                x1, y1, x2, y2 = obj['bbox']
                cropped_product = Last_frame[y1:y2, x1:x2]  # Crop the product's bounding box from the frame
                cropped_product_pil = Image.fromarray(cv2.cvtColor(cropped_product, cv2.COLOR_BGR2RGB))
                Detected_products.append((obj['id'], obj['class_id'],obj['bbox'],cropped_product_pil))
                
            Last_frame=None
        # Release resources
        if Record:
            out.release()  # Release the VideoWriter
        cap.release()
        cv2.destroyAllWindows()
        return Detected_products


# Path to trained YOLO model
MODEL_PATH = "Models/ProductDetection.pt"  
# Load YOLO model
detection_model = YOLO(MODEL_PATH)
PATH="assets/freshlens2.mp4"
res= Process_video(PATH,detection_model)

from DrawBB import DrawOnImage 
res[1] = (res[1][0], res[1][1], res[1][2], "2025-02-08")
res[2] = (res[2][0], res[2][1], res[2][2], "2025-02-13")
res[3] = (res[3][0], res[3][1], res[3][2], "2025-02-05")

save_path = "assets/shelf.jpg"
draw=DrawOnImage(res)
draw = cv2.cvtColor(np.array(draw), cv2.COLOR_RGB2BGR)
cv2.imwrite(save_path, draw)
print(f"Image saved at: {save_path}")
cv2.waitKey(0)
cv2.destroyAllWindows()

""" for i,j,k,l in res:
    l.show()
    if cv2.waitKey(0) & 0xFF == ord('q'):  # Wait for key press, quit if 'q' is pressed
        break """