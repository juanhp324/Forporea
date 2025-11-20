import infrasture.model.MAuth as MAuth
from flask import url_for, redirect, session, request

class authValidator:
    def __init__(self, app):
        self.app = app
        self.app.before_request(self.verify_authentication)
        self.app.add_url_rule('/', 'index', self.index)

    def verify_authentication(self):
        RUTAS_ENDPOINTS_PUBLICOS = ['RAuth.show_login_form', 'RAuth.Login', 'RAuth.logout', 'RAuth.get_latest_version']
        RUTAS_ENDPOINTS_PROTEGIDOS = [
            'RInicio.inicio', 'RInicio.get_user_info',
            'RProductos.productos', 'RProductos.get_productos', 'RProductos.get_producto', 'RProductos.create_producto', 
            'RProductos.update_producto', 'RProductos.delete_producto',
            'RProveedores.proveedores', 'RProveedores.get_proveedores', 'RProveedores.get_proveedor', 'RProveedores.create_proveedor',
            'RProveedores.update_proveedor', 'RProveedores.delete_proveedor',
            'RFacturacion.facturacion', 'RFacturacion.facturas', 'RFacturacion.get_facturas', 'RFacturacion.get_productos_factura', 
            'RFacturacion.create_factura', 'RFacturacion.descargar_factura'
        ]
  
        if request.path.startswith('/static'):
            return
        if request.endpoint in RUTAS_ENDPOINTS_PUBLICOS:
            return
        if 'user_id' not in session:
            return redirect(url_for('RAuth.show_login_form'))
        if request.endpoint in RUTAS_ENDPOINTS_PROTEGIDOS:
            return

    def index(self):
        if 'user_id' in session:
            return redirect(url_for('RInicio.inicio'))
        return redirect(url_for('RAuth.show_login_form'))


class loginValidator:
    def __init__(self, *, is_json: bool, payLoad: dict):
        self.is_json = is_json
        self.payLoad = payLoad or {}
        self.email = self.payLoad.get('email')
        self.password = self.payLoad.get('password')
        self.userData = None
    
    def check_json(self):
        if not self.is_json:
            raise ValueError("Se espera JSON en la solicitud.")

    def check_credentials(self):
        if not self.email or not self.password:
            raise ValueError("Faltan email o contraseña en la solicitud.")

    def check_user(self):
        self.userData = MAuth.getUserByEmail(self.email)
        if not self.userData:
            raise LookupError("Usuario no encontrado")

    def check_password(self):
        if self.password != self.userData["password"]:
            raise PermissionError("Credenciales incorrectas")

    def redirect_user(self):
        return {
            "success": True,
            "message": "Autenticación correcta. Redirigiendo...",
            "redirect": url_for('RInicio.inicio')
        }
        
    def validation(self):
        self.check_json()
        self.check_credentials()
        self.check_user()
        self.check_password()
        return self.userData
