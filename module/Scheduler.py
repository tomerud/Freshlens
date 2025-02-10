from Detect_and_track import Process_video
from Backend_connect import sendToDB, sendToMongo, alert_server
import threading 
from typing import Tuple,List
import signal
from ultralytics import YOLO
from pass_obj_to_expDate import find_exp_date
from DrawBB import DrawOnImage
import socketio
import time

#TODO:

# 1. **Threading**
#    - think about where / if Thread - GIL , Multiproccess

# 2. **Demo**
#    - change demo configuration

# 3. **connection to db and threading**
#    - Should the for loop be switched with while?
#    - Update the Ip list from DB?

# 4. **Secure conneciton** - future work
#    - replace the RTSP with Secure RTSP / vpn etc

# 5. ** YOLO resizing**:
#    - think if resizing training or scaling!!!!

# 6. ** Add SSL/TLS / mTLS**

# Setup socketIO client
socket = socketio.Client( 
    reconnection=True, 
    reconnection_attempts=10, 
    reconnection_delay=1,
    reconnection_delay_max=30)#client will attempt to reconnect when disconnected

@socket.event
def connect():
    print("Connected to SocketIO server.")

@socket.event
def disconnect():
    print("Disconnected from SocketIO server.")

# handle camera notifications (future work - replace with camera notification protocol)
# we assume that when light is turned off, the camera stop streaming,
# in our code(Process_video) there is assumption the streaming stop immeditly (so there is no "black" frame), in future work it will be dealt with

def event_listen(socket,camera_ip: str, port: int, demo : bool, stream: str = "stream") -> None:
    # the function is responsible to "wait" for camera to start streaming (when lights go on)
    # Returns: Nothing, but will pass on data to DB
    stop_event = threading.Event() # this way signal will stop all the threads (since all of them are checking stop_event)

    def handle_signal(signal, frame):
        stop_event.set()  # Set the stop event to signal termination
        print(f"stopping event listener for camera {camera_ip}:{port}...")
    # Set up signal handler for gracefully stopping
    signal.signal(signal.SIGINT, handle_signal)

    # Load a separate YOLO model instance for this thread
    # we have to do it separatly for each thread, since pyhton use GIL
    # consideration for python!!!! maybe multiprocess is better? need to study it
    # BASED ON YOLO DOCS! not thread safe
    # Path to trained YOLO model
    MODEL_PATH = "Models/ProductDetection.pt" 
    model = YOLO(MODEL_PATH)
    class_list = [class_name for _, class_name in sorted(model.names.items())]
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
                if( -1 == detections or None== detections):
                    error_message = "Error Unable to open video stream"
                    alert_server(socket,camera_ip,port,error_message)
                    continue
                expDate=find_exp_date(detections,class_list)
                fimg=DrawOnImage(expDate)
                sendToDB(socket,camera_ip,port,expDate)
                sendToMongo(socket,camera_ip,port,fimg)
            except Exception as e:
                print(f"Error processing video: {e}")
                error_message = "Error processing video"
                alert_server(socket,camera_ip,port,error_message)

    print(f"Stopped event listener for camera {camera_ip}:{port}...")




def get_event_from_camera(camera_ip: str, port: int,demo:List[bool]) -> str: #with Fake-RTSP-Stream, we want to mimic one stream only, in deployment will need to change according to cameras protocol
# Example function for event notifications - we will need to replace with actual implementation
# do to constraints of time and hardware, we have left this "example" instead    
    if demo:
        return "light_detected"
    return "no_light_detected"


 

#connect to server
socket.connect("http://127.0.0.1:5000")

# Start listener for each camera
camera_info = [("10.0.0.1",8554,"concatenated-sample")] # future work - need to centrlize all the camera work and listing
threads = []
for ip, port,stream in camera_info:
    thread = threading.Thread(target=event_listen,
                    args=(socket, ip, port,stream,True), # we are in demo, so True
                    daemon=False) # since we have added join, we can use daemon = True, for now I will leave it as False for future work of improving this logic
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()  #block the main thread until all threads are done


