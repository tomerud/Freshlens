from flask import Blueprint, request, jsonify
from datetime import date
from mysqlDB.DS.predict_shopping_waste import pipeline
from mysqlDB.products.products_queries import about_to_expire_products,get_product_id_from_db, get_top_three_thrown_products
from mysqlDB.products.products_queries import get_waste_summary_by_week

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
        result = [
        {
        "product_id": get_product_id_from_db(row["product"]),
        "product": row["product"],
        "amount_buy": row["quantity_estimated"],
        "amount_will_throw": row["amount_thrown_out_estimated"],
        "recommendation": max(row["quantity_estimated"] - row["amount_thrown_out_estimated"], 0),
        }
        for _, row in res.iterrows()
        ]
        return jsonify(result)
    except Exception as e:
        print("Error fetching user prediciton:", str(e))
        return jsonify({"error": "Failed to fetch user prediciton"}), 500
    
@analysis_bp.route('/get_waste_summary', methods=['GET'])
def get_waste_summary():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    try:
        summary = get_waste_summary_by_week(user_id)
        return jsonify(summary)
    except Exception as e:
        print("Error fetching waste summary:", str(e))
        return jsonify({"error": "Failed to fetch waste summary"}), 500

@analysis_bp.route('/get_top_thrown_products', methods=['GET'])
def get_top_thrown_products():
    try:
        top_products = get_top_three_thrown_products()
        return jsonify(top_products)
    except Exception as e:
        print("Error fetching top thrown products:", str(e))
        return jsonify({"error": "Failed to fetch top thrown products"}), 500

    """
    [{'product_id': 1, 'product': 'Milk', 'amount_buy': 5.0, 'amount_will_throw': 3.0, 'recommendation': 2.0}, 
    {'product_id': 4, 'product': 'Golden Delicious Apples', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}, 
    {'product_id': 6, 'product': 'Cola', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}, 
    {'product_id': 9, 'product': 'Farmers 14% Sour Cream', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}, 
    {'product_id': 10, 'product': 'Baxter 2% Cottage Cheese', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}]
    """

