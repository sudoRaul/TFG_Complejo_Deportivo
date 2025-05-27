from flask import Blueprint, jsonify, json, Response, request
from db import db
from models import Reserva
from models import Usuario
from models import Instalacion
from sqlalchemy.exc import SQLAlchemyError
from extensions import enviar_correo


bp = Blueprint('reservas', __name__, url_prefix='/reservas')

#Mostrar todas las reservas
@bp.route('/', methods=['GET'])
def get_o_buscar_reservas():
    nombre_instalacion = request.args.get("instalacion_name")
    fecha = request.args.get("fecha")

    try:
        # Siempre hacemos el join con Instalacion
        query = db.session.query(Reserva).join(Instalacion)

        if nombre_instalacion:
            query = query.filter(Instalacion.nombre.ilike(f"%{nombre_instalacion}%"))

        if fecha:
            query = query.filter(Reserva.fecha == fecha)

        reservas = query.all()

        if not reservas:
            return jsonify({"error": "Reserves not found"}), 200

        resultado = []
        for r in reservas:
            usuario = Usuario.query.get(r.id_usuario)
            instalacion = Instalacion.query.get(r.id_instalacion)

            resultado.append({
                "id": r.id,
                "fecha": r.fecha.strftime('%Y-%m-%d'),
                "hora": str(r.hora),
                "usuario": {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "email": usuario.email,
                    "edad": usuario.edad,
                    "rol": usuario.rol,
                    "altura": usuario.altura,
                    "peso": usuario.peso,
                    "sexo": usuario.sexo,
                    "telefono": usuario.telefono
                },
                "instalacion": {
                    "id": instalacion.id,
                    "nombre": instalacion.nombre,
                    "categoria": instalacion.categoria,
                    "disponibilidad": instalacion.disponibilidad,
                    "foto": instalacion.foto
                }
            })

        return jsonify(resultado), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Error in DataBase", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


# Obtener reservas por email del usuario
@bp.route('/usuario', methods=['GET'])
def get_reservas_por_usuario():
    email = request.args.get("email")

    if not email:
        return jsonify({"error": "Email cnanot be empty"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404
    

    reservas = Reserva.query.filter_by(id_usuario=usuario.id).all()
    if not reservas:
        return jsonify({"error": "There isn't reserves for this user"}), 200

    resultado = []
    for r in reservas:
        instalacion = Instalacion.query.get(r.id_instalacion)
        resultado.append({
            "id": r.id,
            "fecha": r.fecha.strftime('%Y-%m-%d'),
            "hora": str(r.hora),
            "instalacion": {
                "id": instalacion.id,
                "nombre": instalacion.nombre,
                "categoria": instalacion.categoria,
                "disponibilidad": instalacion.disponibilidad,
                "foto": instalacion.foto,
                "descripcion": instalacion.descripcion
            }
        })

    return jsonify(resultado), 200
    
# Obtener una reserva por ID
@bp.route('/<int:id>', methods=['GET'])
def get_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return Response(
            json.dumps({'error': 'Reserve not found'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )

    
    usuario = Usuario.query.get(reserva.id_usuario) if reserva.id_usuario else None
    instalacion = Instalacion.query.get(reserva.id_instalacion) if reserva.id_instalacion else None

    
    response_data = {
        'id': reserva.id,
        'usuario': {
            'id': usuario.id if usuario else None,
            'nombre': usuario.nombre if usuario else None,
            'apellido': usuario.apellido if usuario else None,
            'email': usuario.email if usuario else None,
            'edad': usuario.edad if usuario else None,
            'rol': usuario.rol if usuario else None,
            'altura': usuario.altura if usuario else None,
            'peso': usuario.peso if usuario else None,
            'sexo': usuario.sexo if usuario else None,
            'telefono': usuario.telefono if usuario else None
        } if usuario else None,
        'instalacion': {
            'id': instalacion.id if instalacion else None,
            'nombre': instalacion.nombre if instalacion else None,
            'categoria': instalacion.categoria if instalacion else None,
            'disponibilidad': instalacion.disponibilidad if instalacion else None
        } if instalacion else None,
        'fecha': reserva.fecha.strftime('%Y-%m-%d') if reserva.fecha else None,
        'hora': str(reserva.hora) if reserva.hora else None
    }

    return Response(
        json.dumps(response_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    
@bp.route('/', methods=['POST'])
def crear_reserva():
    try:
        data = request.get_json()
        required_keys = ("id_usuario", "id_instalacion", "fecha", "hora")
        if not data or not all(key in data for key in required_keys):
            return jsonify({"error": "Incomplete datas: it is require " + ", ".join(required_keys)}), 400

        usuario = Usuario.query.get(data["id_usuario"])
        if not usuario:
            return jsonify({"error": "User not found"}), 404

        instalacion = Instalacion.query.get(data["id_instalacion"])
        if not instalacion:
            return jsonify({"error": "Facility not found"}), 404

        reserva_existente = Reserva.query.filter_by(
            id_instalacion=data["id_instalacion"],
            fecha=data["fecha"],
            hora=data["hora"]
        ).first()

        if reserva_existente:
            return jsonify({"error": "A reserve already exist for this facility in this date and time. Please select another time or date"}), 409

        nueva_reserva = Reserva(
            id_usuario=data["id_usuario"],
            id_instalacion=data["id_instalacion"],
            fecha=data["fecha"],
            hora=data["hora"]
        )

        db.session.add(nueva_reserva)
        db.session.commit()

        # Enviar correo de confirmación
        asunto = "Your reservation has been confirmed!"
        cuerpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #5cb85c;">Hello {usuario.nombre},</h2>
                <p>We're happy to confirm your reservation at our sports complex.</p>
                <p><strong>Facility:</strong> {instalacion.nombre}<br>
                <strong>Date:</strong> {data['fecha']}<br>
                <strong>Time:</strong> {data['hora']}</p>
                <p>Please arrive a few minutes early and bring any necessary equipment.</p>
                <br>
                <p style="color: #5bc0de;">Thanks for booking with us!<br>
                The Sports Complex Team</p>
            </body>
        </html>
        """

        enviar_correo(
            destinatario=usuario.email,
            asunto=asunto,
            cuerpo=cuerpo_html
        )

        return jsonify({"mensaje": "Reserve created and email sent", "id": nueva_reserva.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating the reserve: " + str(e)}), 500


# Actualizar una reserva por ID
@bp.route('/<int:id>', methods=['PUT'])
def actualizar_reserva(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "There isn't datas to update"}), 400

    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"error": "Reserve not found"}), 404

    fecha = data.get("fecha")
    hora = data.get("hora")

    if not fecha and not hora:
        return jsonify({"error": "You should introduce at least date or time to update"}), 400

    # Validar que no exista otra reserva para la misma instalación, fecha y hora (excluyendo la actual)
    id_instalacion = reserva.id_instalacion
    nueva_fecha = fecha if fecha else reserva.fecha
    nueva_hora = hora if hora else reserva.hora
    reserva_existente = Reserva.query.filter(
        Reserva.id_instalacion == id_instalacion,
        Reserva.fecha == nueva_fecha,
        Reserva.hora == nueva_hora,
        Reserva.id != reserva.id
    ).first()
    if reserva_existente:
        return jsonify({"error": "A reserve already exist for this facility in this date and time. Please select another time or date"}), 409

    if fecha:
        reserva.fecha = fecha
    if hora:
        reserva.hora = hora

    try:
        db.session.commit()
        return jsonify({"mensaje": "Reserve updated succesfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error updating the reserve. Try again please " + str(e)}), 500

# Eliminar una reserva por ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'error': 'Reserve not found'}), 404
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserve deleted succesfully'}), 200
