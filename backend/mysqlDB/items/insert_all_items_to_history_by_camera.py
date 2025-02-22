# File: backend/mysqlDB/items/insert_all_items_to_history_by_camera.py

"""
✅ **Check for __init__.py Files:**
Ensure the following directories contain an `__init__.py` file:

- `backend/`
- `backend/mysqlDB/`
- `backend/mysqlDB/items/`
- `backend/mysqlDB/camera/`

This allows Python to recognize these directories as packages, making relative imports work properly.

To create them (if missing), run:
```bash
touch backend/__init__.py
touch backend/mysqlDB/__init__.py
touch backend/mysqlDB/items/__init__.py
touch backend/mysqlDB/camera/__init__.py
```
Each `__init__.py` can be empty.

---
"""

from ..camera.get_items import get_items_by_camera_ip
from .insert_to_history import insert_to_history

def insert_all_items_to_history_by_camera(camera_ip):
    """
    Given a camera IP, retrieves all items associated with that camera and inserts each one into the user_product_history table.
    """
    items = get_items_by_camera_ip(camera_ip)

    if not items:
        print(f"No items found for camera_ip={camera_ip}.")
        return

    for item in items:
        item_id = item[0]  # item_id is the first element in the tuple
        insert_to_history(item_id)

    print(f"Inserted all items for camera_ip={camera_ip} into user_product_history.")

if __name__ == "__main__":
    camera_ip = "192.168.1.100"  # Hardcoded camera IP as requested
    insert_all_items_to_history_by_camera(camera_ip)
