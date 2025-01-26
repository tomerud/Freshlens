from datetime import date
from time import strftime
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

        print(f"Item successfully inserted: item_id={item_id}, camera_ip={camera_ip}, product_id={product_id}")
    
    except mysql.connector.Error as err:
        print(f"Database error: {err.msg}")
        print(f"SQLState: {err.sqlstate}")
        print(f"Error Code: {err.errno}")
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Example usage
if __name__ == "__main__":
    from datetime import date
    
    example_data = {
        "item_id": 3,
        "is_inserted_by_user": False,
        "product_id": 3,
        "camera_ip": "192.168.1.100",
        "date_entered": date.today(),
        "anticipated_expiry_date": date(2025, 1, 31),
        "is_rotten": False
    }

    insert_item_to_db(
        item_id=example_data["item_id"],
        is_inserted_by_user=example_data["is_inserted_by_user"],
        product_id=example_data["product_id"],
        camera_ip=example_data["camera_ip"],
        date_entered=example_data["date_entered"],
        anticipated_expiry_date=example_data["anticipated_expiry_date"],
        is_rotten=example_data["is_rotten"]
    )
