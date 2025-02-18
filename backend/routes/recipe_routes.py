from flask import Blueprint, request, jsonify
from mysqlDB.products.products_queries import get_fridge_products_with_expiry_dates
from python_chatgpt.chat import generate_recipe

recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/get_suggested_recipe', methods=['GET'])
def get_suggested_recipe():
    try:
        fridge_id = request.args.get("fridge_id")
        
        if not fridge_id:
            return jsonify({"error": "fridge_id query parameter is required."}), 400

        inventory = get_fridge_products_with_expiry_dates(fridge_id)

        recipes = generate_recipe(inventory)

        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500