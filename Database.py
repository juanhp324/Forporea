from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Conexión a la base de datos
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["Forporea"]

# ============================================
# INSERTAR USUARIOS
# ============================================
db.usuarios.insert_many([
    {
        "nombre": "Juan Administrador",
        "email": "admin@forporea.com",
        "password": "admin123",
        "rol": "admin"
    },
    {
        "nombre": "María Vendedora",
        "email": "maria@forporea.com",
        "password": "maria123",
        "rol": "vendedor"
    },
    {
        "nombre": "Carlos Usuario",
        "email": "carlos@forporea.com",
        "password": "carlos123",
        "rol": "usuario"
    }
])

# ============================================
# INSERTAR PROVEEDORES
# ============================================
db.proveedores.insert_many([
    {
        "nombre": "Embutidos del Norte S.A.",
        "contacto": "Juan Pérez",
        "telefono": "555-1234",
        "email": "contacto@embutidosnorte.com",
        "direccion": "Calle Principal 123, Ciudad Norte"
    },
    {
        "nombre": "Carnes Premium Ltda.",
        "contacto": "Ana García",
        "telefono": "555-5678",
        "email": "ventas@carnespremium.com",
        "direccion": "Avenida Industrial 456, Zona Este"
    },
    {
        "nombre": "Distribuidora La Española",
        "contacto": "Pedro Martínez",
        "telefono": "555-9012",
        "email": "info@laespanola.com",
        "direccion": "Boulevard Central 789, Centro"
    },
    {
        "nombre": "Productos Cárnicos del Sur",
        "contacto": "Laura Rodríguez",
        "telefono": "555-3456",
        "email": "contacto@carnicosdelsur.com",
        "direccion": "Carrera 10 #20-30, Sur"
    }
])

# Obtener IDs de proveedores
proveedor1 = db.proveedores.find_one({"nombre": "Embutidos del Norte S.A."})["_id"]
proveedor2 = db.proveedores.find_one({"nombre": "Carnes Premium Ltda."})["_id"]
proveedor3 = db.proveedores.find_one({"nombre": "Distribuidora La Española"})["_id"]
proveedor4 = db.proveedores.find_one({"nombre": "Productos Cárnicos del Sur"})["_id"]

# ============================================
# INSERTAR PRODUCTOS
# ============================================
db.productos.insert_many([
    {
        "nombre": "Chorizo Parrillero Premium",
        "descripcion": "Chorizo de cerdo premium especial para parrilla, 500g",
        "precio": 15.50,
        "stock": 150,
        "proveedor_id": proveedor1
    },
    {
        "nombre": "Salchichón Español",
        "descripcion": "Salchichón tipo español curado, 300g",
        "precio": 22.00,
        "stock": 80,
        "proveedor_id": proveedor3
    },
    {
        "nombre": "Jamón Serrano",
        "descripcion": "Jamón serrano curado 12 meses, 200g",
        "precio": 35.00,
        "stock": 45,
        "proveedor_id": proveedor3
    },
    {
        "nombre": "Salchicha Frankfurt",
        "descripcion": "Salchicha tipo Frankfurt, paquete de 8 unidades",
        "precio": 8.50,
        "stock": 200,
        "proveedor_id": proveedor2
    },
    {
        "nombre": "Mortadela Italiana",
        "descripcion": "Mortadela italiana con pistachos, 400g",
        "precio": 12.00,
        "stock": 120,
        "proveedor_id": proveedor2
    },
    {
        "nombre": "Longaniza Casera",
        "descripcion": "Longaniza artesanal estilo casero, 600g",
        "precio": 18.00,
        "stock": 90,
        "proveedor_id": proveedor1
    },
    {
        "nombre": "Salami Milano",
        "descripcion": "Salami tipo Milano, 250g",
        "precio": 16.50,
        "stock": 110,
        "proveedor_id": proveedor3
    },
    {
        "nombre": "Butifarra Catalana",
        "descripcion": "Butifarra catalana tradicional, 500g",
        "precio": 14.00,
        "stock": 75,
        "proveedor_id": proveedor4
    },
    {
        "nombre": "Chorizo Español Picante",
        "descripcion": "Chorizo español picante curado, 400g",
        "precio": 19.00,
        "stock": 95,
        "proveedor_id": proveedor3
    },
    {
        "nombre": "Morcilla de Burgos",
        "descripcion": "Morcilla de Burgos con arroz, 350g",
        "precio": 11.50,
        "stock": 60,
        "proveedor_id": proveedor4
    },
    {
        "nombre": "Pepperoni Premium",
        "descripcion": "Pepperoni premium para pizza, 300g",
        "precio": 13.00,
        "stock": 140,
        "proveedor_id": proveedor2
    },
    {
        "nombre": "Salchicha Bratwurst",
        "descripcion": "Salchicha alemana Bratwurst, 500g",
        "precio": 17.50,
        "stock": 85,
        "proveedor_id": proveedor1
    }
])

# Obtener IDs de productos y usuario
producto1 = db.productos.find_one({"nombre": "Chorizo Parrillero Premium"})["_id"]
producto2 = db.productos.find_one({"nombre": "Salchichón Español"})["_id"]
producto3 = db.productos.find_one({"nombre": "Jamón Serrano"})["_id"]
producto4 = db.productos.find_one({"nombre": "Salchicha Frankfurt"})["_id"]
usuario1 = db.usuarios.find_one({"email": "admin@forporea.com"})["_id"]

# ============================================
# INSERTAR FACTURAS
# ============================================
db.facturas.insert_many([
    {
        "cliente": "Restaurante El Buen Sabor",
        "fecha": datetime(2024, 11, 1, 10, 30, 0),
        "productos": [
            {
                "producto_id": producto1,
                "nombre": "Chorizo Parrillero Premium",
                "cantidad": 10,
                "precio_unitario": 15.50,
                "subtotal": 155.00
            },
            {
                "producto_id": producto2,
                "nombre": "Salchichón Español",
                "cantidad": 5,
                "precio_unitario": 22.00,
                "subtotal": 110.00
            }
        ],
        "total": 265.00,
        "usuario_id": usuario1
    },
    {
        "cliente": "Supermercado La Esquina",
        "fecha": datetime(2024, 11, 2, 14, 15, 0),
        "productos": [
            {
                "producto_id": producto3,
                "nombre": "Jamón Serrano",
                "cantidad": 8,
                "precio_unitario": 35.00,
                "subtotal": 280.00
            },
            {
                "producto_id": producto4,
                "nombre": "Salchicha Frankfurt",
                "cantidad": 15,
                "precio_unitario": 8.50,
                "subtotal": 127.50
            },
            {
                "producto_id": producto1,
                "nombre": "Chorizo Parrillero Premium",
                "cantidad": 12,
                "precio_unitario": 15.50,
                "subtotal": 186.00
            }
        ],
        "total": 593.50,
        "usuario_id": usuario1
    },
    {
        "cliente": "Hotel Plaza Mayor",
        "fecha": datetime(2024, 11, 3, 9, 45, 0),
        "productos": [
            {
                "producto_id": producto2,
                "nombre": "Salchichón Español",
                "cantidad": 20,
                "precio_unitario": 22.00,
                "subtotal": 440.00
            }
        ],
        "total": 440.00,
        "usuario_id": usuario1
    },
    {
        "cliente": "Cafetería Central",
        "fecha": datetime(2024, 11, 5, 16, 20, 0),
        "productos": [
            {
                "producto_id": producto4,
                "nombre": "Salchicha Frankfurt",
                "cantidad": 25,
                "precio_unitario": 8.50,
                "subtotal": 212.50
            },
            {
                "producto_id": producto1,
                "nombre": "Chorizo Parrillero Premium",
                "cantidad": 8,
                "precio_unitario": 15.50,
                "subtotal": 124.00
            }
        ],
        "total": 336.50,
        "usuario_id": usuario1
    }
])

print("Datos insertados correctamente!")