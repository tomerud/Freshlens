[1mdiff --git a/backend/DB/__init__.py b/backend/DB/__init__.py[m
[1mnew file mode 100644[m
[1mindex 0000000..e69de29[m
[1mdiff --git a/backend/DB/create_tables.py b/backend/DB/create_tables.py[m
[1mindex 44ea823..c0ba071 100644[m
[1m--- a/backend/DB/create_tables.py[m
[1m+++ b/backend/DB/create_tables.py[m
[36m@@ -1,4 +1,6 @@[m
 from db_utils import get_db_connection[m
[32m+[m[32mimport mysql.connector[m
[32m+[m
 [m
 def create_tables():[m
     try:[m
[36m@@ -36,7 +38,8 @@[m [mdef create_tables():[m
             """,[m
             "shelves": """[m
                 CREATE TABLE IF NOT EXISTS shelves ([m
[31m-                    shelve_id INT AUTO_INCREMENT PRIMARY KEY,[m
[32m+[m[32m                    shelf_id INT AUTO_INCREMENT PRIMARY KEY,[m
[32m+[m[32m                    shelf_name VARCHAR(255),[m
                     fridge_id INT,[m
                     FOREIGN KEY (fridge_id) REFERENCES fridges(fridge_id)[m
                 )[m
[36m@@ -52,13 +55,12 @@[m [mdef create_tables():[m
                     item_id INT AUTO_INCREMENT PRIMARY KEY,[m
                     product_id INT,[m
                     fridge_id INT,[m
[31m-                    shelve_id INT,[m
[32m+[m[32m                    shelf_id INT,[m
                     date_entered DATE,[m
                     anticipated_expiry_date DATE,[m
                     is_rotten BOOLEAN,[m
                     FOREIGN KEY (product_id) REFERENCES products(product_id),[m
[31m-                    FOREIGN KEY (fridge_id) REFERENCES fridges(fridge_id),[m
[31m-                    FOREIGN KEY (shelve_id) REFERENCES shelves(shelve_id)[m
[32m+[m[32m                    FOREIGN KEY (shelf_id) REFERENCES shelves(shelf_id)[m
                 )[m
             """[m
         }[m
[36m@@ -70,21 +72,21 @@[m [mdef create_tables():[m
         [m
         conn.commit()[m
 [m
[31m-        subscriptions = [[m
[31m-            ("free", 0),[m
[31m-            ("plus", 9.99),[m
[31m-            ("premium", 29.99)[m
[31m-        ][m
[32m+[m[32m        # subscriptions = [[m
[32m+[m[32m        #     ("free", 0),[m
[32m+[m[32m        #     ("plus", 9.99),[m
[32m+[m[32m        #     ("premium", 29.99)[m
[32m+[m[32m        # ][m
 [m
[31m-        # Insert each subscription into the table[m
[31m-        for subscription_name, monthly_cost in subscriptions:[m
[31m-            cursor.execute("""[m
[31m-                INSERT INTO subscription (subscription_name, monthly_cost)[m
[31m-                VALUES (%s, %s)[m
[31m-            """, (subscription_name, monthly_cost))[m
[32m+[m[32m        # # Insert each subscription into the table[m
[32m+[m[32m        # for subscription_name, monthly_cost in subscriptions:[m
[32m+[m[32m        #     cursor.execute("""[m
[32m+[m[32m        #         INSERT INTO subscription (subscription_name, monthly_cost)[m
[32m+[m[32m        #         VALUES (%s, %s)[m
[32m+[m[32m        #     """, (subscription_name, monthly_cost))[m
 [m
[31m-        conn.commit()[m
[31m-        print(f"Inserted subscription: {subscription_name}, {monthly_cost}")[m
[32m+[m[32m        # conn.commit()[m
[32m+[m[32m        # print(f"Inserted subscription: {subscription_name}, {monthly_cost}")[m
 [m
 [m
     except mysql.connector.Error as err:[m
[1mdiff --git a/backend/DB/fridge/__init__.py b/backend/DB/fridge/__init__.py[m
[1mnew file mode 100644[m
[1mindex 0000000..e69de29[m
[1mdiff --git a/backend/DB/fridge/get_fridges.py b/backend/DB/fridge/get_fridges.py[m
[1mnew file mode 100644[m
[1mindex 0000000..ab1926d[m
[1m--- /dev/null[m
[1m+++ b/backend/DB/fridge/get_fridges.py[m
[36m@@ -0,0 +1,30 @@[m
[32m+[m[32m# DB/user/insert_user_to_db.py[m
[32m+[m
[32m+[m[32mfrom mysql.connector import Error  # Ensure you're importing the right Error type[m
[32m+[m[32mfrom ..db_utils import get_db_connection[m
[32m+[m
[32m+[m[32mdef get_fridges_from_db(user_id):[m
[32m+[m[32m    try:[m
[32m+[m[32m        conn = get_db_connection()[m
[32m+[m[32m        cursor = conn.cursor()[m
[32m+[m[32m        query = "SELECT fridge_name FROM fridges WHERE user_id = %s"[m
[32m+[m[32m        cursor.execute(query, (user_id,))[m
[32m+[m[32m        rows = cursor.fetchall()  # Fetch all results[m
[32m+[m[41m        [m
[32m+[m[32m        # Convert the results into a list of dictionaries. Adjust the key name if needed.[m
[32m+[m[32m        fridges = [{"fridge_name": row[0]} for row in rows][m
[32m+[m[32m        return fridges[m
[32m+[m
[32m+[m[32m    except Error as err:[m
[32m+[m[32m        print(f"Database error: {err}")[m
[32m+[m[32m        return None[m
[32m+[m[32m    finally:[m
[32m+[m[32m        if conn.is_connected():[m
[32m+[m[32m            cursor.close()[m
[32m+[m[32m            conn.close()[m
[32m+[m
[32m+[m[32m# Example usage:[m
[32m+[m[32mif __name__ == "__main__":[m
[32m+[m[32m    # Replace with an actual user_id to test[m
[32m+[m[32m    user_id = 1[m
[32m+[m[32m    print(get_fridges_from_db(user_id))[m
[1mdiff --git a/backend/DB/fridge/insert_fridge_to_db.py b/backend/DB/fridge/insert_fridge_to_db.py[m
[1mindex 878dd5c..1b2750f 100644[m
[1m--- a/backend/DB/fridge/insert_fridge_to_db.py[m
[1m+++ b/backend/DB/fridge/insert_fridge_to_db.py[m
[36m@@ -2,10 +2,10 @@[m
 [m
 from datetime import date[m
 from time import strftime[m
[31m-# We are now one directory deeper, so use '..' in the import:[m
[32m+[m[32mimport mysql[m
 from ..db_utils import get_db_connection[m
 [m
[31m-def insert_new_fridge(user_id, fridge_name):[m
[32m+[m[32mdef insert_new_fridge_to_db(user_id, fridge_name):[m
     try:[m
         conn = get_db_connection()[m
         cursor = conn.cursor()[m
[36m@@ -24,3 +24,12 @@[m [mdef insert_new_fridge(user_id, fridge_name):[m
         if conn.is_connected():[m
             cursor.close()[m
             conn.close()[m
[32m+[m
[32m+[m[32m# # Example usage[m
[32m+[m[32m# if __name__ == "__main__":[m
[32m+[m[32m#     # Example data[m
[32m+[m[32m#     example_user_id = 2[m
[32m+[m[32m#     example_fridge_name = "fridge v"[m
[32m+[m
[32m+[m[32m#     # Insert example fridge[m
[32m+[m[32m#     insert_new_fridge_to_db(example_user_id, example_fridge_name)[m
[1mdiff --git a/backend/DB/items/insert_new_item_to_db.py b/backend/DB/items/insert_new_item_to_db.py[m
[1mnew file mode 100644[m
[1mindex 0000000..3a06364[m
[1m--- /dev/null[m
[1m+++ b/backend/DB/items/insert_new_item_to_db.py[m
[36m@@ -0,0 +1,54 @@[m
[32m+[m[32m# DB/item/insert_item_to_db.py[m
[32m+[m
[32m+[m[32mfrom datetime import date, timedelta[m
[32m+[m[32mfrom time import strftime[m
[32m+[m[32mimport mysql[m
[32m+[m[32mfrom ..db_utils import get_db_connection[m
[32m+[m
[32m+[m[32mdef insert_new_item_to_db(product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten):[m
[32m+[m[32m    """[m
[32m+[m[32m    Insert a new item into the item table.[m
[32m+[m[41m    [m
[32m+[m[32m    Parameters:[m
[32m+[m[32m        product_id (int): The ID of the product.[m
[32m+[m[32m        fridge_id (int): The ID of the fridge.[m
[32m+[m[32m        shelf_id (int): The ID of the shelf.[m
[32m+[m[32m        date_entered (str or date): The date when the item was entered into the system.[m
[32m+[m[32m        anticipated_expiry_date (str or date): The date when the item is expected to expire.[m
[32m+[m[32m        is_rotten (int): Typically 0 (false) or 1 (true).[m
[32m+[m[32m    """[m
[32m+[m[32m    try:[m
[32m+[m[32m        conn = get_db_connection()[m
[32m+[m[32m        cursor = conn.cursor()[m
[32m+[m
[32m+[m[32m        cursor.execute("""[m
[32m+[m[32m            INSERT INTO item (product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten)[m
[32m+[m[32m            VALUES (%s, %s, %s, %s, %s, %s)[m
[32m+[m[32m        """, (product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten))[m
[32m+[m[32m        conn.commit()[m
[32m+[m
[32m+[m[32m        print(f"Item inserted successfully: product_id '{product_id}', fridge_id '{fridge_id}', shelf_id '{shelf_id}'.")[m
[32m+[m[32m    except mysql.connector.Error as err:[m
[32m+[m[32m        print(f"Database error: {err}")[m
[32m+[m[32m    finally:[m
[32m+[m[32m        if conn.is_connected():[m
[32m+[m[32m            cursor.close()[m
[32m+[m[32m            conn.close()[m
[32m+[m
[32m+[m[32m# # Example usage[m
[32m+[m[32m# if __name__ == "__main__":[m
[32m+[m[32m#     # Example data:[m
[32m+[m[32m#     product_id = 5    # Example product id; adjust as needed[m
[32m+[m[32m#     fridge_id = 1      # Example fridge id; adjust as needed[m
[32m+[m[32m#     shelf_id = 2      # Example shelf id; adjust as needed[m
[32m+[m[41m    [m
[32m+[m[32m#     # Use today's date as the entry date[m
[32m+[m[32m#     date_entered = date.today().isoformat()[m
[32m+[m[41m    [m
[32m+[m[32m#     # For example, set anticipated expiry date 7 days from now[m
[32m+[m[32m#     anticipated_expiry_date = (date.today() + timedelta(days=7)).isoformat()[m
[32m+[m[41m    [m
[32m+[m[32m#     is_rotten = 0      # 0 for not rotten, 1 for rotten[m
[32m+[m[41m    [m
[32m+[m[32m#     # Insert the new item[m
[32m+[m[32m#     insert_new_item_to_db(product_id, fridge_id, shelf_id, date_entered, anticipated_expiry_date, is_rotten)[m
[1mdiff --git a/backend/DB/products/insert_new_products_to_db.py b/backend/DB/products/insert_new_products_to_db.py[m
[1mnew file mode 100644[m
[1mindex 0000000..826012f[m
[1m--- /dev/null[m
[1m+++ b/backend/DB/products/insert_new_products_to_db.py[m
[36m@@ -0,0 +1,44 @@[m
[32m+[m[32m# DB/products/insert_products_to_db.py[m
[32m+[m
[32m+[m[32mfrom datetime import date[m
[32m+[m[32mfrom time import strftime[m
[32m+[m[32mimport mysql[m
[32m+[m[32mfrom ..db_utils import get_db_connection[m
[32m+[m
[32m+[m[32mdef insert_new_product_to_db(product_name):[m
[32m+[m[32m    try:[m
[32m+[m[32m        conn = get_db_connection()[m
[32m+[m[32m        cursor = conn.cursor()[m
[32m+[m
[32m+[m[32m        cursor.execute("""[m
[32m+[m[32m            INSERT INTO products (product_name)[m
[32m+[m[32m            VALUES (%s)[m
[32m+[m[32m        """, (product_name,))[m
[32m+[m[32m        conn.commit()[m
[32m+[m
[32m+[m[32m        print(f"Product '{product_name}' added successfully.")[m
[32m+[m[32m    except mysql.connector.Error as err:[m
[32m+[m[32m        print(f"Database error: {err}")[m
[32m+[m[32m    finally:[m
[32m+[m[32m        if conn.is_connected():[m
[32m+[m[32m            cursor.close()[m
[32m+[m[32m            conn.close()[m
[32m+[m
[32m+[m[32m# Example usage[m
[32m+[m[32mif __name__ == "__main__":[m
[32m+[m[32m    # List of product names to insert[m
[32m+[m[32m    product_list = [[m
[32m+[m[32m        "apple",[m[41m [m
[32m+[m[32m        "banana",[m[41m [m
[32m+[m[32m        "kale",[m[41m [m
[32m+[m[32m        "cottage cheese",[m[41m [m
[32m+[m[32m        "milk",[m[41m [m
[32m+[m[32m        "yogurt",[m[41m [m
[32m+[m[32m        "orange",[m[41m [m
[32m+[m[32m        "carrot",[m
[32m+[m[32m        "spinach",[m
[32m+[m[32m        "grapes"[m
[32m+[m[32m    ][m
[32m+[m[41m    [m
[32m+[m[32m    for product in product_list:[m
[32m+[m[32m        insert_new_product_to_db(product)[m
[1mdiff --git a/backend/DB/shelves/__init__.py b/backend/DB/shelves/__init__.py[m
[1mnew file mode 100644[m
[1mindex 0000000..e69de29[m
[1mdiff --git a/backend/DB/shelves/insert_shelf.py b/backend/DB/shelves/insert_shelf.py[m
[1mnew file mode 100644[m
[1mindex 0000000..94384b3[m
[1m--- /dev/null[m
[1m+++ b/backend/DB/shelves/insert_shelf.py[m
[36m@@ -0,0 +1,36 @@[m
[32m+[m
[32m+[m[32mfrom datetime import date[m
[32m+[m[32mfrom time import strftime[m
[32m+[m[32mimport mysql[m
[32m+[m[32mfrom ..db_utils import get_db_connection[m
[32m+[m
[32m+[m[32mdef insert_new_shelf_to_db(fridge_id, shelf_name):[m
[32m+[m[32m    try:[m
[32m+[m[32m        conn = get_db_connection()[m
[32m+[m[32m        cursor = conn.cursor()[m
[32m+[m
[32m+[m[32m        cursor.execute("""[m
[32m+[m[32m            INSERT INTO shelves (fridge_id, shelf_name)[m
[32m+[m[32m            VALUES (%s, %s)[m
[32m+[m[32m        """, (fridge_id, shelf_name))[m
[32m+[m[32m        conn.commit()[m
[32m+[m
[32m+[m[32m        print(f"Shelf '{shelf_name}' added successfully for fridge_id '{fridge_id}'.")[m
[32m+[m
[32m+[m[32m    except mysql.connector.Error as err:[m
[32m+[m[32m        print(f"Database error: {err}")[m
[32m+[m[32m    finally:[m
[32m+[m[32m        if conn.is_connected():[m
[32m+[m[32m            cursor.close()[m
[32m+[m[32m            conn.close()[m
[32m+[m
[32m+[m[32m# Example usage: loop to insert multiple shelves for fridge IDs 1 to 4[m
[32m+[m[32mif __name__ == "__main__":[m
[32m+[m[32m    # Define a list of shelf names to insert for each fridge.[m
[32m+[m[32m    shelf_names = ["Top Shelf", "Middle Shelf", "Bottom Shelf"][m
[32m+[m
[32m+[m[32m    # Loop through fridge IDs 1 to 4.[m
[32m+[m[32m    for fridge_id in range(1, 5):[m
[32m+[m[32m        for shelf_name in shelf_names:[m
[32m+[m[32m            insert_new_shelf_to_db(fridge_id, shelf_name)[m
[32m+[m
[1mdiff --git a/backend/DB/tables_info.py b/backend/DB/tables_info.py[m
[1mindex 6d600c6..764259a 100644[m
[1m--- a/backend/DB/tables_info.py[m
[1m+++ b/backend/DB/tables_info.py[m
[36m@@ -1,4 +1,6 @@[m
 from db_utils import get_db_connection[m
[32m+[m[32mimport mysql.connector[m
[32m+[m
 [m
 def describe_tables(database_name):[m
     try:[m
[1mdiff --git a/backend/DB/user/insert_user_to_db.py b/backend/DB/user/insert_user_to_db.py[m
[1mindex e3c848c..827b92b 100644[m
[1m--- a/backend/DB/user/insert_user_to_db.py[m
[1m+++ b/backend/DB/user/insert_user_to_db.py[m
[36m@@ -2,7 +2,7 @@[m
 [m
 from datetime import date[m
 from time import strftime[m
[31m-# We are now one directory deeper, so use '..' in the import:[m
[32m+[m[32mimport mysql.connector[m
 from ..db_utils import get_db_connection[m
 [m
 def insert_new_user(first_name, last_name, email, subscription_type):[m
[36m@@ -36,3 +36,4 @@[m [mdef insert_new_user(first_name, last_name, email, subscription_type):[m
             cursor.close()[m
             conn.close()[m
 [m
[41m+[m
[1mdiff --git a/backend/routes/__init__.py b/backend/routes/__init__.py[m
[1mnew file mode 100644[m
[1mindex 0000000..ef3464c[m
[1m--- /dev/null[m
[1m+++ b/backend/routes/__init__.py[m
[36m@@ -0,0 +1,17 @@[m
[32m+[m[32mfrom routes.user_routes import user_bp[m
[32m+[m[32mfrom routes.item_routes import item_bp[m
[32m+[m[32mfrom routes.fridge_routes import fridge_bp[m
[32m+[m[32mfrom routes.data_routes import app_bp[m
[32m+[m[32mfrom routes.shelves_routes import shelves_bp[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m# List of all blueprints in the routes package.[m
[32m+[m[32mblueprints = [[m
[32m+[m[32m    user_bp,[m
[32m+[m[32m    item_bp,[m
[32m+[m[32m    fridge_bp,[m
[32m+[m[32m    app_bp,[m
[32m+[m[32m    shelves_bp,[m
[32m+[m
[32m+[m[32m][m
[1mdiff --git a/backend/routes/data_routes.py b/backend/routes/data_routes.py[m
[1mnew file mode 100644[m
[1mindex 0000000..3772dcd[m
[1m--- /dev/null[m
[1m+++ b/backend/routes/data_routes.py[m
[36m@@ -0,0 +1,13 @@[m
[32m+[m[32mimport datetime[m
[32m+[m[32mfrom flask import Blueprint, request, jsonify[m
[32m+[m
[32m+[m[32mapp_bp = Blueprint('app_bp', __name__)[m
[32m+[m
[32m+[m
[32m+[m[32m@app_bp.route('/data')[m
[32m+[m[32mdef get_time():[m
[32m+[m[32m    return jsonify({[m
[32m+[m[32m        'Name': "geek",[m
[32m+[m[32m        'Age': "22",[m
[32m+[m[32m        'Date': datetime.datetime.now()[m
[32m+[m[32m    })[m
\ No newli