import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Nombre del archivo de la BBDD

DB_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
DB_FILE = DB_PATH = (os.getenv('DB'))

if not DB_FILE:
    raise ValueError("❌ Error: La variable de entorno DB no existe")
