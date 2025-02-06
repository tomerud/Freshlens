# DB/user/insert_user_to_db.py

from datetime import date
from time import strftime
from ..db_utils import execute_query

def insert_new_user(first_name, last_name, email, subscription_type):

    subscription_result = execute_query(
    "SELECT subscription_id FROM subscription WHERE subscription_name = %s",
    (subscription_type,), fetch_one=True)
    
    if not subscription_result:
        raise ValueError(f"Subscription type '{subscription_type}' does not exist.")
    subscription_id = subscription_result[0]

    execute_query("""
        INSERT INTO users (user_first_name, user_last_name, user_email, date_subscribed, subscription_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, last_name, email, date.today().strftime('%Y-%m-%d'), subscription_id))
    
    print(f"User '{first_name} {last_name}' added successfully.")
