from flask import Flask, jsonify, request
import datetime

from DB.insert_to_db import insert_new_user

app = Flask(__name__)


@app.route('/data')
def get_time():

    return jsonify({
        'Name':"geek", 
        "Age":"22",
        "Date":datetime.datetime.now(), 
         })

@app.route('/sign_user', methods=['POST'])
def sign_user():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    if "@" not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400

    insert_new_user(data["firstName"], data["lastName"], data["email"], data["subscription"])

    return jsonify({"message": "User signed up successfully!", "data": data}), 200
    
if __name__ == '__main__':
    app.run(debug=True)