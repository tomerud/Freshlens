import re
from flask import Blueprint, request, jsonify
<<<<<<< HEAD
<<<<<<< HEAD
from DB.products.products_queries import get_fridge_products_with_expiry_dates
from python_chatgpt.chat import generate_recipe

# TODO:
#  
# **SQL**: 
# - fill the correct from DB.??? import ??? - to get all the product, amount, exp 

=======
from mysqlDB.products.products_queries import get_fridge_products_with_expiry_dates
from python_chatgpt.chat import generate_recipe

>>>>>>> 092d4e2 (Removed API key from chat.py)
=======
from mysqlDB.products.products_queries import get_fridge_products_with_expiry_dates
from python_chatgpt.chat import generate_recipe

>>>>>>> origin/main
recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/get_suggested_recipe', methods=['GET'])
def get_suggested_recipe():
    try:
        fridge_id = request.args.get("fridge_id")
        
        if not fridge_id:
            return jsonify({"error": "fridge_id query parameter is required."}), 400

        inventory = get_fridge_products_with_expiry_dates(fridge_id)

        recipe_string = generate_recipe(inventory)

        formatted_recipes = format_recipes(recipe_string)

        return jsonify({"recipes": formatted_recipes}), 200
    except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
        return jsonify({"error": str(e)}), 500
    


    
=======
        return jsonify({"error": str(e)}), 500
>>>>>>> 092d4e2 (Removed API key from chat.py)
=======
        return jsonify({"error": str(e)}), 500
    

def format_recipes(recipe_string):
    """
    Splits a recipe string using "###" and structures it into JSON format.
    """
    if not recipe_string:
        return []

    raw_recipes = [recipe.strip() for recipe in recipe_string.split("###") if recipe.strip()]

    formatted_recipes = []
    for recipe_text in raw_recipes:
        title = extract_title(recipe_text)
        ingredients = extract_ingredients(recipe_text)
        instructions = extract_instructions(recipe_text)

        if ingredients and instructions:
            formatted_recipes.append({
                "title": title,
                "ingredients": ingredients,
                "instructions": instructions
            })
    
    return formatted_recipes


def extract_title(recipe_text):
    """
    Extracts the title from a recipe string that starts with "1. Title"
    instead of "Recipe X:".
    """
    title_match = re.search(r"^\d+\.\s*(.+)", recipe_text)
    return title_match.group(1).strip() if title_match else "Unknown Recipe"


def extract_ingredients(recipe_text):
    """
    Extracts ingredients from a recipe string and removes leading dashes.
    """
    ingredients_match = re.search(r"Ingredients:\n([\s\S]*?)\n\nInstructions:", recipe_text, re.MULTILINE)
    if ingredients_match:
        return [re.sub(r"^- ", "", line.strip()) for line in ingredients_match.group(1).split("\n") if line.strip()]
    return []

def extract_instructions(recipe_text):
    """
    Extracts instructions from a recipe string and removes leading numbers.
    """
    instructions_match = re.search(r"Instructions:\n([\s\S]*)", recipe_text, re.MULTILINE)
    if instructions_match:
        return [re.sub(r"^\d+\.\s*", "", line.strip()) for line in instructions_match.group(1).split("\n") if line.strip()]
    return []
