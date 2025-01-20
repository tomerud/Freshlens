# DB/products/insert_products_to_db.py

from datetime import date
from time import strftime
import mysql
from ..db_utils import get_db_connection

def insert_new_product_to_db(product_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products (product_name)
            VALUES (%s)
        """, (product_name,))
        conn.commit()

        print(f"Product '{product_name}' added successfully.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Example usage
if __name__ == "__main__":
    # List of product names to insert
    product_list = [
        "apple", 
        "banana", 
        "kale", 
        "cottage cheese", 
        "milk", 
        "yogurt", 
        "orange", 
        "carrot",
        "spinach",
        "grapes"
    ]
    
    for product in product_list:
        insert_new_product_to_db(product)
