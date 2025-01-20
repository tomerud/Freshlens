
from datetime import date
from time import strftime
import mysql
from ..db_utils import get_db_connection

def insert_new_shelf_to_db(fridge_id, shelf_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO shelves (fridge_id, shelf_name)
            VALUES (%s, %s)
        """, (fridge_id, shelf_name))
        conn.commit()

        print(f"Shelf '{shelf_name}' added successfully for fridge_id '{fridge_id}'.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Example usage: loop to insert multiple shelves for fridge IDs 1 to 4
if __name__ == "__main__":
    # Define a list of shelf names to insert for each fridge.
    shelf_names = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]

    # Loop through fridge IDs 1 to 4.
    for fridge_id in range(1, 5):
        for shelf_name in shelf_names:
            insert_new_shelf_to_db(fridge_id, shelf_name)

