from datetime import date
import mysql.connector
from .db_utils import get_db_connection

def insert_new_user(first_name, last_name, email, subscription_type):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get subscription_id from subscription table
        cursor.execute("SELECT subscription_id FROM subscription WHERE subscription_name = %s", (subscription_type,))
        subscription_result = cursor.fetchone()
        if not subscription_result:
            raise ValueError(f"Subscription type '{subscription_type}' does not exist.")
        subscription_id = subscription_result[0]

        # Insert new user into users table
        cursor.execute("""
            INSERT INTO users (user_first_name, user_last_name, date_subscribed, subscription_id)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, date.today().strftime('%Y-%m-%d'), subscription_id))
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

def insert_new_fridge(user_id, fridge_name):
    """
    Adds a new fridge to the fridges table for a given user_id and fridge_name.
    """
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the fridge into the fridges table
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


if __name__ == "__main__":
    insert_new_fridge(1, "work mini fridge")