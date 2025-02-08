
from ..db_utils import execute_query

def insert_new_shelf_to_db(fridge_id, shelf_name):
    execute_query("""
        INSERT INTO shelves (fridge_id, shelf_name)
        VALUES (%s, %s)
    """, (fridge_id, shelf_name))

    print(f"Shelf '{shelf_name}' added successfully for fridge_id '{fridge_id}'.")


if __name__ == "__main__":
    # Define a list of shelf names to insert for each fridge.
    shelf_names = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]

    # Loop through fridge IDs 1 to 4.
    for fridge_id in range(1, 5):
        for shelf_name in shelf_names:
            insert_new_shelf_to_db(fridge_id, shelf_name)

