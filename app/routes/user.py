from flask import request, jsonify, Blueprint
from app.database import db
from app.models import User
from werkzeug.security import generate_password_hash

# Definir el Blueprint
users_bp = Blueprint("users", __name__)

# ✅ Ruta para crear un usuario
@users_bp.route('/users', methods=["POST"])
def create_user():
    data = request.json
    new_user = User(    
    username = data["username"],
    email = data["email"],
    password =generate_password_hash(data["password"],salt_length=3) ,
    is_admin =data["is_admin"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User created successfully"})

# ✅ Ruta para obterner usuarios
@users_bp.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id":user.id, "username":user.username, "email":user.email,"is_admin": user.is_admin ,"password":user.password}for user in users]),200

# ✅ Ruta para obterne un usuario
@users_bp.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    # Buscar usuario
    user = User.query.get(id)
    if not user:
        return jsonify({"message":"Users no encontrado"}), 404

    return jsonify({"id":user.id, "username":user.username, "email":user.email,"is_admin": user.is_admin }),200

# ✅ Ruta para obterner eleiminar un usuario
@users_bp.route('/users/<int:id>',methods=["DELETE"])
def delete_user(id):
    # Buscar usuario
    user = User.query.get(id)
    if not user:
        return jsonify({"message":"Usuario no encontardo"}), 404
    db.session.delete(user)
    db.session.commit
    return jsonify({"message":"usuario eliminado exitosamente"})

# ✅ Ruta para actualizar un usuario
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({"message":"Usuario no encontardo"}), 404
    
     # Actualizar los campos del usuario
    user.username = data.get('username',user.username)
    user.email = data.get('email',user.email)
    user.password = data.get('password',user.password)
    user.is_admin = data.get('is_admin',user.is_admin)

    db.session.commit()
    return jsonify({"message": "Usuario actualizado correctamente"}), 200