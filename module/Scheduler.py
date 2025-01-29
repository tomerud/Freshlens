from Detect_and_track import Process_video
import requests
from threading import Thread
from typing import Tuple,List
import signal
from ultralytics import YOLO
from pass_obj_to_expDate import find_exp_date
from DrawBB import DrawBB

#TODO:

# 1. **Threading**
#    - think about where / if Thread.

# 2. **Video Stream Error Handling**:
#    - Add error handling for situations where the RTSP stream or video file cannot be opened (`cv2.VideoCapture`).

# 3. **bounding boxes**
#    - Draw bounding boxes color on the last frame according to the expiration dates.
#    - Might need to add the bb from the process video function to detections obj - notice need to update all files if thats the case!
#    - Pass it on to Mongo DB, and the rest of the epxiraiton data to the Reational DB

# 4. **Demo**
#    - change demo configuration

# 5. **DB**
#    - Add connection to DB


# handle camera notifications (future work - replace with camera notification protocol)
# we assume that when light is turned off, the camera stop streaming,
# in our code(Process_video) there is assumption the streaming stop immeditly (so there is no "black" frame), in future work it will be dealt with



def event_listen(camera_ip: str, port: int, model_path: str, demo : bool, stream: str = "stream") -> None:
    # the function is responsible to "wait" for camera to start streaming (when lights go on)
    # Returns: Nothing, but will pass on data to DB

    stop_event = threading.Event()

    def handle_signal(signal, frame):
        stop_event.set()  # Set the stop event to signal termination
        print(f"Stopping event listener for camera {camera_ip}:{port}...")

    # Set up signal handler for gracefully stopping
    signal.signal(signal.SIGINT, handle_signal)

    # Load a separate YOLO model instance for this thread
    model = YOLO(model_path)

    # best will be to use interupts or something similar here, for simplicity, time constarint and since we dont have actual IP camera
    while not stop_event.is_set():
        try:
            # Ideaily will also have used CV/interupts etc, in order to control the "waiting" for the event, while not waisting CPU time
            event = get_event_from_camera(camera_ip, port, demo)
        except Exception as e:
            print(f"Error getting event from camera: {e}")
            continue

        if event == "light_detected":
            rtsp_path = f"rtsp://{camera_ip}:{port}/{stream}"

            try:
                detections=Process_video(rtsp_path, model)
                expDate=find_exp_date(detections)
                fimg=DrawBB(expDate)
                sendToDB(camera_ip,expDate)
                sendToMongo(camera_ip,fimg)
            except Exception as e:
                print(f"Error processing video: {e}")

    print("Event listener has been stopped.")



def get_event_from_camera(camera_ip: str, port: int,demo:List[bool]) -> str: #with Fake-RTSP-Stream, we want to mimic one stream only, in deployment will need to change according to cameras protocol
# Example function for event notifications - we will need to replace with actual implementation
# do to constraints of time and hardware, we have left this "example" instead    
    if demo:
        return "light_detected"
    return "no_light_detected"


# Path to trained YOLO model
MODEL_PATH = "Models/ProductDetection.pt"  


# Start listener for each camera
camera_info = [("10.0.0.1",8554,"concatenated-sample")] # future work - need to centrlize all the camera work and listing
for ip, port,stream in camera_info:
    thread = Thread(target=event_listen,
                    args=(ip, port,stream,MODEL_PATH,True), # we are in demo, so True
                    daemon=True)
    thread.start()


