"""
Script para crear una nueva versión en la base de datos
Este script debe ejecutarse después de hacer un commit
"""
import subprocess
import sys
from infrasture.model.MVersiones import createVersion

def get_git_info():
    """Obtiene información del último commit de Git"""
    try:
        # Obtener hash del commit
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        
        # Obtener hash corto
        commit_hash_short = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
        
        # Obtener mensaje del commit
        commit_message = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode('utf-8').strip()
        
        # Obtener autor del commit
        commit_author = subprocess.check_output(['git', 'log', '-1', '--pretty=%an']).decode('utf-8').strip()
        
        # Obtener email del autor
        commit_email = subprocess.check_output(['git', 'log', '-1', '--pretty=%ae']).decode('utf-8').strip()
        
        # Obtener fecha del commit
        commit_date = subprocess.check_output(['git', 'log', '-1', '--pretty=%ci']).decode('utf-8').strip()
        
        # Obtener rama actual
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
        
        # Obtener archivos modificados
        files_changed = subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD']).decode('utf-8').strip().split('\n')
        
        return {
            'commit_hash': commit_hash,
            'commit_hash_short': commit_hash_short,
            'commit_message': commit_message,
            'commit_author': commit_author,
            'commit_email': commit_email,
            'commit_date': commit_date,
            'branch': branch,
            'files_changed': [f for f in files_changed if f]  # Filtrar líneas vacías
        }
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener información de Git: {e}")
        return None
    except FileNotFoundError:
        print("Git no está instalado o no está en el PATH")
        return None

def create_new_version(version_number=None, description=None):
    """Crea una nueva versión en la base de datos"""
    git_info = get_git_info()
    
    if not git_info:
        print("No se pudo obtener información de Git")
        return False
    
    # Si no se proporciona número de versión, usar el hash corto
    if not version_number:
        version_number = f"v-{git_info['commit_hash_short']}"
    
    # Si no se proporciona descripción, usar el mensaje del commit
    if not description:
        description = git_info['commit_message']
    
    version_data = {
        'version': version_number,
        'descripcion': description,
        'commit_hash': git_info['commit_hash'],
        'commit_hash_short': git_info['commit_hash_short'],
        'commit_message': git_info['commit_message'],
        'autor': git_info['commit_author'],
        'email': git_info['commit_email'],
        'commit_date': git_info['commit_date'],
        'branch': git_info['branch'],
        'archivos_modificados': git_info['files_changed'],
        'total_archivos': len(git_info['files_changed'])
    }
    
    try:
        result = createVersion(version_data)
        print(f"✅ Versión creada exitosamente: {version_number}")
        print(f"   Commit: {git_info['commit_hash_short']}")
        print(f"   Mensaje: {git_info['commit_message']}")
        print(f"   Autor: {git_info['commit_author']}")
        print(f"   Archivos modificados: {len(git_info['files_changed'])}")
        return True
    except Exception as e:
        print(f"❌ Error al crear versión: {e}")
        return False

if __name__ == "__main__":
    # Permitir pasar versión y descripción como argumentos
    version = sys.argv[1] if len(sys.argv) > 1 else None
    description = sys.argv[2] if len(sys.argv) > 2 else None
    
    create_new_version(version, description)
