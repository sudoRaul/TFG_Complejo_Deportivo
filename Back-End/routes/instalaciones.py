from flask import Blueprint, jsonify, json, Response, request
from db import db
from models import Instalacion
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import cross_origin
from extensions import enviar_correo
from models import Usuario


bp = Blueprint('instalaciones', __name__, url_prefix='/instalaciones')

#Obtener todas las instalaciones
@bp.route('/', methods=['GET'])
def get_o_filtrar_instalaciones():
    nombre = request.args.get("nombre")  # ejemplo: ?nombre=futbol

    try:
        query = db.session.query(Instalacion)

        if nombre:
            query = query.filter(Instalacion.nombre.ilike(f"%{nombre}%"))

        instalaciones = query.all()

        if not instalaciones:
            return jsonify({"error": "Facilities not found."}), 200

        resultado = [{
            "id": inst.id,
            "nombre": inst.nombre,
            "foto": inst.foto,
            "categoria": inst.categoria,
            "disponibilidad": inst.disponibilidad,
            "descripcion": inst.descripcion
        } for inst in instalaciones]

        return jsonify(resultado), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Error in DataBase", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected Error", "details": str(e)}), 500
    

# Obtener una instalación por ID
@bp.route('/<int:id>', methods=['GET'])
def get_instalacion(id):
    instalacion = Instalacion.query.get(id)
    
    if not instalacion:
        return Response(
            json.dumps({'error': 'Facility not found'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )
    
    instalacion_data = {
        'id': instalacion.id,
        'nombre': instalacion.nombre,
        'foto': instalacion.foto,
        'categoria': instalacion.categoria,
        'disponibilidad': instalacion.disponibilidad,
        "descripcion": instalacion.descripcion
    }
    
    return Response(
        json.dumps(instalacion_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    
    
@bp.route('', methods=['POST'])
def create_instalacion():
    data = request.get_json()

    if not data or not all(key in data for key in ["nombre", "categoria", "disponibilidad", "foto", "descripcion"]):
        return jsonify({"error": "Incomplete datas"}), 400

    nueva_instalacion = Instalacion(
        nombre=data["nombre"],
        categoria=data["categoria"],
        disponibilidad=data["disponibilidad"],
        foto=data["foto"],
        descripcion=data["descripcion"]
    )

    db.session.add(nueva_instalacion)
    db.session.commit()

    # Obtener todos los correos electrónicos de los usuarios
    usuarios = Usuario.query.all()
    correos = [usuario.email for usuario in usuarios if usuario.email]

    # Preparar el mensaje
    asunto = "New facility available at the sports complex"
    cuerpo_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #337ab7;">Exciting News!</h2>
            <p>A new facility has been added to our sports complex:</p>
            <ul>
                <li><strong>Name:</strong> {data['nombre']}</li>
                <li><strong>Category:</strong> {data['categoria']}</li>
                <li><strong>Description:</strong> {data['descripcion']}</li>
                <li><strong>Availability:</strong> {data['disponibilidad']}</li>
            </ul>
            <p>Feel free to check it out and make your reservation!</p>
            <br>
            <p style="color: #5cb85c;">Thank you,<br>
            Sports Complex Management</p>
        </body>
    </html>
    """

    # Enviar a cada usuario
    for correo in correos:
        enviar_correo(
            destinatario=correo,
            asunto=asunto,
            cuerpo=cuerpo_html
        )

    return jsonify({"message": "Facility created succesfully", "id": nueva_instalacion.id}), 201



# Actualizar una instalación por ID
@bp.route('/<int:id>', methods=['PUT'])
def actualizar_instalacion(id):
    data = request.get_json()
    instalacion = Instalacion.query.get(id)

    if not instalacion:
        return jsonify({"error": "Facility not found"}), 404

    if "nombre" in data:
        instalacion.nombre = data["nombre"]
    if "categoria" in data:
        instalacion.categoria = data["categoria"]
    if "disponibilidad" in data:
        instalacion.disponibilidad = data["disponibilidad"]
    if "foto" in data:
        instalacion.foto = data["foto"]
    if "descripcion" in data:
        instalacion.descripcion = data["descripcion"]

    db.session.commit()
    return jsonify({"mensaje": "Facility updated succesfully"}), 200


# Eliminar una instalación por ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_instalacion(id):
    instalacion = Instalacion.query.get(id)
    if not instalacion:
        return jsonify({'error': 'Facility not found'}), 404
    db.session.delete(instalacion)
    db.session.commit()
    return jsonify({'message': 'Facility deleted succesfully'}), 200
