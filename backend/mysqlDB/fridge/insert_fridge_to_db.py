# mysql/user/insert_user_to_db.py

from mysqlDB.db_utils import execute_query

def insert_new_fridge_to_db(user_id, fridge_name):
    execute_query("""
        INSERT INTO fridges (user_id, fridge_name)
        VALUES (%s, %s)
    """, (user_id, fridge_name))

    print(f"Fridge '{fridge_name}' added successfully for user_id '{user_id}'.")

