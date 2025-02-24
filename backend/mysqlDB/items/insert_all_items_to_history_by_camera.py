from ..camera.get_items import get_items_by_camera_ip
from ..items.insert_to_history import insert_to_history  # Correct relative import

def insert_all_items_to_history_by_camera(camera_ip):
    """
    Retrieves all items associated with the given camera IP and inserts them into user_product_history.
    """
    items = get_items_by_camera_ip(camera_ip)

    if not items:
        print(f"No items found for camera_ip={camera_ip}.")
        return

    for item in items:
        print(f"Processing item: {item}")
        item_id = item.get('item_id')
        if item_id:
            insert_to_history(item_id)
        else:
            print(f"Warning: 'item_id' not found in item: {item}")

    print(f"Inserted all items for camera_ip={camera_ip} into user_product_history.")

if __name__ == "__main__":
    camera_ip = "192.168.1.100"  # Hardcoded camera IP
    insert_all_items_to_history_by_camera(camera_ip)
