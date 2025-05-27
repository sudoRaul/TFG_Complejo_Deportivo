from flask import Blueprint, jsonify, json, Response, request
from db import db
from models import Contacto
from extensions import enviar_correo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('contacto', __name__, url_prefix='/contacto')

# Obtener todos los contactos
@bp.route('/', methods=['GET'])
def get_contactos():
    contactos = Contacto.query.all()

    if not contactos:
        return jsonify({"error": "There are not contacts to show"}), 200

    data = [{
        'id': c.id,
        'nombre': c.nombre,
        'apellido': c.apellido,
        'email': c.email,
        'telefono': c.telefono,
        'comentario': c.comentario
    } for c in contactos]

    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    
# Obtener un contacto por ID
@bp.route('/<int:id>', methods=['GET'])
def get_contacto(id):
    contacto = Contacto.query.get(id)
    
    if not contacto:
        return Response(
            json.dumps({'error': 'Contact not found'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )
    
    contacto_data = {
        'id': contacto.id,
        'nombre': contacto.nombre,
        'apellido': contacto.apellido,
        'email': contacto.email,
        'telefono': contacto.telefono,
        'comentario': contacto.comentario
    }
    
    return Response(
        json.dumps(contacto_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )


# Crear un nuevo contacto
@bp.route('/', methods=['POST'])
def create_contacto():
    data = request.get_json()

    if not data or not all(key in data for key in ["nombre", "apellido", "email", "telefono", "comentario"]):
        return jsonify({"error": "Incomplete datas"}), 400

    nuevo_contacto = Contacto(
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        telefono=data["telefono"],
        comentario=data["comentario"]
    )

    db.session.add(nuevo_contacto)
    db.session.commit()

    return jsonify({"message": "Contact registered succesfully", "id": nuevo_contacto.id}), 201


# Enviar un mensaje desde el formulario de contacto (sin guardar en la BBDD)
@bp.route('/<int:id>/responder', methods=['POST'])
def responder_contacto(id):

    data = request.get_json()
    respuesta = data.get("respuesta", "").strip()

    if not respuesta:
        return jsonify({"error": "The response cannot be empty."}), 400

    # Buscar el contacto por ID
    contacto = Contacto.query.get(id)
    if not contacto:
        return jsonify({"error": "Message not found."}), 404

    # Construir cuerpo del mensaje de respuesta
    cuerpo = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <p>Hello <strong>{contacto.nombre}</strong>,</p>

            <p>We received your message and we are happy to respond to you:</p>

            <p><strong>Your message was:</strong><br>
            "{contacto.comentario}"</p>

            <p><strong>Our response is:</strong><br>
            "{respuesta}"</p>

            <br>
            <p style="color: #5bc0de;"><strong>The Sports Complex Team</strong></p>
        </body>
    </html>
    """

    try:
        # Enviar correo al contacto
        enviar_correo(asunto="Response to your contact message", cuerpo=cuerpo, destinatario=contacto.email)

        # Eliminar el mensaje de la base de datos
        db.session.delete(contacto)
        db.session.commit()

        return jsonify({"message": "Response send and message deleted succesfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error sending the response or deleting the message: {str(e)}"}), 500