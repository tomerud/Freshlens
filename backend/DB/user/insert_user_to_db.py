# DB/user/insert_user_to_db.py

from datetime import date
from time import strftime
import mysql.connector
from ..db_utils import get_db_connection

def insert_new_user(first_name, last_name, email, subscription_type):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT subscription_id FROM subscription WHERE subscription_name = %s",
            (subscription_type,)
        )
        subscription_result = cursor.fetchone()
        if not subscription_result:
            raise ValueError(f"Subscription type '{subscription_type}' does not exist.")
        subscription_id = subscription_result[0]

        cursor.fetchall()
        cursor.execute("""
            INSERT INTO users (user_first_name, user_last_name, user_email, date_subscribed, subscription_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, date.today().strftime('%Y-%m-%d'), subscription_id))
        
        conn.commit()
        print(f"User '{first_name} {last_name}' added successfully.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except ValueError as ve:
        print(f"Value error: {ve}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
