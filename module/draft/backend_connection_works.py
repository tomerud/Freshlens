from socketio import Client
from datetime import datetime
import base64
import cv2

# Initialize the SocketIO client
socket = Client()

def sendToDB(camera_ip: str, expDate: list):
    # send data to the database, using socketIO
    
    data = {
        "camera_ip": camera_ip,
        "product_id": expDate[0],   
        "class_id": expDate[1],    
        "date_today": datetime.today().strftime("%Y-%m-%d"),
        "expdate": expDate[3]      
    }

    try:
        socket.emit("send_to_db", data)
        print(f"Data sent to backend for DB: {data}")
    except Exception as e:
        print(f"Error sending data to backend for DB: {e}")

#depends on tomer:
#from bson import Binary
def sendToMongo(camera_ip: str, image):
    # send the images with corresponding camera IP

    # Encode the image as a base64 string
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    # OR
    # _, buffer = cv2.imencode('.jpg', image)
    # image_binary = Binary(buffer)
    # data = {
    #     "camera_ip": camera_ip,
    #     "image": image_binary
    # }
    # etc

    data = {
        "camera_ip": camera_ip,
        "image": image_base64
    }

    
    try:
        socket.emit("send_to_mongo", data)
        print(f"Data sent to backend for MongoDB: {data}")
    except Exception as e:
        print(f"Error sending data to backend for MongoDB: {e}")

if __name__ == "__main__": # testing
    try:
        socket.connect("http://127.0.0.1:5000") 
        print("SocketIO connection established.")
    except Exception as e:
        print(f"Error connecting to SocketIO server: {e}")
        exit(1)

    # Example data for test
    camera_ip = "192.168.1.100"
    expDate = [1, 2, (100, 200, 300, 400), "2025-02-01"]  
    image = cv2.imread("example.jpg")  

    # Send data
    sendToDB(camera_ip, expDate)
    #sendToMongo(camera_ip, image)

    # Close the connection when done
    socket.disconnect()
    print("SocketIO connection closed.")
