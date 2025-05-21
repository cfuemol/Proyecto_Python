import sqlite3 as base_datos
from database.settings import DB_FILE
from flask import flash

class BaseDatos:
    def __init__(self):
        try:
            self.connection = base_datos.connect(DB_FILE)
            self.cursor = self.connection.cursor()

            # Script para crear las tabas si no existen
            self.crear_tablas()

            # Habilitar las FK
            self.ejecutar_consulta("PRAGMA foreign_keys = ON;")

        except:
            print(f'\nError en la BBDD, inténtelo de nuevo más tarde')

    def crear_tablas(self):
        tablas = """
            CREATE TABLE IF NOT EXISTS usuarios(
                dni TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                telefono TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                nombre_usuario TEXT UNIQUE NOT NULL,
                passw TEXT NOT NULL,
                rol TEXT DEFAULT 'cliente' CHECK (rol IN('admin','empleado','cliente'))
                );

            CREATE TABLE IF NOT EXISTS cuentas_bancarias(
                id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
                dni_titular TEXT NOT NULL,
                telefono TEXT UNIQUE NOT NULL,
                saldo REAL DEFAULT 0.0,
                fecha_creacion DATE DEFAULT CURRENT_DATE,

                FOREIGN KEY(dni_titular) REFERENCES usuarios(dni) 
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                );

            CREATE TABLE IF NOT EXISTS transacciones(
                id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                cuenta_origen INTEGER NOT NULL,
                cuenta_destino INTEGER NOT NULL,
                concepto TEXT NOT NULL,
                fecha DATE DEFAULT CURRENT_DATE,
                monto REAL NOT NULL,

                FOREIGN KEY(cuenta_origen) REFERENCES cuentas_bancarias(id_cuenta)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,

                FOREIGN KEY(cuenta_destino) REFERENCES cuentas_bancarias(id_cuenta)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                );

            -- Insertar los datos del administrador del sistema --

            INSERT INTO usuarios(dni,nombre,apellidos,telefono,email,nombre_usuario,passw,rol)
                VALUES('99999999Z','Admin','De la App','600123123','admin@pythonbank.com','adminuser','admin123','admin');

            """ 
        
        self.cursor.executescript(tablas)
        self.connection.commit()

    def ejecutar_consulta(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
                self.connection.commit()
            else:
                self.cursor.execute(query)
                self.connection.commit()

        except:
            print(f'\n¡¡¡Hay un error en la consulta, revísalo!!!')

    def resultado_consulta(self):
        return self.cursor.fetchall()
    
    def cerrar_conexion(self):
        self.connection.close()        