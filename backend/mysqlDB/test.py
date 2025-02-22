from datetime import date, timedelta
import random

from mysqlDB.camera.insert_camera_to_db import insert_camera_to_db
from mysqlDB.fridge.insert_fridge_to_db import insert_new_fridge_to_db
from mysqlDB.items.insert_new_item_to_db import get_all_products_from_db, insert_item_to_db
from mysqlDB.products.insert_new_products_to_db import insert_new_category_to_db, insert_new_product_to_db, load_canadian_prices_from_kaggle, load_storage_tips
from mysqlDB.user.insert_user_to_db import insert_new_user
from mysqlDB.db_utils import execute_query

def get_items_by_camera_ip(camera_ip):
    items = execute_query("""
        SELECT item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten
        FROM item
        WHERE camera_ip = %s
    """, (camera_ip,))
    return items

def update_item_in_db(item_id, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten):
    execute_query("""
        UPDATE item
        SET product_id = %s,
            camera_ip = %s,
            date_entered = %s,
            anticipated_expiry_date = %s,
            is_rotten = %s
        WHERE item_id = %s
    """, (product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten, item_id))
    print(f"Item {item_id} updated successfully.")

def sync_items_with_camera(camera_ip, new_items):
    """
    Sync items for a given camera IP:
    1. Remove all existing items with the specified camera_ip.
    2. Insert the new list of items.

    Args:
        camera_ip (str): The camera IP to sync items with.
        new_items (list of dict): Each dict should contain keys: product_id, date_entered, anticipated_expiry_date, is_rotten.
    """
    # Remove existing items
    execute_query("DELETE FROM item WHERE camera_ip = %s", (camera_ip,))
    print(f"Removed all existing items for camera_ip: {camera_ip}")

    # Get the current max item_id to avoid primary key conflicts
    result = execute_query("SELECT MAX(item_id) AS max_id FROM item", fetch_one=True)
    start_id = (result['max_id'] or 0) + 1

    inserted_item_ids = []

    # Insert new items
    for i, item in enumerate(new_items, start=start_id):
        insert_item_to_db(
            item_id=i,
            is_inserted_by_user=True,
            product_id=item['product_id'],
            camera_ip=camera_ip,
            date_entered=item['date_entered'],
            anticipated_expiry_date=item['anticipated_expiry_date'],
            remove_from_fridge_date=item.get('remove_from_fridge_date'),
            is_rotten=item['is_rotten']
        )
        inserted_item_ids.append(i)
        print(f"Inserted item {i} with product_id {item['product_id']} for camera_ip: {camera_ip}")

    return inserted_item_ids

if __name__ == "__main__":
    camera_ip = "192.168.1.200"

    # Example usage of sync function with sample items
    new_items = [
        {
            "product_id": 1,
            "date_entered": date(2025, 2, 20),
            "anticipated_expiry_date": date(2025, 2, 27),
            "remove_from_fridge_date": date(2025, 2, 25),
            "is_rotten": False
        },
        {
            "product_id": 2,
            "date_entered": date(2025, 2, 21),
            "anticipated_expiry_date": date(2025, 3, 1),
            "remove_from_fridge_date": date(2025, 2, 28),
            "is_rotten": False
        },
        {
            "product_id": 3,
            "date_entered": date(2025, 2, 22),
            "anticipated_expiry_date": date(2025, 3, 2),
            "remove_from_fridge_date": date(2025, 3, 1),
            "is_rotten": True
        }
    ]

    print("Before syncing:")
    items_before = get_items_by_camera_ip(camera_ip)
    print(items_before)

    inserted_ids = sync_items_with_camera(camera_ip, new_items)

    print("\nInserted item IDs:", inserted_ids)

    print("\nAfter syncing:")
    items_after = get_items_by_camera_ip(camera_ip)
    print(items_after)