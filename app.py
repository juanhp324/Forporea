from flask import Flask, redirect, url_for, session, request

app = Flask(__name__, template_folder='presentation/templates', static_folder='presentation/static')

# Configuración de la clave secreta para las sesiones
app.secret_key = 'forporea_secret_key_embutidos_2024'

# Importar blueprints
from application.routes.RAuth import bp as RAuth_bp
from application.routes.RInicio import bp as RInicio_bp
from application.routes.RProductos import bp as RProductos_bp
from application.routes.RProveedores import bp as RProveedores_bp
from application.routes.RFacturacion import bp as RFacturacion_bp

# Importar validador de autenticación
from domain.VAuth import authValidator

# Registrar blueprints
app.register_blueprint(RAuth_bp)
app.register_blueprint(RInicio_bp)
app.register_blueprint(RProductos_bp)
app.register_blueprint(RProveedores_bp)
app.register_blueprint(RFacturacion_bp)

# Validaciones de autenticación
authValidator(app)

if __name__ == '__main__':
    app.run(debug=True)
