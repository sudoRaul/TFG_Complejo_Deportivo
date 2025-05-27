from flask import Blueprint, json, Response, request, jsonify
from werkzeug.security import generate_password_hash
from db import db
from models import Usuario
from flask_jwt_extended import create_access_token
from extensions import enviar_correo


bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

#Obtener todos los usuarios
@bp.route('/', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()

    if not usuarios:
        return jsonify({"error": "Users not found"}), 200

    data = [{
        'id': u.id,
        'nombre': u.nombre,
        'apellido': u.apellido,
        'email': u.email,
        'edad': u.edad,
        'rol': u.rol,
        'altura': u.altura,
        'peso': u.peso,
        'sexo': u.sexo,
        'telefono': u.telefono,
    } for u in usuarios]

    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    
# Obtener un usuario por ID
@bp.route('/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    
    if not usuario:
        # Para el error también usamos el formato correcto
        return Response(
            json.dumps({'error': 'User not found'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )
    
    # Estructura de datos del usuario
    usuario_data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'email': usuario.email,
        'edad': usuario.edad,
        'altura': usuario.altura,
        'peso': usuario.peso,
        'sexo': usuario.sexo,
        'telefono': usuario.telefono,
        'rol': usuario.rol,
        'contrasena': usuario.contraseña 
    }
    
    return Response(
        json.dumps(usuario_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    
# Crear un nuevo usuario
@bp.route('/', methods=['POST'])
def create_usuario():
    data = request.get_json()
    required_keys = ["nombre", "apellido", "email", "contraseña", "edad", "rol", "altura", "peso", "sexo", "telefono"]

    if not data or not all(key in data for key in required_keys):
        return jsonify({"error": "Incomplete datas: it's required " + ", ".join(required_keys)}), 400

    try:
        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "This email is already registered"}), 409

        hashed_password = generate_password_hash(data["contraseña"])
        nuevo_usuario = Usuario(
            nombre=data["nombre"],
            apellido=data["apellido"],
            email=data["email"],
            contraseña=hashed_password,
            edad=data["edad"],
            rol=data["rol"],
            altura=data["altura"],
            peso=data["peso"],
            sexo=data["sexo"],
            telefono=data["telefono"]
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        # Creamos el token tras el registro
        access_token = create_access_token(identity={"id": nuevo_usuario.id, "rol": nuevo_usuario.rol})

        # Enviar correo de bienvenida al usuario
        asunto = "<h1>Welcome to the sport center</h1>"
        cuerpo = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; color: #333;">
                        <h2 style="color: #2e6c80;">Welcome, {nuevo_usuario.nombre}</h2>
                        <p>Thanks for register in our sport center.</p>
                        <p>We welcome you to our platform and we hope that you enjoy our facilities, we are so glad that you belong to our family.</p>
                        <p>If you have some question, don't doubt to contact us.</p>
                        <button style="background-color: #2e6c80; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                            <a href="http://localhost:5173/contact" target-blank=true style="color: white; text-decoration: none;">Contact</a>
                        </button>
                        <br>
                        <p style="color: #888;">We'll see you in the sport center,<br><strong>The Sports Complex Team</strong></p>
                        <button style="background-color: #2e6c80; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                            <a href="http://localhost:5173" target-blank=true style="color: white; text-decoration: none;">Go to the Web</a>
                        </button>
                    </body>
                    </html>
                """

        enviar_correo(nuevo_usuario.email, asunto, cuerpo)

        return jsonify({
            "mensaje": "User created successfully",
            "access_token": access_token,
            "usuario": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email,
                "edad": nuevo_usuario.edad,
                "rol": nuevo_usuario.rol,
                "altura": nuevo_usuario.altura,
                "peso": nuevo_usuario.peso,
                "sexo": nuevo_usuario.sexo,
                "telefono": nuevo_usuario.telefono
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating the user: {str(e).encode('utf-8', errors='replace').decode('utf-8')}"}), 500


# Actualizar un usuario por ID
@bp.route('/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({"error": "User not found"}), 404

    if "nombre" in data:
        usuario.nombre = data["nombre"]
    if "apellido" in data:
        usuario.apellido = data["apellido"]
    if "email" in data:
        usuario.email = data["email"]
    if "edad" in data:
        usuario.edad = data["edad"]
    if "rol" in data:
        usuario.rol = data["rol"]
    if "altura" in data:
        usuario.altura = data["altura"]
    if "peso" in data:
        usuario.peso = data["peso"]
    if "sexo" in data:
        usuario.sexo = data["sexo"]
    if "telefono" in data:
        usuario.telefono = data["telefono"]
    if "contraseña" in data:
        usuario.contraseña = generate_password_hash(data["contraseña"])  # Se hashea la nueva contraseña

    db.session.commit()
    return jsonify({"mensaje": "User updated succesfully"}), 200


# Eliminar un usuario por ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'User not found'}), 404
    
    # Enviar correo de despedida antes de eliminar
    asunto = "We're sad to see you go!"
    cuerpo_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #d9534f;">Goodbye {usuario.nombre},</h2>
            <p>We're sorry to see you leave our sports complex platform.</p>
            <p>If you ever change your mind, we'll be more than happy to welcome you back anytime.</p>
            <p>Wishing you all the best in your future activities!</p>
            <br>
            <p style="color: #5bc0de;">The Sports Complex Team</p>
        </body>
    </html>
    """

    enviar_correo(
        destinatario=usuario.email,
        asunto=asunto,
        cuerpo=cuerpo_html,
        
    )

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'User deleted succesfully'}), 200



# Eliminar un usuario por ID
@bp.route('/recPassword', methods=['POST'])
def sendEmailForgot():
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    email = data["email"]
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"error": "User with this email does not exist"}), 404

    subject = "Password Recovery Instructions"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #2e6c80;">Hello, {usuario.nombre}</h2>
            <p>We received a request to reset your password for your Sports Complex account.</p>
            <p>If you did not request a password reset, please ignore this email.</p>
            <p>To reset your password, please follow the instructions below:</p>
            <ol>
                <li>Go to the password recovery page: <a href="http://localhost:5173/forgot-password" target="_blank">Reset Password</a></li>
                <li>Enter your email address and follow the steps provided.</li>
            </ol>
            <p>If you have any questions, feel free to contact our support team.</p>
            <br>
            <p style="color: #888;">Best regards,<br><strong>The Sports Complex Team</strong></p>
        </body>
    </html>
    """

    enviar_correo(email, subject, body)
    return jsonify({"message": "Recovery instructions sent to your email"}), 200
    
    