# DB/user/insert_user_to_db.py

from datetime import date
from time import strftime
import mysql
from ..db_utils import get_db_connection

def insert_new_fridge(user_id, fridge_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO fridges (user_id, fridge_name)
            VALUES (%s, %s)
        """, (user_id, fridge_name))
        conn.commit()

        print(f"Fridge '{fridge_name}' added successfully for user_id '{user_id}'.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


