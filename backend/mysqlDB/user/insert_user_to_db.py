from datetime import date
from time import strftime
from backend.mysqlDB.db_utils import execute_query

def insert_new_user(user_id, user_name, email, subscription_type):
    subscription_result = execute_query(
    "SELECT subscription_id FROM subscription WHERE subscription_name = %s",
    (subscription_type,), fetch_one=True)
    
    if not subscription_result:
        raise ValueError(f"Subscription type '{subscription_type}' does not exist.")
    subscription_id = subscription_result['subscription_id']

    execute_query("""
        INSERT INTO users (user_id, user_name, user_email, date_subscribed, subscription_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, user_name, email, date.today().strftime('%Y-%m-%d'), subscription_id))
    
    print(f"User '{user_name}' added successfully.")
