from flask import Blueprint, request, jsonify
from DB.fridge.get_fridges import get_fridges_from_db
#from DB.??? import ???  

# TODO:
#  
# **SQL**: 
# - fill the correct from DB.??? import ??? - to get all the product, amount, exp 

# ** recpie func**: 
# - fill recpie = .... with the right function
recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/get_recipe', methods=['GET'])
def get_recipe():
    try:
        # data is user_id
    
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id query parameter is required."}), 400
        
        # Get fridges
        fridges = get_fridges_from_db(user_id)
        #fridges_list = [{"fridge_id": row[0], "fridge_name": row[1]} for row in fridges]

        # Get products for each fridge: need to get the procut, amount, expdate
        ingridients = None # fill

        # Generate recipe
        recipe = generate_recipe(ingridients)

        return jsonify(recipe), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
