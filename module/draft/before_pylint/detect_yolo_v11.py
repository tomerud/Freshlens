import cv2
from ultralytics import YOLO
from typing import List, Tuple
import time
from PIL import Image
import numpy as np
import threading # just to know the thread that handle this camera
from datetime import datetime
from collections import defaultdict


#TODO:
# 1. **Debugging and Visualization**:
#    - Remove or conditionally disable debug print statements (`YOLO Detection` and `DeepSORT Track` printouts) after testing.
# 2. **loading**
#    - add load states
# 3. **Deepsort? botsort?**
# 4. **delete bbox or boxes**
# fix annotated intalization, fix 


def process_video(rtsp_path:str, model: YOLO,Record:bool=False
                  ) -> List[Tuple[int,int,Tuple[int, int, int, int],Image.Image]]: #Record is for presentation and debugging purpose only
        #   Recive Video by RTSP, detect and track objects in the video
        #   Returns:Id of the object (product), id of class, bounding boxes of the product and Image of product 

        Detected_products = []  # List to store Track_id(object id), class_id,bounding_box,img]
        tracker_path="Models/botsort.yaml"
        # Open video capture
        retry_count = 5
        for i in range(retry_count):
            cap = cv2.VideoCapture(rtsp_path)
            if cap.isOpened():
                break
            print(f"Failed to open stream. Retrying... ({i}")
            time.sleep(i+1)  # give time to try and recover
        else:
            print("Error - unable to open video stream after several retries.")
            return -1 
        class_list = [class_name for _, class_name in sorted(model.names.items())]
        last_frame=None
        track_history = defaultdict(lambda: [])
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

        while cap.isOpened():

            ret, frame = cap.read()
            if not ret:
                break
                
            
                        # Initialize a list to store objects for the current frame
            last_frame_objects = []
            Last_frame = frame.copy()            # Run YOLO detection on the frame
            annotated_frame=frame.copy()
            results = model.track(frame, persist=True,tracker=tracker_path)
            if results[0].boxes.data is not None and len(results[0].boxes.data)>0:
                # Get the boxes and track IDs
                boxes = results[0].boxes.xywh.cpu() # make sure if can remove after tesr
                #bbox = results[0].boxes.xyxy.cpu() might replace after removing ploting tracks
                track_ids = results[0].boxes.id.int().cpu().tolist() if results[0].boxes.id is not None else []
                class_indices = results[0].boxes.cls.int().cpu().numpy()
                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Plot the tracks
                if track_ids:
                    for box, track_id,class_id in zip(boxes, track_ids,class_indices):
                        x, y, w, h = box
                        track = track_history[track_id]
                        track.append((float(x), float(y)))  # x, y center point
                        if len(track) > 30:  # retain 90 tracks for 90 frames
                            track.pop(0)

                        # Draw the tracking lines
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(
                            annotated_frame,
                            [points],
                            isClosed=False,
                            color=(230, 230, 230),
                            thickness=10,
                        )
                        x1 = x
                        y1 = y
                        x2 = x + w
                        y2 = y + h
                        # Add to last frame objects
                        last_frame_objects.append({
                                    "id": track_id,
                                    "class_id": class_list[class_id],
                                    "bbox": (x1, y1, x2, y2)
                                })
            if Record:
                out.write(annotated_frame)

            # Display the annotated frame
            cv2.imshow("YOLO11 Tracking", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        
        print("\nLast Frame Objects:") # remove after debug
        for obj in last_frame_objects:
            print(f"ID: {obj['id']}, Class: {obj['class_id']}")
        if Last_frame is not None:
            last_frame_pil = Image.fromarray(cv2.cvtColor(Last_frame, cv2.COLOR_BGR2RGB))
            Detected_products.append((-1,-1,-1 ,last_frame_pil))  # add the Last frame, for drawing later the bounding boxes.
        if last_frame_objects:
            for obj in last_frame_objects:
                print(type(y1), type(y2), type(x1), type(x2))
                x1, y1, x2, y2 = obj['bbox']
                cropped_product = Last_frame[int(y1):int(y2), int(x1):int(x2)]  # Crop the product's bounding box from the frame
                cropped_product_pil = Image.fromarray(cv2.cvtColor(cropped_product, cv2.COLOR_BGR2RGB))
                Detected_products.append((obj['id'], obj['class_id'],obj['bbox'],cropped_product_pil))
                
            Last_frame=None
        # Release resources
        if Record:
            out.release()  # Release the VideoWriter
        # Release the video capture object and close the display window
        cap.release()
        cv2.destroyAllWindows()


# Path to trained YOLO model
MODEL_PATH = "Models/object_detect_v11.pt"
  
# Load YOLO model
detection_model = YOLO(MODEL_PATH)
PATH="assets/freshlens2.mp4"

video_folder = ["assets/fridge_videos/IMG_0729.mp4","assets/fridge_videos/IMG_0725.mp4","assets/fridge_videos/IMG_0718.mp4","assets/fridge_videos/IMG_0717.mp4"]
vd_path=video_folder[0]
vd_path=video_folder[1]
vd_path=video_folder[2]
vd_path=video_folder[3]

res = process_video(video_folder[1], detection_model, True)

#res= process_video(PATH,detection_model,True)

#from draw_bb import draw_on_image
# if res: 
#     res[1] = (res[1][0], res[1][1], res[1][2], "2025-02-08")
#     res[2] = (res[2][0], res[2][1], res[2][2], "2025-02-13")
#     res[3] = (res[3][0], res[3][1], res[3][2], "2025-02-05")

#     save_path = "assets/shelf2.jpg"
#     draw=draw_on_image(res)
#     draw = cv2.cvtColor(np.array(draw), cv2.COLOR_RGB2BGR)
#     cv2.imwrite(save_path, draw)
#     print(f"Image saved at: {save_path}")
cv2.waitKey(0)
cv2.destroyAllWindows()
