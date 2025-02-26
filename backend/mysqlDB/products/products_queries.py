import datetime
from mysqlDB.db_utils import execute_query


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
        SELECT distinct p.product_id, p.product_name
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

def get_product_id_from_db(product_name):
    """
    Retrieves product id based on the product name.

    Returns:
        int or None: The product ID, or None if not found.
    """
    result= execute_query("""
        SELECT p.product_id
        FROM product_global_info p
        WHERE p.product_name = %s
    """, (product_name,))
    if result:
        return result[0]['product_id'] if 'product_id' in result[0] else None
    else:
        return None

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
    for row in result:
        product_name = row["product_name"]
        expiry_date = row["anticipated_expiry_date"]
        if isinstance(expiry_date, str):  # if str, wont work beacusedyt dosent have strftime 
            try:
                expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")  # Adjust format 
            except ValueError:
                expiry_date = None  # Handle invalid date formats

        expiry_date_str = expiry_date.strftime("%Y-%m-%d") if expiry_date else "Unknown"
        formatted_entry = f"{product_name}: {expiry_date_str}"
        product_entries.append(formatted_entry)

    
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


def get_freshness_score_from_db(user_id):
    return execute_query("""
    SELECT round(AVG(CASE 
    WHEN days_till_expiry_date < 0 THEN 0 
    WHEN days_till_expiry_date = 0 THEN 20 
    WHEN days_till_expiry_date = 1 THEN 40
    WHEN days_till_expiry_date = 2 THEN 60
    WHEN days_till_expiry_date = 3 THEN 80
    WHEN days_till_expiry_date > 3 THEN 100
    END)) as avg_freshness_score
    FROM (
        SELECT DATEDIFF(i.anticipated_expiry_date, CURDATE()) AS days_till_expiry_date, i.anticipated_expiry_date, CURDATE()
        FROM product_global_info p
        JOIN item i ON p.product_id = i.product_id
        JOIN camera ca ON i.camera_ip = ca.camera_ip
        JOIN fridges f ON f.fridge_id = ca.fridge_id
        where f.user_id = %s
    ) AS sub
    """, (user_id, ),fetch_one=True)


def get_waste_summary_by_month(user_id):
    """
    Retrieves wasted items (is_thrown=1) for the given user,
    joins with product info and Canadian prices, groups them by month,
    and returns a list of objects where each object contains:
      - "month": a string in the format "YYYY-MM"
      - "value": the total price wasted in that month.
    """
    query = """
        SELECT DATE_FORMAT(uph.date_entered, '%Y-%m') AS month, SUM(cpp.price) AS value
        FROM user_product_history uph
        JOIN product_global_info pg ON uph.product_id = pg.product_id
        JOIN canadian_products_prices cpp ON pg.product_name = cpp.name
        WHERE uph.user_id = %s AND uph.is_thrown = 1
                AND uph.date_entered >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY month
        ORDER BY month ASC
    """
    return execute_query(query, (user_id,), fetch_all=True)


def get_top_three_thrown_products():
    """
    Retrieves the top 3 products that have been thrown away most frequently.
    Returns a list of dictionaries with each product's name and the number of times it was thrown.
    """
    return execute_query("""
        SELECT p.product_name, COUNT(*) as thrown_count
        FROM user_product_history uph
        JOIN product_global_info p ON uph.product_id = p.product_id
        WHERE uph.is_thrown = 1
        GROUP BY p.product_name
        ORDER BY thrown_count DESC
        LIMIT 3
<<<<<<< HEAD
    """, (), fetch_all=True)
=======
    """, (), fetch_all=True)


def get_user_products_and_quantities(user_id):
    """
    Retrieves all products associated with a user's fridges along with the quantity for each product.
    
    It joins the 'item', 'camera', 'fridges', and 'product_global_info' tables to fetch product names and counts.
    
    Args:
        user_id (str): The unique identifier of the user.
    
    Returns:
        list of dict: Each dictionary contains:
            - product_name: The name of the product.
            - quantity: The number of times the product appears (i.e. its count).
    """
    query = """
        SELECT pgi.product_name, COUNT(*) AS quantity
          FROM item i
          JOIN camera c ON i.camera_ip = c.camera_ip
          JOIN fridges f ON c.fridge_id = f.fridge_id
          JOIN product_global_info pgi ON i.product_id = pgi.product_id
         WHERE f.user_id = %s
         GROUP BY pgi.product_name
    """
    results = execute_query(query, (user_id,))
    return results


def get_avg_weekly_history_per_product():
    """
    Calculates the average weekly count of history entries for each product.
    
    For each product in the user_product_history table, the function:
      1. Determines the total number of history entries.
      2. Finds the earliest and latest date_entered.
      3. Computes the number of days between these dates (using 1 if there is only one entry).
      4. Calculates the average weekly count by dividing the total entries by the number of days and multiplying by 7.
    
    Returns:
        list of dict: Each dictionary contains:
            - product_name: The product's name.
            - total_entries: Total count of history records for that product.
            - num_days: The number of days between the earliest and latest entry (minimum 1).
            - avg_weekly: The computed average number per week.
    """
    query = """
        SELECT 
            pgi.product_name,
            COUNT(*) AS total_entries,
            CASE
                WHEN DATEDIFF(MAX(uph.date_entered), MIN(uph.date_entered)) = 0 THEN 1
                ELSE DATEDIFF(MAX(uph.date_entered), MIN(uph.date_entered))
            END AS num_days,
            (COUNT(*) / CASE
                WHEN DATEDIFF(MAX(uph.date_entered), MIN(uph.date_entered)) = 0 THEN 1
                ELSE DATEDIFF(MAX(uph.date_entered), MIN(uph.date_entered))
            END) * 7 AS avg_weekly
          FROM user_product_history uph
          JOIN product_global_info pgi ON uph.product_id = pgi.product_id
         GROUP BY pgi.product_name;
    """
    results = execute_query(query)
    return results

def get_recommendations_for_each_item(user_id):
    """
    For each product that a user currently has in their fridge, this function computes
    the difference between the current quantity (as returned by get_user_products_and_quantities)
    and the weekly average count from history (as returned by get_avg_weekly_history_per_product).

    Returns:
        list of dict: Each dictionary contains:
            - product_name: The name of the product.
            - current_quantity: The current count of the product in the fridge.
            - weekly_avg: The average weekly count of the product from history.
            - difference: (current_quantity - weekly_avg)
    """
    # Retrieve the current quantities per product for the user.
    current_quantities = get_user_products_and_quantities(user_id)
    
    # Retrieve the average weekly history count per product.
    weekly_avgs = get_avg_weekly_history_per_product()
    
    # Convert weekly averages to a dictionary keyed by product name.
    weekly_dict = {row['product_name']: float(row['avg_weekly']) for row in weekly_avgs}
    
    recommendations = []
    for row in current_quantities:
        product_name = row['product_name']
        current_qty = int(row['quantity'])
        weekly_avg = weekly_dict.get(product_name, 0.0)
        difference = current_qty - weekly_avg
        
        recommendations.append({
            'product_name': product_name,
            'current_quantity': current_qty,
            'weekly_avg': weekly_avg,
            'difference': difference
        })
        
    return recommendations

# Example usage:
if __name__ == "__main__":
    test_user = "0NNRFLhbXJRFk3ER2_iTr8VulFm4"
    products_quantities = get_user_products_and_quantities(test_user)
    print("User products and quantities:")
    for row in products_quantities:
        print(f"Product: {row['product_name']}, Quantity: {row['quantity']}")




    
    # Test top thrown products function


#for testing
# if __name__ == '__main__':
#     user_id = "0NNRFLhbXJRFk3ER2_iTr8VulFm4"
#     summary = get_waste_summary_by_week(user_id)
#     print(summary)
>>>>>>> main
