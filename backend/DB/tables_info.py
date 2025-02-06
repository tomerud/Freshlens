from db_utils import execute_query


def describe_tables(database_name):
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
    FROM information_schema.COLUMNS c
    LEFT JOIN information_schema.KEY_COLUMN_USAGE k
    ON c.TABLE_SCHEMA = k.TABLE_SCHEMA AND
        c.TABLE_NAME = k.TABLE_NAME AND
        c.COLUMN_NAME = k.COLUMN_NAME
    WHERE c.TABLE_SCHEMA = '{database_name}'
    ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION;
    """

    results = execute_query(query)

    print(f"{'Table':<20}{'Column':<20}{'Type':<20}{'Nullable':<10}{'Key':<10}{'Extra':<20}{'Referenced Table':<20}{'Referenced Column':<20}")
    print("-" * 130)
    for row in results:
        table, column, col_type, is_nullable, col_key, extra, ref_table, ref_column = row
        print(f"{table:<20}{column:<20}{col_type:<20}{is_nullable:<10}{col_key:<10}{extra:<20}{ref_table or '':<20}{ref_column or '':<20}")


def get_users():
    query = """
    SELECT user_id, user_first_name FROM users
    """
    return execute_query(query)



# Example Usage
if __name__ == "__main__":
    # Describe tables
    describe_tables("freshlens")

    # Get users
    users = get_users()
    print("\nUsers:")
    for user_id, user_first_name in users:
        print(f"User ID: {user_id}, First Name: {user_first_name}")