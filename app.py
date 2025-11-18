from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={
    r"/api/*": {
        "origins": Config.CORS_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Importar blueprints
from application.routes.RAuth import bp as RAuth_bp
from application.routes.RInicio import bp as RInicio_bp
from application.routes.RProductos import bp as RProductos_bp
from application.routes.RProveedores import bp as RProveedores_bp
from application.routes.RFacturacion import bp as RFacturacion_bp

# Registrar blueprints
app.register_blueprint(RAuth_bp, url_prefix='/api/auth')
app.register_blueprint(RInicio_bp, url_prefix='/api')
app.register_blueprint(RProductos_bp, url_prefix='/api')
app.register_blueprint(RProveedores_bp, url_prefix='/api')
app.register_blueprint(RFacturacion_bp, url_prefix='/api')

# Ruta de health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "API Forporea funcionando correctamente"
    }), 200

# Manejadores de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Error interno del servidor"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
