from datetime import date
from mysqlDB.db_utils import execute_query

def insert_to_history(item_id):
    """
    Inserts a record into user_product_history with is_thrown = 1 if the current date 
    is after the anticipated expiry date of the item, otherwise inserts with is_thrown = 0.
    Also records the current date in the date_entered column.
    """
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

    product_id = item['product_id']
    user_id = item['user_id']
    anticipated_expiry_date = item['anticipated_expiry_date']
    is_thrown = 1 if date.today() > anticipated_expiry_date else 0
    current_date = date.today()

    execute_query("""
        INSERT INTO user_product_history (user_id, product_id, is_thrown, date_entered)
        VALUES (%s, %s, %s, %s)
    """, (user_id, product_id, is_thrown, current_date))

    print(f"Inserted into user_product_history: user_id={user_id}, product_id={product_id}, is_thrown={is_thrown}, date_entered={current_date}")
