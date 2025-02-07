from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("send_to_db")
def handle_send_to_db(data):
    """ you get camera Ip, port and a list
    [(product_id,class_id,exp date)]
    format of exp date -> with Elya!

    """
    # Handle the data 
    print("Received data for DB:", data)
    
    
@socketio.on("send_to_mongo")
def handle_send_to_mongo(data):
    """ you get camera Ip, port and an image
    decide how you want the data to be encoded / sent - image_base64, image_Binary, nparray etc
    """
    # 
    # Handle the data
    return

if __name__ == "__main__":
    print("Starting Flask-SocketIO server on port 5000...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
