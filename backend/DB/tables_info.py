from db_utils import get_db_connection

def describe_tables(database_name):
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch table and column details
        query = f"""
        SELECT
            c.TABLE_NAME,
            c.COLUMN_NAME,
            c.COLUMN_TYPE,
            c.IS_NULLABLE,
            c.COLUMN_KEY,
            c.EXTRA,
            k.REFERENCED_TABLE_NAME,
            k.REFERENCED_COLUMN_NAME
        FROM
            information_schema.COLUMNS c
        LEFT JOIN
            information_schema.KEY_COLUMN_USAGE k
        ON
            c.TABLE_SCHEMA = k.TABLE_SCHEMA AND
            c.TABLE_NAME = k.TABLE_NAME AND
            c.COLUMN_NAME = k.COLUMN_NAME
        WHERE
            c.TABLE_SCHEMA = '{database_name}'
        ORDER BY
            c.TABLE_NAME, c.ORDINAL_POSITION;
        """

        cursor.execute(query)

        # Fetch and display results
        results = cursor.fetchall()
        print(f"{'Table':<20}{'Column':<20}{'Type':<20}{'Nullable':<10}{'Key':<10}{'Extra':<20}{'Referenced Table':<20}{'Referenced Column':<20}")
        print("-" * 130)
        for row in results:
            table, column, col_type, is_nullable, col_key, extra, ref_table, ref_column = row
            print(f"{table:<20}{column:<20}{col_type:<20}{is_nullable:<10}{col_key:<10}{extra:<20}{ref_table or '':<20}{ref_column or '':<20}")
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_users():
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch user details
        query = """
        SELECT user_id, user_first_name FROM users
        """

        cursor.execute(query)

        # Fetch and return results
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Example Usage
if _name_ == "_main_":
    # Describe tables
    describe_tables("freshlens")

    # Get users
    users = get_users()
    print("\nUsers:")
    for user_id, user_first_name in users:
        print(f"User ID: {user_id}, First Name: {user_first_name}")