from flask import Blueprint, request, jsonify
from datetime import date
from DS.nutrition_idea import get_nutrition_data
from DS.predict_shopping_waste import pipeline
from mysqlDB.products.products_queries import about_to_expire_products

analysis_bp = Blueprint('analysis_bp', __name__)

@analysis_bp.route('/get_notifications', methods=['GET'])
def get_fridge_name():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    try:
        products_to_notify = about_to_expire_products(user_id)
        
        today = date.today()
        notifications = []

        for product in products_to_notify:
            exp_date = product["anticipated_expiry_date"]
            days_left = (exp_date - today).days

            product_name = product['product_name'].title()

            if days_left < 1:
                notifications.append({
                    "id": f"urgent-{product['product_id']}",
                    "message": f"🚨 {product_name} expires today!",
                    "timestamp": today.isoformat()
                })
            elif days_left <= 3:
                notifications.append({
                    "id": f"warning-{product['product_id']}",
                    "message": f"⚠️ {product_name} will expire in {days_left} days.",
                    "timestamp": today.isoformat()
                })
            elif days_left <= 7:
                notifications.append({
                    "id": f"reminder-{product['product_id']}",
                    "message": f"ℹ️ {product_name} is getting old. Consider using it soon.",
                    "timestamp": today.isoformat()
                })

        notifications.append({
            "id": "update-1",
            "message": "🔔 A new fridge update is available!",
            "timestamp": today.isoformat()
        })

        notifications.append({
            "id": "savings-1",
            "message": "💰Reminder to check your cart!",
            "timestamp": today.isoformat()
        })

        notifications.append({
            "id": "recipe-1",
            "message": "🔔 We have new recipes for you!",
            "timestamp": today.isoformat()
        })

        return jsonify(notifications)

    except Exception as e:
        print("Error fetching notifications:", str(e))
        return jsonify({"error": "Failed to fetch notifications"}), 500
    
    
@analysis_bp.route('/get_nutritional_advice', methods=['GET'])
def get_nutritional_advice():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    try:
        nutritional_values = get_nutrition_data(user_id)
        return jsonify(nutritional_values) #need to format
        #maybe chain to another LLM to get ?
    except Exception as e:
        print("Error fetching nutritional advice:", str(e))
        return jsonify({"error": "Failed to fetch nutritional advice"}), 500


@analysis_bp.route('/get_shopping_cart_recommendations', methods=['GET'])
def get_shopping_cart_recommendations():
    #for now only inserted history for user_id = 101, can change it by using randomised_history_insert.py
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    try:
        res=pipeline(user_id)
        if res is None:
            return jsonify({"error": "No predictions available for the user."}), 404
        return res.to_json(orient='records')
    except Exception as e:
        print("Error fetching user prediciton:", str(e))
        return jsonify({"error": "Failed to fetch user prediciton"}), 500

    """
    res : <class 'pandas.core.frame.DataFrame'>
    this is how res look like, if we printed it:
        ds                quantity_estimated| amount_thrown_out_estimated| user_id|             product
    0 2025-03-03                 5.0                          3.0     101                      Milk
    1 2025-03-10                 6.0                          3.0     101                      Milk
    3 2025-03-10                 5.0                          2.0     101   Golden Delicious Apples
    4 2025-03-03                 7.0                          4.0     101                      Cola
    5 2025-03-10                 6.0                          3.0     101                      Cola
    6 2025-03-03                 7.0                          4.0     101    Farmers 14% Sour Cream
    7 2025-03-10                 6.0                          3.0     101    Farmers 14% Sour Cream
    8 2025-03-03                 7.0                          4.0     101  Baxter 2% Cottage Cheese
    9 2025-03-10                 7.0                          4.0     101  Baxter 2% Cottage Cheese
    """

