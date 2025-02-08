import socketio
from Backend_connect import sendToDB,sendToMongo
# Setup socketIO client - I ahve updated the setup, need to check updated version
socket = socketio.Client()

@socket.event
def connect():
    print(f"Connected to SocketIO server.")

@socket.event
def disconnect():
    print(f"Disconnected from SocketIO server.")

# Connect to SocketIO before threads start
def connect_to_socket():
    try:
        socket.connect("http://127.0.0.1:5000",transports=["websocket"]) 
        print("SocketIO connected.")
    except Exception as e:
        print(f"Error connecting to SocketIO server: {e}")

connect_to_socket()
camera_ip = "10.0.0.1"
port=8554
expDate = [1, 2, (100, 200, 300, 400), "2025-02-01"]
sendToDB(socket,camera_ip,port, expDate)
#image = cv2.imread("example.jpg")
#sendToMongo(camera_ip, image)