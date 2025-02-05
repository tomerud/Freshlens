# DB/user/insert_camera_to_db.py

import mysql

from ..db_utils import get_db_connection

def insert_camera_to_db(camera_ip, fridge_id):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the camera into the database
        cursor.execute("""
            INSERT INTO camera (camera_ip, fridge_id)
            VALUES (%s, %s)
        """, (camera_ip, fridge_id))
        conn.commit()

        print(f"Camera successfully inserted: camera_ip={camera_ip}, fridge_id={fridge_id}")
    
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
    example_camera_ip = "192.168.1.100"
    example_fridge_id = 1

    insert_camera_to_db(camera_ip=example_camera_ip, fridge_id=example_fridge_id)