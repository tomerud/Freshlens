import datetime
from flask import Blueprint, request, jsonify

app_bp = Blueprint('app_bp', __name__)


@app_bp.route('/data')
def get_time():
    return jsonify({
        'Name': "geek",
        'Age': "22",
        'Date': datetime.datetime.now()
    })