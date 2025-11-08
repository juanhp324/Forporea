from pymongo import MongoClient

# Configuración de la conexión
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "Forporea"

# Configuración optimizada para evitar timeouts
CONNECTION_CONFIG = {
    "serverSelectionTimeoutMS": 10000,  # 10 segundos
    "connectTimeoutMS": 10000,           # 10 segundos
    "socketTimeoutMS": 10000,            # 10 segundos
    "maxPoolSize": 50,                   # Pool de conexiones
    "minPoolSize": 10,                   # Mínimo de conexiones en el pool
    "maxIdleTimeMS": 45000,              # Tiempo máximo de inactividad
    "retryWrites": True,                 # Reintentar escrituras
    "retryReads": True,                  # Reintentar lecturas
    "w": "majority",                     # Write concern
    "journal": True                      # Journaling habilitado
}

# Crear una única instancia de cliente MongoDB (Singleton)
_client = None
_db = None

def get_database():
    """
    Obtiene la instancia de la base de datos.
    Crea la conexión si no existe (patrón Singleton).
    """
    global _client, _db
    
    if _client is None:
        try:
            _client = MongoClient(MONGODB_URI, **CONNECTION_CONFIG)
            # Verificar la conexión
            _client.admin.command('ping')
            _db = _client[DATABASE_NAME]
            print(f"[OK] Conexion exitosa a MongoDB: {DATABASE_NAME}")
        except Exception as e:
            print(f"[ERROR] Error al conectar a MongoDB: {e}")
            raise
    
    return _db

def close_connection():
    """Cierra la conexión a MongoDB"""
    global _client, _db
    
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        print("[OK] Conexion a MongoDB cerrada")

# Obtener la base de datos al importar el módulo
db = get_database()
