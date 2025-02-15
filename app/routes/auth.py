from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime
from app.database import db
from app.models import User
from app.config import Config

auth_bp = Blueprint("auth", __name__)

# ruta para login y generar token
@auth_bp.route('/auth', methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    #Buscar ususario en la base de datos
    user = User.query.filter_by(email=email).first()
    print(user.username)
    #verificar si el usuario existe
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message":"Password incorrecto o usuario no existe"}),401
 
    # Crear token JWT
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # Expira en 3 horas
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "username": user.username, "is_admin": user.is_admin})

# ✅ Middleware para proteger rutas
from functools import wraps

SECRET_KEY = Config.SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            response = jsonify({"message": "Token es requerido"})
            response.status_code = 401
            response.headers["Access-Control-Allow-Origin"] = "*"  # 🔥 Añade CORS en error
            return response

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            response = jsonify({"message": "Token expirado"})
            response.status_code = 401
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response
        except jwt.InvalidTokenError:
            response = jsonify({"message": "Token inválido"})
            response.status_code = 401
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

        return f(*args, **kwargs)

    return decorated