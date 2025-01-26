# DB/products/insert_products_to_db.py

from datetime import date
from time import strftime
import mysql
from ..db_utils import get_db_connection


def insert_category(category_name):
    """
    Inserts a new category into the `categories` table.

    Args:
        category_name (str): The name of the category.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the category into the database
        cursor.execute("""
            INSERT INTO categories (category_name)
            VALUES (%s)
        """, (category_name,))
        conn.commit()
        print(f"Category '{category_name}' inserted successfully.")
    
    except mysql.connector.Error as err:
        print(f"Database error: {err.msg}")
        print(f"SQLState: {err.sqlstate}")
        print(f"Error Code: {err.errno}")
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


def insert_product(product_name, category_id):
    """
    Inserts a new product into the `product` table.

    Args:
        product_name (str): The name of the product.
        category_id (int): The ID of the category the product belongs to.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the product into the database
        cursor.execute("""
            INSERT INTO product (product_name, category_id)
            VALUES (%s, %s)
        """, (product_name, category_id))
        conn.commit()
        print(f"Product '{product_name}' inserted successfully under category_id={category_id}.")
    
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
    # Insert categories
    categories = ["Dairy", "Vegetables", "Fruits", "Meat", "Beverages", "Snacks"]
    for category in categories:
        insert_category(category)

    # Insert products
    products = [
        {"product_name": "Milk", "category_name": "Dairy"},
        {"product_name": "Cheese", "category_name": "Dairy"},
        {"product_name": "Carrot", "category_name": "Vegetables"},
        {"product_name": "Apple", "category_name": "Fruits"},
        {"product_name": "Chicken", "category_name": "Meat"},
        {"product_name": "Cola", "category_name": "Beverages"},
        {"product_name": "Chips", "category_name": "Snacks"}
    ]

    # Insert products with corresponding category_id
    for product in products:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get the category_id from the categories table
        cursor.execute("""
            SELECT category_id FROM categories WHERE category_name = %s
        """, (product["category_name"],))
        category_id = cursor.fetchone()[0]

        # Insert the product
        insert_product(product["product_name"], category_id)
        
        cursor.close()
        conn.close()
