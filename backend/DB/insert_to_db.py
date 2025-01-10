from db_utils import get_db_connection

def insert_new_user(first_name, last_name, date_subscribed, subscription_type):
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 1: Get subscription_id from subscription table
        cursor.execute("SELECT subscription_id FROM subscription WHERE subscription_name = %s", (subscription_type,))
        subscription_result = cursor.fetchone()
        if not subscription_result:
            raise ValueError(f"Subscription type '{subscription_type}' does not exist.")
        subscription_id = subscription_result[0]

        # Step 2: Insert new user into users table
        cursor.execute("""
            INSERT INTO users (user_first_name, user_last_name, date_subscribed, subscription_id)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, date_subscribed, subscription_id))
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

# Example Usage
if __name__ == "__main__":
    insert_new_user("mimi", "df", "2025-01-11", "premium")
