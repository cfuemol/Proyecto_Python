### Aquí ponemos todas las consultas que realizaremos a la BBDD ###

from models.database import BaseDatos
from datetime import datetime


### Consultas del Administrador del Sistema ###
### Consultas del Empleado ###

    ## Empleado usa consultar_cuenta_cliente para buscar ##

def consultar_total_clientes(dni):
    try:
        db = BaseDatos()

        consulta = """SELECT u.nombre, u.apellidos, u.dni, SUM(cb.saldo) AS saldo_total 
                        FROM usuarios u JOIN cuentas_bancarias cb ON u.dni = cb.dni_titular
                            GROUP BY u.dni;"""
        
        db.ejecutar_consulta(consulta,(dni,))
        resultado = db.resultado_consulta()
        db.cerrar_conexion()

        return resultado
    
    except Exception as e:
        print(f'\n¡¡¡ERROR al buscar al cliente {e}!!!')

    finally:
        db.cerrar_conexion()

def crear_cuenta_bancaria(dni,telefono,saldo):
    try:
        db = BaseDatos()

        consulta = """INSERT INTO usuarios (dni, telefono, saldo)
                        VALUES(?, ?, ?);"""
        
        db.ejecutar_consulta(consulta,(dni,telefono,saldo))
        db.cerrar_conexion()

    except Exception as e:
        print(f'\n¡¡¡ERROR al buscar al cliente {e}!!!')

    finally:
        db.cerrar_conexion()


### Consultas del Usuario - Cliente ###

def consultar_cuenta_cliente(dni):
    try:
        db = BaseDatos()

        consulta = """SELECT * FROM cuentas_bancarias WHERE dni_titular = ?;"""
        db.ejecutar_consulta(consulta,(dni,))
        resultado = db.resultado_consulta()
        db.cerrar_conexion()

        return resultado
    
    except Exception as e:
        print(f'\n¡¡¡ERROR al buscar al cliente {e}!!!')

    finally:
        db.cerrar_conexion()

def consultar_transferencia_cliente(dni):

    ## Con esta consulta vamos a conseguir todas las transferencias realizadas ##
    ## y/o recibidas en las cuentas de un cliente ##

    try:
        db = BaseDatos()

        consulta = """SELECT * FROM transacciones WHERE cuenta_origen 
                        IN (SELECT id_cuenta FROM cuentas_bancarias WHERE dni_titular = ?) 
                            OR cuenta_destino IN (SELECT id_cuenta FROM cuentas_bancarias WHERE dni_titular = ?);"""
        
        db.ejecutar_consulta(consulta,(dni,))
        resultado = db.resultado_consulta()
        db.cerrar_conexion()

        return resultado

    except Exception as e:
        print(f'\n¡¡¡ERROR al buscar al cliente {e}!!!')

    finally:
        db.cerrar_conexion()

def hacer_transferencia(origen,destino,concepto,monto):
    try:
        if origen == destino:
            raise ValueError("No se pueden hacer transferencias a la misma cuenta.")
        
        db = BaseDatos()

        # Verificar si el saldo es suficiente para hacer la operación
        resultado = db.ejecutar_consulta('SELECT saldo FROM cuentas_bancarias WHERE id_cuenta = ?',(origen,))

        if resultado[0][0] < monto:
            raise ValueError('Saldo insuficiente en la cuenta de origen')            

        consulta = """INSERT INTO transacciones (cuenta_origen, cuenta_destino, concepto, monto) VALUES (?, ?, ?, ?);"""
        
        actualiza_origen = """UPDATE cuentas_bancarias SET saldo = saldo - ? WHERE id_cuenta = ?;"""
        actualiza_destino = """UPDATE cuentas_bancarias SET saldo = saldo + ? WHERE id_cuenta = ?;"""

        # Realizar la transacción
        db.ejecutar_consulta(consulta(origen,destino,concepto,monto))

        # Actualizar saldo cuenta origen
        db.ejecutar_consulta(actualiza_origen,(monto,origen))

        # Actualizar saldo cuenta destino
        db.ejecutar_consulta(actualiza_destino,(monto,destino))

        db.cerrar_conexion()

    except Exception as e:
        if db:
            db.ejecutar_consulta('ROLLBACK')

        print(f'\n¡¡¡ERROR al realizar la transferencia!!!\nDetalles: {e}')

    finally:
        if db:
            db.cerrar.conexion()

def operacion_efectivo(origen,monto,opcion):

    try:
        if opcion == 'ingresar':
            db = BaseDatos()
            actualizar_saldo = """UPDATE cuentas_bancarias SET saldo = saldo + ? WHERE id_cuenta = ?;"""

            db.ejecutar_consulta(actualizar_saldo,(monto,origen))
            db.cerrar_conexion()

        elif opcion == 'retirar':
            
            # Verificar si el saldo de la cuenta es suficiente para hacer la operacion
            resultado = db.ejecutar_consulta('SELECT saldo FROM cuentas_bancarias WHERE id_cuenta = ?',(origen,))
            
            if resultado[0][0] < monto:
                raise ValueError('Saldo insuficiente en la cuenta de origen') 
            
            actualizar_saldo = """UPDATE cuentas_bancarias SET saldo = saldo - ? WHERE id_cuenta = ?;"""

            db.ejecutar_consulta(actualizar_saldo,(monto,origen))
            db.cerrar_conexion()

    except Exception as e:
        if db:
            db.ejecutar_consulta('ROLLBACK')

        print(f'\n¡¡¡ERROR al realizar la transferencia!!!\nDetalles: {e}')

    finally:
        if db:
            db.cerrar.conexion()


