from flask import Flask
from app.config import Config
from app.database import db
from app.routes.incidents import incidents_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(incidents_bp, url_prefix="/api")

    return app
