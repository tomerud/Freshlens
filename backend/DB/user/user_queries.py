from ..db_utils import execute_query

def is_user_already_known_in_db(user_id):
    query = "SELECT count(*) FROM users WHERE user_id = %s"
    result = execute_query(query, (user_id,), fetch_one=True)
    return bool(result[0])

def update_user_subscription_in_db(user_id, new_subscription_id):
    query = "UPDATE users SET `subscription_id` = %s WHERE `user_id` = %s"
    execute_query(query, (new_subscription_id, user_id,))

    print(f"Subscription_id UPDATED successfully.")
