from mysqlDB.db_utils import execute_query

def insert_item_to_db(item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, remove_from_fridge_date, is_rotten):
    execute_query("""
        INSERT INTO item (item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, remove_from_fridge_date, is_rotten )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, remove_from_fridge_date, is_rotten))
    
    print(f"Item inserted: item_id={item_id}, product_id={product_id}, camera_ip={camera_ip}")

def get_all_products_from_db():
    """Fetch all products from the database and return a list of tuples (product_id, product_name, category_name)."""
    
    products = execute_query("""SELECT p.product_id, p.product_name, c.category_name
                    FROM product_global_info p
                    join categories c
                    on c.category_id = p.category_id""")
    return products

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


def sync_items_for_camera(camera_ip, items):
    """
    1) Deletes from DB any items with this camera_ip that are NOT in 'items'.
    2) Inserts any new items from 'items' that do not exist in the DB.
    3) Updates any existing items with new values.
    """
    existing_records = get_items_by_camera_ip(camera_ip)
    existing_item_ids = {row[0] for row in existing_records}

    incoming_item_ids = {item["item_id"] for item in items}

    if incoming_item_ids:
        placeholders = ",".join(["%s"] * len(incoming_item_ids))
        query = f"""
            DELETE FROM item
             WHERE camera_ip = %s
               AND item_id NOT IN ({placeholders})
        """
        params = (camera_ip,) + tuple(incoming_item_ids)
        execute_query(query, params)
    else:
        execute_query("DELETE FROM item WHERE camera_ip = %s", (camera_ip,))

    for item in items:
        item_id = item["item_id"]
        product_id = item["product_id"]
        date_entered = item["date_entered"]
        anticipated_expiry_date = item["anticipated_expiry_date"]
        is_rotten = item["is_rotten"]

        if item_id not in existing_item_ids:
            insert_item_to_db(
                item_id=item_id,
                is_inserted_by_user=0,
                product_id=product_id,
                camera_ip=camera_ip,
                date_entered=date_entered,
                anticipated_expiry_date=anticipated_expiry_date,
                is_rotten=is_rotten
            )
        else:
            update_item_in_db(
                item_id=item_id,
                product_id=product_id,
                camera_ip=camera_ip,
                date_entered=date_entered,
                anticipated_expiry_date=anticipated_expiry_date,
                is_rotten=is_rotten
            )