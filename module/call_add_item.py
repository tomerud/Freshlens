import requests
import json

# URL of your Flask backend endpoint
url = "http://127.0.0.1:5000/add_item"

# Data to be inserted into the database
data = {
    "product_id": 1,  # Replace with a valid product_id from your database
    "fridge_id": 2,   # Replace with a valid fridge_id from your database
    "date_entered": "2025-01-25",  # Format: YYYY-MM-DD
    "anticipated_expiry_date": "2025-02-01",  # Format: YYYY-MM-DD
    "is_rotten": 0    # 0 for not rotten, 1 for rotten
}

# Make the POST request
try:
    response = requests.post(url, json=data)

    # Check the response status
    if response.status_code == 200:
        print("Item successfully inserted!")
        print("Response:", json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to insert item. Status code: {response.status_code}")
        print("Error message:", response.text)
except Exception as e:
    print(f"An error occurred: {str(e)}")
