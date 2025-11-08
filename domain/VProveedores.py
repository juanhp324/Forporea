from bson import ObjectId

class createProveedorValidator:
    def __init__(self, *, isJson: bool, payLoad: dict):
        self.isJson = isJson
        self.payLoad = payLoad or {}
        self.nombre = self.payLoad.get('nombre')
        self.contacto = self.payLoad.get('contacto')
        self.telefono = self.payLoad.get('telefono')
        self.email = self.payLoad.get('email')
        self.direccion = self.payLoad.get('direccion')

    def checkData(self):
        if not self.nombre or not self.contacto:
            raise ValueError("Faltan datos obligatorios (nombre y contacto)")

    def validation(self):
        self.checkData()
        return {
            "nombre": self.nombre,
            "contacto": self.contacto,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion
        }


class updateProveedorValidator:
    def __init__(self, *, isJson: bool, payLoad: dict):
        self.isJson = isJson
        self.payLoad = payLoad or {}
        self.nombre = self.payLoad.get('nombre')
        self.contacto = self.payLoad.get('contacto')
        self.telefono = self.payLoad.get('telefono')
        self.email = self.payLoad.get('email')
        self.direccion = self.payLoad.get('direccion')

    def checkData(self):
        if not self.nombre or not self.contacto:
            raise ValueError("Faltan datos obligatorios (nombre y contacto)")

    def validation(self):
        self.checkData()
        return {
            "nombre": self.nombre,
            "contacto": self.contacto,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion
        }


class getProveedorValidator:
    def __init__(self, *, proveedor_data):
        self.proveedor_data = proveedor_data

    def checkData(self):
        if not self.proveedor_data:
            raise LookupError('Proveedor no encontrado')

    def validation(self):
        self.checkData()
        return self.proveedor_data
