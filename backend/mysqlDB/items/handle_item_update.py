from ..camera.get_items import get_items_by_camera_ip
from ..items.insert_to_history import insert_to_history
from ..items.insert_new_item_to_db import insert_item_to_db  
from ..db_utils import execute_query 


def delete_all_items_by_camera_ip(camera_ip):
    """Deletes all items associated with the given camera IP from the 'item' table."""
    execute_query("""
        DELETE FROM item
        WHERE camera_ip = %s
    """, (camera_ip,))
    print(f"Deleted all items for camera_ip={camera_ip} from the database.")


def handle_camera_update(camera_ip, item_list):
    """
    Handles a camera update:
    1. Compares existing DB items with the new item_list and inserts missing items into history.
    2. Deletes all items associated with the camera_ip.
    3. Inserts new items from the item_list into the 'item' table.

    Args:
        camera_ip (str): The IP address of the camera.
        item_list (list): List of dictionaries representing new items to insert.
    """
    # Step 1: Compare current DB items with the new item_list
    current_items = get_items_by_camera_ip(camera_ip)
    item_list_ids = {item['item_id'] for item in item_list if 'item_id' in item}
    current_item_ids = {item['item_id'] for item in current_items if 'item_id' in item}

    # Items to insert into history: Items in DB but not in the new item list
    items_to_insert_into_history = current_item_ids - item_list_ids

    for item_id in items_to_insert_into_history:
        print(f"Inserting item_id={item_id} into history.")
        insert_to_history(item_id)

    # Step 2: Delete all items associated with this camera, easiear than checkinjg for chenges in evry single item.
    delete_all_items_by_camera_ip(camera_ip)

    # Step 3: Insert new items into the 'item' table
    if not item_list:
        print(f"No new items to insert for camera_ip={camera_ip}.")
        return

    for item in item_list:
        required_fields = ['item_id', 'is_inserted_by_user', 'product_id', 'camera_ip', 'date_entered', 'anticipated_expiry_date']
        missing_fields = [field for field in required_fields if field not in item]

        if missing_fields:
            print(f"Warning: Missing required fields {missing_fields} in item: {item}. Skipping insertion.")
            continue

        insert_item_to_db(
            item_id=item['item_id'],
            is_inserted_by_user=item['is_inserted_by_user'],
            product_id=item['product_id'],
            camera_ip=item['camera_ip'],
            date_entered=item['date_entered'],
            anticipated_expiry_date=item['anticipated_expiry_date'],
            remove_from_fridge_date=item.get('remove_from_fridge_date'),
            is_rotten=item.get('is_rotten', 0)
        )
        print(f"Inserted item_id={item['item_id']} into the database.")

    print(f"Camera update processed for camera_ip={camera_ip}: "
          f"{len(items_to_insert_into_history)} items inserted into history, "
          f"{len(item_list)} new items inserted.")


if __name__ == "__main__":
    camera_ip = "192.168.1.100"

    # Example new item list from the camera
    new_items = [
        {
            "item_id": 1,
            "is_inserted_by_user": 1,
            "product_id": 45,
            "camera_ip": camera_ip,
            "date_entered": "2025-02-20",
            "anticipated_expiry_date": "2025-02-24",
            "remove_from_fridge_date": None,
            "is_rotten": 0
        },
        {
            "item_id": 2,
            "is_inserted_by_user": 0,
            "product_id": 46,
            "camera_ip": camera_ip,
            "date_entered": "2025-02-21",
            "anticipated_expiry_date": "2025-02-25",
            "remove_from_fridge_date": None,
            "is_rotten": 0
        }
    ]

    handle_camera_update(camera_ip, new_items)
