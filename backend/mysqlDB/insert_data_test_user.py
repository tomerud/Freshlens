from mysqlDB.user.insert_user_to_db import insert_new_user
from mysqlDB.fridge.insert_fridge_to_db import insert_new_fridge_to_db
from mysqlDB.camera.insert_camera_to_db import insert_camera_to_db
from mysqlDB.items.insert_new_item_to_db import insert_item_to_db
from mysqlDB.db_utils import execute_query
from datetime import date, timedelta
import random

def insert_test_data():
    # Insert User
    user_id = "test_user_id_123"
    user_name = "Test User"
    user_email = "test.user@example.com"
    subscription_type = "free"  # Assuming "free" is a valid subscription type
    insert_new_user(user_id, user_name, user_email, subscription_type)
    print(f"Inserted new user: {user_name} with email: {user_email}")

    # Insert Fridge
    fridge_name = "Test User's Fridge"
    insert_new_fridge_to_db(user_id, fridge_name)
    print(f"Inserted new fridge: {fridge_name} for user: {user_name}")

    # Retrieve the fridge_id for the inserted fridge
    fridge_query = "SELECT fridge_id FROM fridges WHERE user_id = %s AND fridge_name = %s"
    fridge_result = execute_query(fridge_query, (user_id, fridge_name), fetch_one=True)

    if not fridge_result:
        print("Error: Could not retrieve fridge_id.")
        return

    fridge_id = fridge_result['fridge_id']
    print(f"Retrieved fridge_id: {fridge_id} for fridge: {fridge_name}")

    # Insert Camera
    camera_ip = "192.168.1.200"
    insert_camera_to_db(camera_ip=camera_ip, fridge_id=fridge_id)
    print(f"Inserted new camera with IP: {camera_ip} for fridge_id: {fridge_id}")

    # Insert Items
    for i in range(1, 4):
        product_id = i  # Replace with actual product_id from your database
        is_inserted_by_user = True
        date_entered = date.today() - timedelta(days=random.randint(0, 5))
        anticipated_expiry_date = date_entered + timedelta(days=random.randint(5, 10))
        remove_from_fridge_date = date_entered + timedelta(days=random.randint(1, 12))
        is_rotten = random.choice([False, True])

        insert_item_to_db(
            item_id=i + 6666,
            is_inserted_by_user=is_inserted_by_user,
            product_id=product_id,
            camera_ip=camera_ip,
            date_entered=date_entered,
            anticipated_expiry_date=anticipated_expiry_date,
            remove_from_fridge_date=remove_from_fridge_date,
            is_rotten=is_rotten
        )
        print(f"Inserted item {i} with product_id {product_id} into fridge_id {fridge_id}")

if __name__ == "__main__":
    insert_test_data()
