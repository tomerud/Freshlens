from datetime import date, timedelta
import random

from backend.mysqlDB.camera.insert_camera_to_db import insert_camera_to_db
from backend.mysqlDB.fridge.insert_fridge_to_db import insert_new_fridge_to_db
from backend.mysqlDB.items.insert_new_item_to_db import get_all_products_from_db, insert_item_to_db
from backend.mysqlDB.products.insert_new_products_to_db import insert_new_category_to_db, insert_new_product_to_db, load_canadian_prices_from_kaggle, load_storage_tips
from backend.mysqlDB.user.insert_user_to_db import insert_new_user
from backend.mysqlDB.db_utils import execute_query

def create_tables():
    tables = {
        "subscription": """
            CREATE TABLE IF NOT EXISTS subscription (
                subscription_id INT AUTO_INCREMENT PRIMARY KEY,
                subscription_name VARCHAR(255),
                monthly_cost DECIMAL(10, 2)
            )
        """,
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(28) NOT NULL UNIQUE PRIMARY KEY,
                user_name VARCHAR(255),
                user_email VARCHAR(255),
                date_subscribed DATE,
                subscription_id INT,
                FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
            )
        """,
        "fridges": """
            CREATE TABLE IF NOT EXISTS fridges (
                fridge_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(28) NOT NULL,
                fridge_name VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """,
        "categories": """
            CREATE TABLE IF NOT EXISTS categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                category_name VARCHAR(255)                  
            )
        """,
        "product_global_info": """
            CREATE TABLE IF NOT EXISTS product_global_info (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                category_id INT NOT NULL,
                serving_size VARCHAR(255) NULL,
                energy_kcal FLOAT NULL,
                protein_g FLOAT NULL,
                fat_g FLOAT NULL,
                saturated_fat_g FLOAT NULL,
                carbs_g FLOAT NULL,
                sugars_g FLOAT NULL,
                fiber_g FLOAT NULL,
                sodium_mg FLOAT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        """,
            "camera": """
            CREATE TABLE IF NOT EXISTS camera (
                camera_ip VARCHAR(255) PRIMARY KEY,
                fridge_id INT,
                FOREIGN KEY (fridge_id) REFERENCES fridges(fridge_id)
            )
        """,
            "item": """
                CREATE TABLE IF NOT EXISTS item (
                    item_id INT NOT NULL UNIQUE PRIMARY KEY,
                    is_inserted_by_user BOOLEAN NOT NULL,
                    product_id INT,
                    camera_ip VARCHAR(255),
                    date_entered DATE,
                    anticipated_expiry_date DATE,
                    remove_from_fridge_date DATE,
                    is_rotten BOOLEAN,
                    FOREIGN KEY (product_id) REFERENCES product_global_info(product_id),
                    FOREIGN KEY (camera_ip) REFERENCES camera(camera_ip)
                )
            """,
            "canadian_products_prices": """
                CREATE TABLE IF NOT EXISTS canadian_products_prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price DECIMAL(10,2) NOT NULL            
                );
            """,
            "food_storage_tips": """
                CREATE TABLE IF NOT EXISTS food_storage_tips (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL,
                    refrigerate_tips TEXT,
                    freeze_tips TEXT,
                    is_specific_product_tip BOOLEAN
                )
            """,
         "user_product_history": """
            CREATE TABLE IF NOT EXISTS user_product_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(28) NOT NULL,
                product_id INT NOT NULL,
                is_thrown BOOLEAN NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES product_global_info(product_id)
            );
        """
    }


    for table_name, table_sql in tables.items():
        execute_query(table_sql)
        print(f"Table '{table_name}' created successfully.")

def drop_all_tables():
    tables = {
            "item": """DROP TABLE IF EXISTS item""",
            "camera": """DROP TABLE IF EXISTS camera""",
            "fridges": """DROP TABLE IF EXISTS fridges""",
            "users": """DROP TABLE IF EXISTS users""",
            "subscription": """DROP TABLE IF EXISTS subscription""",
            "product_global_info": """DROP TABLE IF EXISTS product_global_info""",
            "categories": """DROP TABLE IF EXISTS categories""",
            "canadian_products_prices": """DROP TABLE IF EXISTS canadian_products_prices""",
            "food_storage_tips" : "DROP TABLE IF EXISTS food_storage_tips",
            "item_usage": """DROP TABLE IF EXISTS item_usage""",
            "user_purchases": """DROP TABLE IF EXISTS user_purchases""",

            "user_product_history": """DROP TABLE IF EXISTS user_product_history"""
        }

    for table_name, table_sql in tables.items():
        execute_query(table_sql)
        print(f"Table '{table_name}' dropped successfully.")


def insert_demo_data_to_fridge_table():
    example_user_id = "0NNRFLhbXJRFk3ER2_iTr8VulFm4"
    example_fridge_name_1 = "my home fridge"
    insert_new_fridge_to_db(example_user_id, example_fridge_name_1)

    example_user_id = "0NNRFLhbXJRFk3ER2_iTr8VulFm4"
    example_fridge_name_2 = "my office fridge"
    insert_new_fridge_to_db(example_user_id, example_fridge_name_2)

def insert_demo_data_to_camera_table():
    example_fridge_id = 1
    insert_camera_to_db(camera_ip="192.168.1.100", fridge_id=example_fridge_id)
    insert_camera_to_db(camera_ip="192.168.1.101", fridge_id=example_fridge_id)
    insert_camera_to_db(camera_ip="192.168.1.102", fridge_id=example_fridge_id)

def insert_demo_data_to_item_table():
    products = get_all_products_from_db()
    selected_products = random.sample(products, 20)  # Pick 20 random products
    for i, product in enumerate(selected_products, start=1):  
        product_id = product["product_id"]  
        category_name = product["category_name"]

        # Generate realistic expiry dates based on category
        expiry_days = {
            "Dairy": 7,
            "Vegetables": 5,
            "Fruits": 6,
            "Meat": 4,
            "Beverages": 14,
            "Snacks": 30
        }
        days_to_expiry = expiry_days.get(category_name, 7)  # Default to 7 days if category is missing

        # Randomized values
        is_inserted_by_user = random.choice([True, False])
        camera_ip = "192.168.1.100"
        date_entered = date.today() - timedelta(days=random.randint(0, 5))
        anticipated_expiry_date = date_entered + timedelta(days=days_to_expiry)
        remove_from_fridge_date = date_entered + timedelta(days=random.randint(0, days_to_expiry + 5))
        is_rotten = random.choice([False, False, False, True])  # 75% chance not rotten

        insert_item_to_db(
            item_id=i,
            is_inserted_by_user=is_inserted_by_user,
            product_id=product_id,
            camera_ip=camera_ip,
            date_entered=date_entered,
            anticipated_expiry_date=anticipated_expiry_date,
            remove_from_fridge_date=remove_from_fridge_date,
            is_rotten=is_rotten
        )

def insert_demo_data_to_categories_table():
    categories = ["Dairy", "Vegetables", "Fruits", "Meat", "Beverages", "Snacks"]
    
    for category in categories:
        insert_new_category_to_db(category)

def insert_demo_data_to_product_table():
    products = [
        {"product_name": "Milk", "category_name": "Dairy"},
        {"product_name": "Cheese", "category_name": "Dairy"},
        {"product_name": "Carrot", "category_name": "Vegetables"},
        {"product_name": "Golden Delicious Apples", "category_name": "Fruits"},
        {"product_name": "Chicken Breast Boneless Skinless", "category_name": "Meat"},
        {"product_name": "Cola", "category_name": "Beverages"},
        {"product_name": "Chips", "category_name": "Snacks"},
        # Dairy
        {"product_name": "Heavy Cream", "category_name": "Dairy"},
        {"product_name": "swiss Cheese", "category_name": "Dairy"},
        {"product_name": "Coffee Creamer", "category_name": "Dairy"},
        {"product_name": "Ricotta Cheese", "category_name": "Dairy"},
        {"product_name": "Yogurt", "category_name": "Dairy"},
        
        # Vegetables       
        {"product_name": "ginger", "category_name": "Vegetables"},
        {"product_name": "eggplant", "category_name": "Vegetables"},
        {"product_name": "lemon", "category_name": "Vegetables"},
        {"product_name": "Kale", "category_name": "Vegetables"},
        {"product_name": "Tomato", "category_name": "Vegetables"},
        {"product_name": "Cucumber", "category_name": "Vegetables"},
        
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

    for product in products:
        result = execute_query("SELECT category_id FROM categories WHERE category_name = %s", (product["category_name"],), fetch_one=True)

        if result:
            category_id = result['category_id']
            insert_new_product_to_db(product["product_name"], category_id)
        else:
            print(f"Error: Category '{product['category_name']}' not found in database.")

def insert_demo_data_to_subscriptions_table():
    subscriptions = [
            ("free", 0),
            ("plus", 9.99),
            ("premium", 29.99)
        ]

    for subscription_name, monthly_cost in subscriptions:
        execute_query("""
            INSERT INTO subscription (subscription_name, monthly_cost)
            VALUES (%s, %s)
        """, (subscription_name, monthly_cost))

    print(f"Inserted subscription: {subscription_name}, {monthly_cost}")

def insert_demo_data_to_users_table():
    users = [
            {"user_id" : "0NNRFLhbXJRFk3ER2_iTr8VulFm4", "user_name": "Liam Anderson", "email": "liam.anderson@example.com", "subscription_type": "free"},
            {"user_id" : "-vcfzeUDAuMjEmFTI2HYuQhBMVUH", "user_name": "Emma Garcia", "email": "emma.garcia@example.com", "subscription_type": "plus"},
            {"user_id" : "jpbySIdd5uktuLN1GleVlZ4EmOLv", "user_name": "Noah Smith", "email": "noah.smith@example.com", "subscription_type": "free"},
            {"user_id" : "ETqCemxYH7HP135eIMoLnIO9H1tm", "user_name": "Olivia Johnson", "email": "olivia.johnson@example.com", "subscription_type": "premium"},
            {"user_id" : "iWOBibVuFhg3svYbFqxNIM34Drrf", "user_name": "Ethan Martinez", "email": "ethan.martinez@example.com", "subscription_type": "free"}
            ]

    for user in users:
        insert_new_user(user["user_id"], user["user_name"], user["email"], user["subscription_type"]) 

def insert_demo_data_to_all_tables():
    insert_demo_data_to_categories_table()
    insert_demo_data_to_product_table()
    insert_demo_data_to_subscriptions_table()
    insert_demo_data_to_users_table()
    insert_demo_data_to_fridge_table()
    insert_demo_data_to_camera_table()
    insert_demo_data_to_item_table()
    load_canadian_prices_from_kaggle()
    load_storage_tips()


if __name__ == "__main__":
    drop_all_tables()
    create_tables()
    insert_demo_data_to_all_tables()



