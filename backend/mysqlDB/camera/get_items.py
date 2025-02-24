from ..db_utils import execute_query

def get_items_by_camera_ip(camera_ip):
    items = execute_query("""
        SELECT item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten
          FROM item
         WHERE camera_ip = %s
    """, (camera_ip,))
    return items