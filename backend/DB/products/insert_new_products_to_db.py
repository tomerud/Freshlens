# DB/products/insert_new_products_to_db.py

from ..db_utils import execute_query

def insert_new_category_to_db(category_name):
    """
    Inserts a new category into the `categories` table.

    Args:
        category_name (str): The name of the category.
    """

    execute_query("""
        INSERT INTO categories (category_name)
        VALUES (%s)
    """, (category_name,))
    
    print(f"Category '{category_name}' inserted successfully.")

def insert_new_product_to_db(product_name, category_id):
    """
    Inserts a new product into the `product` table.

    Args:
        product_name (str): The name of the product.
        category_id (int): The ID of the category the product belongs to.
    """
    execute_query("""
        INSERT INTO product (product_name, category_id)
        VALUES (%s, %s)
    """, (product_name, category_id))

    print(f"Product '{product_name}' inserted successfully under category_id={category_id}.")