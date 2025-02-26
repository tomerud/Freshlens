from datetime import datetime
from ..camera.get_items import get_items_by_camera_ip
from ..items.insert_to_history import insert_to_history
from ..items.insert_new_item_to_db import insert_item_to_db  
from ..db_utils import execute_query 


def delete_item_by_camera_and_item_id(camera_ip, item_id):
    """Deletes a single item with the given camera IP and item_id from the 'item' table."""
    execute_query("""
        DELETE FROM item
        WHERE camera_ip = %s AND item_id = %s
    """, (camera_ip, item_id))
    print(f"Deleted item_id={item_id} for camera_ip={camera_ip} from the database.")


def handle_camera_update(camera_ip, item_list):
    """
    Handles a camera update:
    1. Retrieves current DB items with the given camera IP.
    2. For each DB item:
         - If it is not in the new item_list, insert it into history and delete it.
         - If it is in the new item_list, delete it (so it can be reinserted) but keep its previous date_entered.
    3. Inserts items from item_list:
         - For items that existed previously, uses their old date_entered.
         - For new items, uses the current date.
    4. For each inserted item, sets is_rotten to 1 if the current date is greater than its anticipated expiry date; otherwise 0.

    Args:
        camera_ip (str): The IP address of the camera.
        item_list (list): List of dictionaries representing new items to insert.
    """
    # Step 1: Retrieve current DB items for this camera and build a lookup dictionary.
    current_items = get_items_by_camera_ip(camera_ip)
    existing_map = {item['item_id']: item for item in current_items if 'item_id' in item}
    new_item_ids = {item['item_id'] for item in item_list if 'item_id' in item}

    # Step 2: Process current items in DB.
    for current_item in current_items:
        current_id = current_item.get('item_id')
        if current_id not in new_item_ids:
            print(f"Inserting item_id={current_id} into history before deletion (item not in new list).")
            insert_to_history(current_id)
            delete_item_by_camera_and_item_id(camera_ip, current_id)
        else:
            # Item exists in both DB and new list; delete from DB to reinsert with previous date_entered.
            print(f"Deleting item_id={current_id} from DB to update with previous date_entered.")
            delete_item_by_camera_and_item_id(camera_ip, current_id)

    # Step 3: Insert items from the new list.
    if not item_list:
        print(f"No new items to insert for camera_ip={camera_ip}.")
        return

    now = datetime.now()
    for item in item_list:
        required_fields = [
            'item_id', 'is_inserted_by_user', 'product_id', 
            'camera_ip', 'date_entered', 'anticipated_expiry_date'
        ]
        missing_fields = [field for field in required_fields if field not in item]
        if missing_fields:
            print(f"Warning: Missing required fields {missing_fields} in item: {item}. Skipping insertion.")
            continue

        # For items that existed before, use the previous date_entered; otherwise, use current date.
        if item['item_id'] in existing_map:
            date_entered = existing_map[item['item_id']]['date_entered']
            print(f"Using previous date_entered for item_id={item['item_id']}: {date_entered}")
        else:
            date_entered = now.strftime("%Y-%m-%d")
            print(f"Using current date_entered for new item_id={item['item_id']}: {date_entered}")

        # Parse anticipated_expiry_date if it's a string.
        anticipated_date = item['anticipated_expiry_date']
        if isinstance(anticipated_date, str):
            try:
                anticipated_date_obj = datetime.fromisoformat(anticipated_date)
            except ValueError:
                print(f"Warning: Invalid date format for anticipated_expiry_date in item: {item}. Skipping insertion.")
                continue
        else:
            anticipated_date_obj = anticipated_date

        # Determine if the item is rotten based on the current date.
        is_rotten = 1 if now > anticipated_date_obj else 0

        insert_item_to_db(
            item_id=item['item_id'],
            is_inserted_by_user=item['is_inserted_by_user'],
            product_id=item['product_id'],
            camera_ip=item['camera_ip'],
            date_entered=date_entered,
            anticipated_expiry_date=item['anticipated_expiry_date'],
            remove_from_fridge_date= item['anticipated_expiry_date'], # for now, improvements in the next generation.
            is_rotten=is_rotten
        )
        print(f"Inserted item_id={item['item_id']} into the database with is_rotten={is_rotten} and date_entered={date_entered}.")

    print(f"Camera update processed for camera_ip={camera_ip}: "
          f"{len([i for i in current_items if i['item_id'] not in new_item_ids])} items inserted into history and deleted, "
          f"{len(item_list)} items inserted (including updates for existing items).")
