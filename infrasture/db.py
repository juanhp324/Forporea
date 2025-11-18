from pymongo import MongoClient
import threading
import os

# Configuración de la conexión
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://juanhp324_db_user:93J4a48Ex1Q0DW7O@forporeacluster.n0etmfd.mongodb.net/?retryWrites=true&w=majority&appName=ForporeaCluster")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Forporea")

# Configuración optimizada para evitar timeouts
CONNECTION_CONFIG = {
    "serverSelectionTimeoutMS": 5000,   # 5 segundos
    "connectTimeoutMS": 5000,            # 5 segundos
    "socketTimeoutMS": 5000,             # 5 segundos
    "maxPoolSize": 50,                   # Pool de conexiones
    "minPoolSize": 10,                   # Mínimo de conexiones en el pool
    "maxIdleTimeMS": 30000,              # 30 segundos de inactividad
    "retryWrites": True,                 # Reintentar escrituras
    "retryReads": True,                  # Reintentar lecturas
    "w": "majority",                     # Write concern
    "journal": True,                     # Journaling habilitado
    "waitQueueTimeoutMS": 5000           # Timeout para esperar conexión del pool
}

# Crear una única instancia de cliente MongoDB (Singleton)
_client = None
_db = None
_lock = threading.Lock()  # Lock para thread-safety

def get_database():
    """
    Obtiene la instancia de la base de datos.
    Crea la conexión si no existe (patrón Singleton).
    Thread-safe para evitar race conditions.
    """
    global _client, _db
    
    # Si ya existe la conexión, retornarla directamente
    if _client is not None and _db is not None:
        return _db
    
    # Usar lock solo cuando necesitamos crear/verificar la conexión
    with _lock:
        # Double-check: otro thread pudo haber creado la conexión
        if _client is not None and _db is not None:
            return _db
            
        try:
            _client = MongoClient(MONGODB_URI, **CONNECTION_CONFIG)
            # Verificar la conexión
            _client.admin.command('ping')
            _db = _client[DATABASE_NAME]
            print(f"[OK] Conexion exitosa a MongoDB: {DATABASE_NAME}")
        except Exception as e:
            print(f"[ERROR] Error al conectar a MongoDB: {e}")
            _client = None
            _db = None
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
