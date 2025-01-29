from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("send_to_db")
def handle_send_to_db(data):
    print("Received data for DB:", data)
    # Handle the data 
    
@socketio.on("send_to_mongo")
def handle_send_to_mongo(data):
    # decide how you want the data to be encoded / sent
    # Handle the data
    return

if __name__ == "__main__":
    print("Starting Flask-SocketIO server on port 5000...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
