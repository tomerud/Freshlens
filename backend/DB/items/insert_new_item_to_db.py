from DB.db_utils import execute_query

def insert_item_to_db(item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten):
    execute_query("""
        INSERT INTO item (item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten))
    
    print(f"Item inserted: item_id={item_id}, product_id={product_id}, camera_ip={camera_ip}")

def get_all_products_from_db():
    """Fetch all products from the database and return a list of tuples (product_id, product_name, category_name)."""
    
    products = execute_query("""SELECT p.product_id, p.product_name, c.category_name
                    FROM freshlens.product p
                    join freshlens.categories c
                    on c.category_id = p.category_id""")
    return products