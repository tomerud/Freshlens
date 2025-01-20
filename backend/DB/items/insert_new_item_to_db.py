# DB/item/insert_item_to_db.py

from datetime import date, timedelta
from time import strftime
import mysql
from ..db_utils import get_db_connection

def insert_new_item_to_db(product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten):
    """
    Insert a new item into the item table.
    
    Parameters:
        product_id (int): The ID of the product.
        fridge_id (int): The ID of the fridge.
        shelf_id (int): The ID of the shelf.
        date_entered (str or date): The date when the item was entered into the system.
        anticipated_expiry_date (str or date): The date when the item is expected to expire.
        is_rotten (int): Typically 0 (false) or 1 (true).
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO item (product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten))
        conn.commit()

        print(f"Item inserted successfully: product_id '{product_id}', fridge_id '{fridge_id}', shelf_id '{shelf_id}'.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# # Example usage
# if __name__ == "__main__":
#     # Example data:
#     product_id = 5    # Example product id; adjust as needed
#     fridge_id = 1      # Example fridge id; adjust as needed
#     shelf_id = 2      # Example shelf id; adjust as needed
    
#     # Use today's date as the entry date
#     date_entered = date.today().isoformat()
    
#     # For example, set anticipated expiry date 7 days from now
#     anticipated_expiry_date = (date.today() + timedelta(days=7)).isoformat()
    
#     is_rotten = 0      # 0 for not rotten, 1 for rotten
    
#     # Insert the new item
#     insert_new_item_to_db(product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten)
