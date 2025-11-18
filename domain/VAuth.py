import infrasture.model.MAuth as MAuth

class loginValidator:
    def __init__(self, *, is_json: bool, payLoad: dict):
        self.is_json = is_json
        self.payLoad = payLoad or {}
        self.email = self.payLoad.get("email")
        self.password = self.payLoad.get("password")
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
        if self.password != self.userData.get("password"):
            raise PermissionError("Credenciales incorrectas")
        
    def validation(self):
        self.check_json()
        self.check_credentials()
        self.check_user()
        self.check_password()
        return self.userData
