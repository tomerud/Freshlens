from db_utils import get_db_connection

def create_tables():
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Define table creation queries
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
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_first_name VARCHAR(255),
                    user_last_name VARCHAR(255),
                    date_subscribed DATE,
                    subscription_id INT,
                    FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
                )
            """,
            "fridges": """
                CREATE TABLE IF NOT EXISTS fridges (
                    fridge_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    fridge_name VARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """,
            "shelves": """
                CREATE TABLE IF NOT EXISTS shelves (
                    shelve_id INT AUTO_INCREMENT PRIMARY KEY,
                    fridge_id INT,
                    FOREIGN KEY (fridge_id) REFERENCES fridges(fridge_id)
                )
            """,
            "products": """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(255)         
                )
            """,
            "item": """
                CREATE TABLE IF NOT EXISTS item (
                    item_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT,
                    fridge_id INT,
                    shelve_id INT,
                    date_entered DATE,
                    anticipated_expiry_date DATE,
                    is_rotten BOOLEAN,
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    FOREIGN KEY (fridge_id) REFERENCES fridges(fridge_id),
                    FOREIGN KEY (shelve_id) REFERENCES shelves(shelve_id)
                )
            """
        }

        # Execute each table creation query
        for table_name, table_sql in tables.items():
            cursor.execute(table_sql)
            print(f"Table '{table_name}' created successfully.")
        
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Execute table creation
if _name_ == "_main_":
    create_tables()