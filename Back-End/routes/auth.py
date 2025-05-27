from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import Usuario
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.contraseña, password):
        return jsonify({"error": "Incorrect credentials"}), 401

    # Generamos el token JWT con el ID y el rol
    access_token = create_access_token(identity={"id": usuario.id, "rol": usuario.rol})

    return jsonify({
        "access_token": access_token,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "edad": usuario.edad,
            "rol": usuario.rol
        }
    }), 200
