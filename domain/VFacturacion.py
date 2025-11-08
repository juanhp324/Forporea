from bson import ObjectId
from datetime import datetime

class createFacturaValidator:
    def __init__(self, *, isJson: bool, payLoad: dict):
        self.isJson = isJson
        self.payLoad = payLoad or {}
        self.cliente = self.payLoad.get('cliente')
        self.productos = self.payLoad.get('productos', [])

    def checkData(self):
        if not self.cliente:
            raise ValueError("Falta el nombre del cliente")
        
        if not self.productos or len(self.productos) == 0:
            raise ValueError("Debe agregar al menos un producto")
        
        for producto in self.productos:
            if not producto.get('producto_id') or not producto.get('cantidad'):
                raise ValueError("Cada producto debe tener ID y cantidad")
            
            try:
                producto['cantidad'] = int(producto['cantidad'])
            except ValueError:
                raise ValueError("La cantidad debe ser un número válido")

    def validation(self):
        self.checkData()
        return {
            "cliente": self.cliente,
            "productos": self.productos,
            "fecha": datetime.now(),
            "usuario_id": None  # Se asignará en la ruta
        }
