from flask import Flask
from app.config import Config
from app.database import db
from app.routes.incidents import incidents_bp
from app.routes.user import users_bp
from app.routes.auth import auth_bp
from flask_cors import CORS
from flask_mail import Mail, Message


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
     # esto esta bien
    mail = Mail(app)
    # Habilitar CORS para todas las rutas
    CORS(app, supports_credentials=True)
    db.init_app(app)   
   

    with app.app_context():
       
        db.create_all()

    app.register_blueprint(incidents_bp, url_prefix="/api")    
    app.register_blueprint(users_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")


    return app
