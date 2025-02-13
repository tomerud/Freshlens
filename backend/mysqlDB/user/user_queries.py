from ..db_utils import execute_query

def is_user_already_known_in_db(user_id):
    query = "SELECT count(*) as cnt FROM users WHERE user_id = %s"
    result = execute_query(query, (user_id,), fetch_one=True)
    return bool(result['cnt'])

def update_user_subscription_in_db(user_id, new_subscription_id):
    query = "UPDATE users SET `subscription_id` = %s WHERE `user_id` = %s"
    execute_query(query, (new_subscription_id, user_id,))

    print(f"Subscription_id UPDATED successfully.")


def get_user_camera_ips(user_id):
    query = """SELECT f.fridge_id, f.fridge_name, c.camera_ip
                FROM fridges f
                join camera c
                on c.fridge_id = f.fridge_id 
                WHERE f.user_id = %s"""
    return execute_query(query, (user_id,)) or []
