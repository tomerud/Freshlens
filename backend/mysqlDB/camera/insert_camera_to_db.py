from backend.mysqlDB.db_utils import execute_query

def insert_camera_to_db(camera_ip, fridge_id):
    execute_query("""
        INSERT INTO camera (camera_ip, fridge_id)
        VALUES (%s, %s)
    """, (camera_ip, fridge_id))

    print(f"Camera successfully inserted: camera_ip={camera_ip}, fridge_id={fridge_id}")