from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from db import db
from errors import register_error_handlers  # Asegúrate de tener este archivo
from routes.auth import auth_bp
from routes import usuarios, instalaciones, reservas, contacto  # Rutas de tu proyecto

# Inicialización de la aplicación
app = Flask(__name__)

# Configuración CORS (permitir acceso desde el frontend)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})

# Cargamos toda la configuración desde la clase Config
app.config.from_object(Config)

# Inicialización de JWT
jwt = JWTManager(app)

# Inicialización de la base de datos
db.init_app(app)


# Registro de blueprints
app.register_blueprint(auth_bp)  # Rutas para autenticación
app.register_blueprint(usuarios.bp)  # Rutas para gestionar usuarios
app.register_blueprint(instalaciones.bp)  # Rutas para instalaciones
app.register_blueprint(reservas.bp)  # Rutas para reservas
app.register_blueprint(contacto.bp)  # Rutas para contacto

# Registro de manejadores de errores personalizados
register_error_handlers(app)

# Si el archivo se ejecuta directamente, la app se corre en modo debug
if __name__ == '__main__':
    app.run(debug=True)
