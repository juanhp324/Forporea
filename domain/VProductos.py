from bson import ObjectId

class createProductoValidator:
    def __init__(self, *, isJson: bool, payLoad: dict):
        self.isJson = isJson
        self.payLoad = payLoad or {}
        self.nombre = self.payLoad.get('nombre')
        self.descripcion = self.payLoad.get('descripcion')
        self.precio = self.payLoad.get('precio')
        self.stock = self.payLoad.get('stock')
        self.proveedor_id = self.payLoad.get('proveedor_id')

    def checkData(self):
        if not self.nombre or not self.precio or not self.stock or not self.proveedor_id:
            raise ValueError("Faltan datos obligatorios")
        
        try:
            self.precio = float(self.precio)
            self.stock = float(self.stock)
            if self.precio <= 0 or self.stock <= 0:
                raise ValueError("Precio y stock deben ser mayores a 0")
        except ValueError:
            raise ValueError("Precio y stock deben ser números válidos")
        
        if not ObjectId.is_valid(self.proveedor_id):
            raise ValueError("ID de proveedor inválido")

    def validation(self):
        self.checkData()
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
            "proveedor_id": ObjectId(self.proveedor_id)
        }


class updateProductoValidator:
    def __init__(self, *, isJson: bool, payLoad: dict):
        self.isJson = isJson
        self.payLoad = payLoad or {}
        self.nombre = self.payLoad.get('nombre')
        self.descripcion = self.payLoad.get('descripcion')
        self.precio = self.payLoad.get('precio')
        self.stock = self.payLoad.get('stock')
        self.proveedor_id = self.payLoad.get('proveedor_id')

    def checkData(self):
        if not self.nombre or not self.precio or not self.stock or not self.proveedor_id:
            raise ValueError("Faltan datos obligatorios")
        
        try:
            self.precio = float(self.precio)
            self.stock = float(self.stock)
            if self.precio <= 0 or self.stock <= 0:
                raise ValueError("Precio y stock deben ser mayores a 0")
        except ValueError:
            raise ValueError("Precio y stock deben ser números válidos")
        
        if not ObjectId.is_valid(self.proveedor_id):
            raise ValueError("ID de proveedor inválido")

    def validation(self):
        self.checkData()
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
            "proveedor_id": ObjectId(self.proveedor_id)
        }


class getProductoValidator:
    def __init__(self, *, producto_data):
        self.producto_data = producto_data

    def checkData(self):
        if not self.producto_data:
            raise LookupError('Producto no encontrado')

    def validation(self):
        self.checkData()
        return self.producto_data
