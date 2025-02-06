from ..db_utils import execute_query


def get_all_categories_from_db(fridge_id):
    """
    Retrieves all categories from the `categories` table.

    Returns:
        list: A list of tuples containing category data.
    """
    return execute_query("""
        SELECT distinct c.category_id, c.category_name
        FROM categories c
        JOIN product p ON c.category_id = p.category_id
        JOIN item i ON p.product_id = i.product_id
        JOIN camera ca ON i.camera_ip = ca.camera_ip
        WHERE ca.fridge_id = %s
    """, (fridge_id,))

def get_fridge_products_by_category_from_db(fridge_id, category_name):
    """
    Retrieves all fridge products from a category

    Returns:
        list: A list of tuples containing product data.
    """
    return execute_query("""
        SELECT p.product_id, p.product_name
        FROM categories c
        JOIN product p ON c.category_id = p.category_id
        JOIN item i ON p.product_id = i.product_id
        JOIN camera ca ON i.camera_ip = ca.camera_ip
        WHERE ca.fridge_id = %s and c.category_name = %s
    """, (fridge_id, category_name))

def get_fridge_product_items_from_db(fridge_id, product_id):
    """
    Retrieves all fridge items from specific product

    Returns:
        list: A list of tuples containing items.
    """
    return execute_query("""
        SELECT p.product_name, i.is_rotten 
        FROM freshlens.product p
        JOIN freshlens.item i ON p.product_id = i.product_id
        JOIN freshlens.camera ca ON i.camera_ip = ca.camera_ip
        WHERE ca.fridge_id = %s and p.product_id = %s
    """, (fridge_id, product_id))