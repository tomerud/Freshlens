"""
This module contain calling to other function, in order to allow us "play" with the app-module
and see results
"""

import socketio

from ultralytics import YOLO
from module.detect_and_track import process_video
from module.backend_connect import send_to_db, send_to_mongo, alert_server
from module.pass_obj_to_exp_date import find_exp_date
from module.draw_bb import draw_on_image


# # Setup socketIO client - I ahve updated the setup, need to check updated version
# socket_client = socketio.Client(
#     reconnection=True,
#     reconnection_attempts=10,
#     reconnection_delay=1,
#     reconnection_delay_max=30,
#     ssl_verify=False
# )  # Client will attempt to reconnect when disconnected.

# @socket_client.event
# def connect():
#     print(f"Connected to SocketIO server.")

# @socket_client.event
# def disconnect():
#     print(f"Disconnected from SocketIO server.")

# # Connect to SocketIO before threads start
# def connect_to_socket():
#     try:
#         socket_client.connect("wss://127.0.0.1:5000",transports=["websocket"]) 
#         print("SocketIO connected.")
#     except Exception as e:
#         print(f"Error connecting to SocketIO server: {e}")

# connect_to_socket()

# # set up the camera IP and port - this is connected to the user id!
# cam_ip = "10.0.0.1"
# cam_port=8554

# dont change this:
MODEL_PATH = "../models/object_detect_v8.pt" 
detection_model = YOLO(MODEL_PATH)
class_list = [class_name for _, class_name in sorted(detection_model.names.items())]

# can change to any video path
PATH="../assets/freshlens2.MP4"

# dont change - this is the pipeline
# if want to see the tracking video, change the False to True
detections = process_video(PATH,detection_model,False)
# if detections in (-1, None):
#     alert_server(socket_client, cam_ip, cam_port, "Error: Unable to open video stream.")
# else:    
#     exp_date = find_exp_date(detections, class_list)
#     fimg = draw_on_image(exp_date)
#     send_to_db(socket_client, cam_ip, cam_port, exp_date)
#     send_to_mongo(socket_client, cam_ip, cam_port, fimg)
print(detections)