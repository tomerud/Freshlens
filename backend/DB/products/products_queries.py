# DB/products/product_queries.py

import mysql
from ..db_utils import get_db_connection


def get_all_categories_from_db(fridge_id):
    """
    Retrieves all categories from the `categories` table.

    Returns:
        list: A list of tuples containing category data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT distinct c.category_id, c.category_name
            FROM categories c
            JOIN product p ON c.category_id = p.category_id
            JOIN item i ON p.product_id = i.product_id
            JOIN camera ca ON i.camera_ip = ca.camera_ip
            WHERE ca.fridge_id = %s
        """, (fridge_id,))

        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Database error: {err.msg}")
        print(f"SQLState: {err.sqlstate}")
        print(f"Error Code: {err.errno}")
        return []

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_fridge_products_by_category_from_db(fridge_id, category_name):
    """
    Retrieves all fridge products from a category

    Returns:
        list: A list of tuples containing product data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.product_id, p.product_name
            FROM categories c
            JOIN product p ON c.category_id = p.category_id
            JOIN item i ON p.product_id = i.product_id
            JOIN camera ca ON i.camera_ip = ca.camera_ip
            WHERE ca.fridge_id = %s and c.category_name = %s
        """, (fridge_id, category_name))

        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Database error: {err.msg}")
        print(f"SQLState: {err.sqlstate}")
        print(f"Error Code: {err.errno}")
        return []

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_fridge_product_items_from_db(fridge_id, product_id):
    """
    Retrieves all fridge items from specific product

    Returns:
        list: A list of tuples containing items.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.product_name, i.is_rotten 
            FROM freshlens.product p
            JOIN freshlens.item i ON p.product_id = i.product_id
            JOIN freshlens.camera ca ON i.camera_ip = ca.camera_ip
            WHERE ca.fridge_id = %s and p.product_id = %s
        """, (fridge_id, product_id))

        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Database error: {err.msg}")
        print(f"SQLState: {err.sqlstate}")
        print(f"Error Code: {err.errno}")
        return []

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()