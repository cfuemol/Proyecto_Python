from pymongo import MongoClient
import os
from dotenv import load_dotenv

class BaseDatos:
    def __init__(self):
        try:
            # Cargar las variables de entorno
            load_dotenv()
            mong_url = os.getenv("MONGO_URL")

            # Conexión a MongoDB
            self.client = MongoClient(mong_url)
            self.db = self.client["Python_Bank"]

            self.inicializar_colecciones()

            print("✅ Conexión a MongoDB establecida correctamente.")

        except Exception as e:
            print(f"\n❌ Falló la conexión a MongoDB: {e}")

    def inicializar_colecciones(self):
        colecciones = ['cuenta_bancaria', 'transacción', 'usuarios']
        col_existentes = self.db.list_collection_names()

        for coleccion in colecciones:
            if coleccion not in col_existentes:
                self.db.create_collection(coleccion)
                print(f"📁 Colección '{coleccion}' creada.")

    def insertar_admin(self):
        
        #Sólo se ejecutará si la tabla usuarios está vacía

        if self.db['usuarios'].count_documents({}) == 0:
            usuario_inicial = {
                "dni": "99999999Z",
                "nombre": "Admin",
                "apellidos": "De la App",
                "telefono": "600123213",
                "email": "admin@pythonbank.com",
                "nombre_usuario": "adminuser",
                "passw": "admin123",
                "rol": "admin"
            }
            self.db['usuarios'].insert_one(usuario_inicial)
            print("👤 Usuario administrador insertado en la colección 'usuarios'.")
        else:
            print("⚠️ La colección 'usuarios' ya contiene registros.")

    def insertar_user(self, user):
        self.db['usuarios'].insert_one(user)

    # Nos devuelve la coleccion (tabla) cuyo nombre le especifiquemos
    def obtener_colecciones(self,nombre):
        return self.db[nombre]