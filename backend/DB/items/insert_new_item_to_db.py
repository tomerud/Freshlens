from datetime import date, timedelta
import random
import mysql
from ..db_utils import get_db_connection

def insert_item_to_db(item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the item into the database
        cursor.execute("""
            INSERT INTO item (item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (item_id, is_inserted_by_user, product_id, camera_ip, date_entered, anticipated_expiry_date, is_rotten))
        conn.commit()

        print(f"✅ Item inserted: item_id={item_id}, product_id={product_id}, camera_ip={camera_ip}")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_all_products_from_db():
    """Fetch all products from the database and return a list of tuples (product_id, product_name, category_name)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""SELECT p.product_id, p.product_name, c.category_name
                    FROM freshlens.product p
                    join freshlens.categories c
                    on c.category_id = p.category_id""")
    products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return products

# Example usage
if __name__ == "__main__":
    
    # example_data = {
    #     "item_id": 3,
    #     "is_inserted_by_user": False,
    #     "product_id": 3,
    #     "camera_ip": "192.168.1.100",
    #     "date_entered": date.today(),
    #     "anticipated_expiry_date": date(2025, 1, 31),
    #     "is_rotten": False
    # }

    # insert_item_to_db(
    #     item_id=example_data["item_id"],
    #     is_inserted_by_user=example_data["is_inserted_by_user"],
    #     product_id=example_data["product_id"],
    #     camera_ip=example_data["camera_ip"],
    #     date_entered=example_data["date_entered"],
    #     anticipated_expiry_date=example_data["anticipated_expiry_date"],
    #     is_rotten=example_data["is_rotten"]
    # )

    products = get_all_products_from_db()


    selected_products = random.sample(products, 20)  # Pick 20 random products

    for i, (product_id, product_name, category_name) in enumerate(selected_products, start=1):
        # Generate realistic expiry dates based on category
        expiry_days = {
            "Dairy": 7,
            "Vegetables": 5,
            "Fruits": 6,
            "Meat": 4,
            "Beverages": 14,
            "Snacks": 30
        }
        days_to_expiry = expiry_days.get(category_name, 7)  # Default to 7 days if category is missing

        # Randomized values
        is_inserted_by_user = random.choice([True, False])
        camera_ip = f"192.168.1.100"
        date_entered = date.today() - timedelta(days=random.randint(0, 5))
        anticipated_expiry_date = date_entered + timedelta(days=days_to_expiry)
        is_rotten = random.choice([False, False, False, True])  # 75% chance not rotten

        insert_item_to_db(
            item_id=i,
            is_inserted_by_user=is_inserted_by_user,
            product_id=product_id,
            camera_ip=camera_ip,
            date_entered=date_entered,
            anticipated_expiry_date=anticipated_expiry_date,
            is_rotten=is_rotten
        )
