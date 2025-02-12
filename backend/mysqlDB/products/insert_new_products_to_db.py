import os
import re
from flask import json
import requests
from ..db_utils import execute_query

import kagglehub
import pandas as pd
from kagglehub import KaggleDatasetAdapter


def insert_new_category_to_db(category_name):
    """
    Inserts a new category into the `categories` table.

    Args:
        category_name (str): The name of the category.
    """

    execute_query("""
        INSERT INTO categories (category_name)
        VALUES (%s)
    """, (category_name,))
    
    print(f"Category '{category_name}' inserted successfully.")


def get_nutritional_values(product_name: str) -> dict:
    """
    Fetch only the top 8 nutritional values from the USDA API for a given product name.
    """
    api_key = os.getenv("USDA_API_KEY")
    if not api_key:
        return {"error": "API key is missing"}

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={product_name}&api_key={api_key}&pageSize=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

    data = response.json()

    if not data.get("foods"):
        return {"error": "No results found for this product"}

    first_food = data["foods"][0]
    nutrients = first_food.get("foodNutrients", [])
    serving_size = first_food.get("servingSize", None)

    # Mapping from USDA API names to our column names
    important_nutrients = {
        "Energy": "Energy",
        "Protein": "Protein",
        "Total lipid (fat)": "Total lipid (fat)",
        "Fatty acids, total saturated": "Fatty acids, total saturated",
        "Carbohydrate, by difference": "Carbohydrate, by difference",
        "Total Sugars": "Total Sugars",
        "Fiber, total dietary": "Fiber, total dietary",
        "Sodium, Na": "Sodium, Na"
    }

    nutritional_info_per_100g = {}

    for nutrient in nutrients:
        nutrient_name = nutrient.get("nutrientName", "Unknown Nutrient")
        value = nutrient.get("value", None)
        unit = nutrient.get("unitName", "")

        if nutrient_name in important_nutrients and value is not None:
            # Convert to per 100g if serving size is available
            if serving_size and serving_size > 0:
                value = round((value / serving_size) * 100, 2)
            
            nutritional_info_per_100g[important_nutrients[nutrient_name]] = {"value": value, "unit": unit}

    return {
        "product_name": first_food.get("description", product_name),
        "serving_size": serving_size, 
        "nutritional_info_per_100g": nutritional_info_per_100g
    }


def clean_price(price_str):
    """Removes dollar sign and converts valid prices to float. Returns 0.0 if invalid."""
    if not isinstance(price_str, str):  # Ensure it's a string
        return 0.0
    
    match = re.search(r"\d+(\.\d+)?", price_str)  # Looks for numbers like 5.99 or 10
    if match:
        return float(match.group(0))  # Convert to float

    return 0.0


def load_canadian_prices_from_kaggle():
    df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            os.getenv("KAGGLE_DATASET"),
            os.getenv("KAGGLE_FILE_PATH")
        )

    df.columns = df.columns.str.replace(" ", "_").str.lower()
    data_to_insert = [
        (row["name"], clean_price(row["price"]))
        for _, row in df.iterrows()
        ]
    
    for row in data_to_insert:
        execute_query("""
            INSERT INTO canadian_products_prices (name, price)
            VALUES (%s, %s)
        """, row)
    print(f"Successfully inserted rows into canadian_products_prices!")



def parse_usda_storage_tips():
    try:
        with open('../backend/src/foodkeeper-food-safety-tips.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        tips = []
        for sheet in data.get("sheets", []):
            if sheet.get("name") == "Product":
                for entry in sheet.get("data", []):
                    if isinstance(entry, list):
                        product_data = {list(item.keys())[0]: list(item.values())[0] for item in entry if isinstance(item, dict)}

                        product_name = product_data.get("Name")
                        refrigerate_tips = product_data.get("Refrigerate_tips")
                        freeze_tips = product_data.get("Freeze_Tips")

                        if product_name and (refrigerate_tips or freeze_tips):
                            tips.append((product_name, refrigerate_tips, freeze_tips))
        return tips
    except Exception as e:
        print(f"Error parsing USDA storage tips: {e}")
        return []


def insert_storage_tips(tips, is_specific):
    """
    Inserts storage tips into the database.

    :param tips: List of tuples (product_name, refrigerate_tips, freeze_tips)
    :param is_specific: Boolean flag (1 for product-specific, 0 for general tips)
    """
    if not tips:
        return

    insert_query = '''
        INSERT INTO food_storage_tips (product_name, refrigerate_tips, freeze_tips, is_specific_product_tip)
        VALUES (%s, %s, %s, %s)
    '''

    formatted_tips = [(tip[0], tip[1], tip[2], int(is_specific)) for tip in tips]
    for tip in formatted_tips:
        execute_query(insert_query, params=tip, commit=True)


def load_storage_tips():
    product_tips = parse_usda_storage_tips()
    insert_storage_tips(product_tips, is_specific=True)

    general_tips = [
        ("Temperature Safety", "Keep food below 5°C to prevent bacteria growth.", "Freeze below -15°C to keep food safe."),
        ("High-Risk Foods", "Store raw and cooked meat separately in sealed containers.", "Avoid refreezing thawed food."),
        ("Cooked Food", "Cool hot food in small portions before refrigerating.", None),
        ("Perishable Items", "Refrigerate dairy, eggs, seafood, and prepared salads.", None),
        ("Leftovers", "Store leftovers in airtight containers and eat within days.", "Freeze leftovers for longer storage."),
        ("Opened Packages", "Transfer canned and jarred food to proper containers.", None),
        ("Raw vs Cooked", "Store raw food below cooked food to prevent contamination.", None),
        ("Expiration", "Throw away food left out for 4+ hours.", None),
        ("Use-By Dates", "Always check expiration dates before eating.", None),
        ("Cooling Hot Food", "Let hot food cool slightly before refrigerating.", None),
        ("Grocery Storage", "Put frozen and refrigerated foods away immediately.", None),
        ("Cold Transport", "Use insulated bags for frozen food on hot days.", None),
        ("Defrosting", "Keep defrosted food in the fridge until cooking.", None),
        ("Microwave Thawing", "Cook food immediately after microwave thawing.", None),
        ("Food Storage Containers", "Use clean, non-toxic, sealed containers.", None),
        ("Pantry Items", "Store dry foods in cool, dark places.", None)
    ]

    insert_storage_tips(general_tips, is_specific=False)
    print(f"Successfully inserted rows into food_storage_tips!")


def insert_new_product_to_db(product_name, category_id):
    """
    Inserts a new product into the `product_global_info` table and adds separate nutritional values.

    Args:
        product_name (str): The name of the product.
        category_id (int): The ID of the category the product belongs to.
    """
    nutrition_data = get_nutritional_values(product_name)

    if "error" in nutrition_data:
        print(f"Error fetching nutritional data: {nutrition_data['error']}")
        return
    
    serving_size = nutrition_data.get("serving_size", "N/A")
    nutrients = nutrition_data["nutritional_info_per_100g"]

    # Extract nutrients safely with default values
    energy = nutrients.get("Energy", {}).get("value", None)
    protein = nutrients.get("Protein", {}).get("value", None)
    fat = nutrients.get("Total lipid (fat)", {}).get("value", None)
    saturated_fat = nutrients.get("Fatty acids, total saturated", {}).get("value", None)
    carbs = nutrients.get("Carbohydrate, by difference", {}).get("value", None)
    sugars = nutrients.get("Total Sugars", {}).get("value", None)
    fiber = nutrients.get("Fiber, total dietary", {}).get("value", None)
    sodium = nutrients.get("Sodium, Na", {}).get("value", None)

    # Insert data into separate columns
    execute_query("""
        INSERT INTO product_global_info 
        (product_name, category_id, serving_size, energy_kcal, protein_g, fat_g, saturated_fat_g, 
         carbs_g, sugars_g, fiber_g, sodium_mg) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (product_name, category_id, serving_size, energy, protein, fat, saturated_fat, carbs, sugars, fiber, sodium))

    print(f"Product '{product_name}' inserted successfully under category_id={category_id}.")