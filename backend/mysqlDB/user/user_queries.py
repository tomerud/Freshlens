from backend.mysqlDB.db_utils import execute_query

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


from datetime import datetime, timedelta

def get_user_nutrition_consumption(user_id):

    last_week_date = datetime.now() - timedelta(days=7)
    query = """
        SELECT 
            COALESCE(SUM(pgi.energy_kcal), 0) AS total_energy_kcal,
            COALESCE(SUM(pgi.protein_g), 0) AS total_protein_g,
            COALESCE(SUM(pgi.fat_g), 0) AS total_fat_g,
            COALESCE(SUM(pgi.saturated_fat_g), 0) AS total_saturated_fat_g,
            COALESCE(SUM(pgi.carbs_g), 0) AS total_carbs_g,
            COALESCE(SUM(pgi.sugars_g), 0) AS total_sugars_g,
            COALESCE(SUM(pgi.fiber_g), 0) AS total_fiber_g,
            COALESCE(SUM(pgi.sodium_mg), 0) AS total_sodium_mg
        FROM item i
        JOIN camera c ON i.camera_ip = c.camera_ip
        JOIN fridges f ON c.fridge_id = f.fridge_id
        JOIN product_global_info pgi ON i.product_id = pgi.product_id
        WHERE f.user_id = %s AND i.remove_from_fridge_date >= %s
    """
    result = execute_query(query, (user_id, last_week_date), fetch_one=True)
    return result or {}

if __name__ == "__main__":
    users=["vcfzeUDAuMjEmFTI2HYuQhBMVUH","0NNRFLhbXJRFk3ER2_iTr8VulFm4","ETqCemxYH7HP135eIMoLnIO9H1tm","iWOBibVuFhg3svYbFqxNIM34Drrf"]
    for user in users:
        print("----------------")
        print(get_user_nutrition_consumption(user))
        print("----------------")

