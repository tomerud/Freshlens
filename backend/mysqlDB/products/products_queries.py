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
        JOIN product_global_info p ON c.category_id = p.category_id
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
        JOIN product_global_info p ON c.category_id = p.category_id
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
        SELECT i.item_id, i.is_rotten, i.date_entered, i.anticipated_expiry_date
        FROM item i
        JOIN camera ca ON i.camera_ip = ca.camera_ip
        WHERE ca.fridge_id = %s and i.product_id = %s
    """, (fridge_id, product_id))


def get_product_nutrient_data(product_id):
    """
    Retrieves all product nutrient data from specific product

    Returns:
        list: A list of tuples containing items.
    """
    return execute_query("""
        SELECT *
        FROM product_global_info p
        WHERE p.product_id = %s
    """, (product_id,))


def get_product_price_from_db(product_id):
    """
    Retrieves all product nutrient data from specific product

    Returns:
        list: A list of tuples containing items.
    """
    return execute_query("""
        SELECT p.product_name, AVG(c.price) as avg_price
        FROM product_global_info p 
        join canadian_products_prices c
        on c.name like concat('%', p.product_name, '%')
        WHERE p.product_id = %s
        group by p.product_name
    """, (product_id,))


def get_specific_product_tips_from_db(product_id):
    return execute_query("""
        SELECT p.product_name, t.refrigerate_tips, t.freeze_tips
        from product_global_info p
        join food_storage_tips t
        on t.product_name like concat('%' , p.product_name, '%' ) 
        WHERE t.is_specific_product_tip 
        AND p.product_id = %s
    """, (product_id, ))


def get_general_tips_from_db():
    return execute_query("""
        SELECT t.product_name, concat(product_name, ' - ', t.refrigerate_tips) as refrigerate_tips, concat(product_name, ' - ', t.freeze_tips) as freeze_tips
        from food_storage_tips t
        WHERE not t.is_specific_product_tip 
    """)


def get_product_name_from_db(product_id):
    """
    Retrieves product name

    Returns:
        list: A list of product names by id.
    """
    return execute_query("""
        SELECT p.product_id, p.product_name
        FROM product_global_info p 
        WHERE p.product_id = %s
    """, (product_id,))


def get_fridge_products_with_expiry_dates(fridge_id):
    """
    Retrieves all products and their anticipated expiration dates for a given fridge,
    and returns them as a formatted string.

    Args:
        fridge_id (int): The ID of the fridge.

    Returns:
        str: A string where each product name is followed by its expiration date.
    """
    result = execute_query("""
        SELECT p.product_name, i.anticipated_expiry_date
        FROM product_global_info p
        JOIN item i ON p.product_id = i.product_id
        JOIN camera ca ON i.camera_ip = ca.camera_ip
        WHERE ca.fridge_id = %s
        ORDER BY p.product_name, i.anticipated_expiry_date
    """, (fridge_id,))

    # Create a list to hold formatted strings
    product_entries = []

    for product_name, expiry_date in result:
        expiry_date_str = expiry_date.strftime("%Y-%m-%d") if expiry_date else "Unknown"
        formatted_entry = f"{product_name}: {expiry_date_str}"
        product_entries.append(formatted_entry)

    # Join all entries into a single string
    a = ', '.join(product_entries)
    print(a)
    return ', '.join(product_entries)


def about_to_expire_products(user_id):
    # get only products that it lless then 20% time untill anticipated expiry date
    return execute_query("""
        SELECT p.product_id, p.product_name, i.anticipated_expiry_date
        FROM product_global_info p
        JOIN item i ON p.product_id = i.product_id
        JOIN camera ca ON i.camera_ip = ca.camera_ip
        join fridges f ON f.fridge_id = ca.fridge_id
        where DATE_ADD(i.date_entered, INTERVAL (DATEDIFF(i.anticipated_expiry_date, i.date_entered) * 0.8) DAY) < CURDATE()
                AND f.user_id = %s
    """, (user_id, ))
