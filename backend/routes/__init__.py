from routes.user_routes import user_bp
from routes.item_routes import item_bp
from routes.fridge_routes import fridge_bp
from routes.camera_routes import camera_bp
from routes.images_routes import image_bp

# List of all blueprints in the routes package.
blueprints = [
    user_bp,
    item_bp,
    fridge_bp,
    camera_bp,
    image_bp
]