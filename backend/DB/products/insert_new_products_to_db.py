# DB/products/insert_new_products_to_db.py

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
        {"product_name": "Chips", "category_name": "Snacks"},
        # Dairy
        {"product_name": "Greek Yogurt", "category_name": "Dairy"},
        {"product_name": "Sour Cream", "category_name": "Dairy"},
        {"product_name": "Cottage Cheese", "category_name": "Dairy"},
        {"product_name": "Mozzarella Cheese", "category_name": "Dairy"},
        {"product_name": "Feta Cheese", "category_name": "Dairy"},
        {"product_name": "Parmesan Cheese", "category_name": "Dairy"},
        {"product_name": "Heavy Cream", "category_name": "Dairy"},
        {"product_name": "Whipped Cream", "category_name": "Dairy"},
        {"product_name": "Goat Cheese", "category_name": "Dairy"},
        {"product_name": "Ricotta Cheese", "category_name": "Dairy"},
        
        # Vegetables
        {"product_name": "Lettuce", "category_name": "Vegetables"},
        {"product_name": "Spinach", "category_name": "Vegetables"},
        {"product_name": "Kale", "category_name": "Vegetables"},
        {"product_name": "Tomato", "category_name": "Vegetables"},
        {"product_name": "Cucumber", "category_name": "Vegetables"},
        {"product_name": "Carrot", "category_name": "Vegetables"},
        {"product_name": "Celery", "category_name": "Vegetables"},
        {"product_name": "Bell Pepper", "category_name": "Vegetables"},
        {"product_name": "Zucchini", "category_name": "Vegetables"},
        {"product_name": "Broccoli", "category_name": "Vegetables"},
        
        # Fruits
        {"product_name": "Apple", "category_name": "Fruits"},
        {"product_name": "Orange", "category_name": "Fruits"},
        {"product_name": "Grapes", "category_name": "Fruits"},
        {"product_name": "Strawberries", "category_name": "Fruits"},
        {"product_name": "Blueberries", "category_name": "Fruits"},
        {"product_name": "Raspberries", "category_name": "Fruits"},
        {"product_name": "Pineapple", "category_name": "Fruits"},
        {"product_name": "Mango", "category_name": "Fruits"},
        {"product_name": "Watermelon", "category_name": "Fruits"},
        {"product_name": "Peach", "category_name": "Fruits"},
        
        # Meat
        {"product_name": "Chicken Breast", "category_name": "Meat"},
        {"product_name": "Ground Beef", "category_name": "Meat"},
        {"product_name": "Turkey Slices", "category_name": "Meat"},
        {"product_name": "Smoked Salmon", "category_name": "Meat"},
        {"product_name": "Sausages", "category_name": "Meat"},
        {"product_name": "Bacon", "category_name": "Meat"},
        {"product_name": "Ham", "category_name": "Meat"},
        {"product_name": "Steak", "category_name": "Meat"},
        {"product_name": "Pork Chops", "category_name": "Meat"},
        {"product_name": "Meatballs", "category_name": "Meat"},
        
        # Beverages
        {"product_name": "Milk", "category_name": "Beverages"},
        {"product_name": "Orange Juice", "category_name": "Beverages"},
        {"product_name": "Apple Juice", "category_name": "Beverages"},
        {"product_name": "Iced Tea", "category_name": "Beverages"},
        {"product_name": "Lemonade", "category_name": "Beverages"},
        {"product_name": "Cold Brew Coffee", "category_name": "Beverages"},
        {"product_name": "Coconut Water", "category_name": "Beverages"},
        {"product_name": "Almond Milk", "category_name": "Beverages"},
        {"product_name": "Soy Milk", "category_name": "Beverages"},
        {"product_name": "Smoothie", "category_name": "Beverages"},
        
        # Snacks
        {"product_name": "Chocolate Bar", "category_name": "Snacks"},
        {"product_name": "Cheese Sticks", "category_name": "Snacks"},
        {"product_name": "Hummus", "category_name": "Snacks"},
        {"product_name": "Guacamole", "category_name": "Snacks"},
        {"product_name": "Salsa", "category_name": "Snacks"},
        {"product_name": "Yogurt Parfait", "category_name": "Snacks"},
        {"product_name": "Pudding", "category_name": "Snacks"},
        {"product_name": "Rice Cakes with Topping", "category_name": "Snacks"},
        {"product_name": "Energy Balls", "category_name": "Snacks"},
        {"product_name": "Granola Bars", "category_name": "Snacks"}
        ]

    conn = get_db_connection()
    cursor = conn.cursor()

    for product in products:
        # Fetch category_id
        cursor.execute("SELECT category_id FROM categories WHERE category_name = %s", (product["category_name"],))
        result = cursor.fetchone()

        if result:
            category_id = result[0]
            insert_product(product["product_name"], category_id)
        else:
            print(f"Error: Category '{product['category_name']}' not found in database.")

    cursor.close()
    conn.close()
