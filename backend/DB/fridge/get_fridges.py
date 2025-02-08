from ..db_utils import execute_query

def get_fridges_from_db(user_id):
    query = "SELECT fridge_id, fridge_name FROM fridges WHERE user_id = %s"
    return execute_query(query, (user_id,))
