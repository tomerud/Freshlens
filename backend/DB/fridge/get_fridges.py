# check...

from mysql.connector import Error  # Ensure you're importing the right Error type
from ..db_utils import get_db_connection

def get_fridges_from_db(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT fridge_id, fridge_name FROM fridges WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchall()  # Fetch all results

    except Error as err:
        print(f"Database error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Example usage:
if __name__ == "__main__":
    # Replace with an actual user_id to test
    user_id = 1
    print(get_fridges_from_db(user_id))
