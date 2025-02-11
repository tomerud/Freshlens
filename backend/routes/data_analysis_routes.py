from flask import Blueprint, request, jsonify
from datetime import date
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

            if days_left < 1:
                notifications.append({
                    "id": f"urgent-{product['product_id']}",
                    "message": f"🚨 {product['product_name']} expires today!",
                    "timestamp": today.isoformat()
                })
            elif days_left <= 3:
                notifications.append({
                    "id": f"warning-{product['product_id']}",
                    "message": f"⚠️ {product['product_name']} will expire in {days_left} days.",
                    "timestamp": today.isoformat()
                })
            elif days_left <= 7:
                notifications.append({
                    "id": f"reminder-{product['product_id']}",
                    "message": f"ℹ️ {product['product_name']} is getting old. Consider using it soon.",
                    "timestamp": today.isoformat()
                })

        notifications.append({
            "id": "update-1",
            "message": "🔔 A new fridge update is available!",
            "timestamp": today.isoformat()
        })

        notifications.append({
            "id": "savings-1",
            "message": "💰Reminder to check your smart cart!",
            "timestamp": today.isoformat()
        })
        print(notifications)
        return jsonify(notifications)

    except Exception as e:
        print("Error fetching notifications:", str(e))
        return jsonify({"error": "Failed to fetch notifications"}), 500
