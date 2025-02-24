import datetime
from flask import Blueprint, request, jsonify
from datetime import date
from DS.nutrition_idea import get_nutrition_data
from DS.predict_shopping_waste import pipeline
from db_utils import execute_query
from mysqlDB.products.products_queries import about_to_expire_products,get_product_id_from_db

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
    
@analysis_bp.route('/get_wasted_items_by_week', methods=['GET'])
def get_wasted_items_by_week():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    try:
        # Query for wasted items with their waste_date, product details, and price.
        query = """
            SELECT h.waste_date, p.product_id, p.product_name, cpp.price
            FROM user_product_history h
            JOIN product_global_info p ON h.product_id = p.product_id
            JOIN canadian_products_prices cpp ON p.product_name = cpp.name
            WHERE h.user_id = %s AND h.is_thrown = 1
        """
        results = execute_query(query, (user_id,), fetch_all=True)
        
        weekly_data = {}
        for row in results:
            # Convert the waste_date to a date object
            waste_date = row["waste_date"]
            if isinstance(waste_date, str):
                waste_date = datetime.strptime(waste_date, "%Y-%m-%d").date()
            
            # Get the ISO calendar year and week number
            year, week, _ = waste_date.isocalendar()
            key = f"{year}-W{week}"
            
            if key not in weekly_data:
                weekly_data[key] = {"items": [], "total_price": 0.0}
            
            # Append the item and add its price to the week's total
            item_data = {
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "price": float(row["price"]),
                "waste_date": waste_date.isoformat()
            }
            weekly_data[key]["items"].append(item_data)
            weekly_data[key]["total_price"] += float(row["price"])
        
        return jsonify(weekly_data)
    except Exception as e:
        print("Error fetching wasted items by week:", str(e))
        return jsonify({"error": "Failed to fetch wasted items by week"}), 500

    """
    [{'product_id': 1, 'product': 'Milk', 'amount_buy': 5.0, 'amount_will_throw': 3.0, 'recommendation': 2.0}, 
    {'product_id': 4, 'product': 'Golden Delicious Apples', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}, 
    {'product_id': 6, 'product': 'Cola', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}, 
    {'product_id': 9, 'product': 'Farmers 14% Sour Cream', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}, 
    {'product_id': 10, 'product': 'Baxter 2% Cottage Cheese', 'amount_buy': 7.0, 'amount_will_throw': 4.0, 'recommendation': 3.0}]
    """

