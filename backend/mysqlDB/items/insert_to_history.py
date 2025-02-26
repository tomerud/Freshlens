from datetime import date
from ..db_utils import execute_query

def insert_to_history(item_id):
    item = execute_query("""
        SELECT product_id, 
               (SELECT user_id 
                FROM fridges f 
                JOIN camera c ON f.fridge_id = c.fridge_id 
                WHERE c.camera_ip = i.camera_ip) AS user_id, 
               anticipated_expiry_date
        FROM item i
        WHERE item_id = %s
    """, (item_id,), fetch_one=True)
    if not item:
        print(f"Item with item_id={item_id} not found.")
        return
    is_thrown = 0
    product_id = item['product_id']
    user_id = item['user_id']
    anticipated_expiry_date = item['anticipated_expiry_date']
    current_date = date.today()
    if anticipated_expiry_date:
        if anticipated_expiry_date > current_date:
            is_thrown = 1
    execute_query("""
        INSERT INTO user_product_history (user_id, product_id, is_thrown, date_entered)
        VALUES (%s, %s, %s, %s)
    """, (user_id, product_id, is_thrown, current_date))
    print(f"Inserted into user_product_history: user_id={user_id}, product_id={product_id}, is_thrown={is_thrown}, date_entered={current_date}")