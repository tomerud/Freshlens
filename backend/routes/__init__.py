from routes.user_routes import user_bp
from routes.item_routes import item_bp
from routes.fridge_routes import fridge_bp
from routes.data_routes import app_bp


# List of all blueprints in the routes package.
blueprints = [
    user_bp,
    item_bp,
    fridge_bp,
    app_bp,
]
