class CuentaBancaria:
    #Constructor de la clase
    def __init__(self,id_cuenta:int,dni_titular:str,telefono:str,saldo:float,fecha_creacion:str):
        self.__id_cuenta = id_cuenta
        self.__dni_titular = dni_titular
        self.__telefono = telefono
        self.__saldo = saldo
        self.__fecha_creacion = fecha_creacion

    #ID Cuenta
    def get_id_cuenta(self):
        return self.__id_cuenta
    
    def set_id_cuenta(self, id_cuenta_nuevo:int):
        self.__id_cuenta = id_cuenta_nuevo

    #DNI Titular de la cuena
    def get_dni_titular(self):
        return self.__dni_titular
    
    def set_dni_titular(self, dni_titular_nuevo:str):
        self.__dni_titular = dni_titular_nuevo
    
    #Teléfono vinculado a la cuenta
    def get_telefono(self):
        return self.__telefono
    
    def set_telefono(self, telefono_nuevo:str):
        self.__telefono = telefono_nuevo

    #Saldo de la cuenta
    def get_saldo(self):
        return self.__saldo
    
    def set_saldo(self, saldo_nuevo:float):
        self.__saldo = saldo_nuevo

    #Fecha de Creación de la cuenta
    def get_fecha_creacion(self):
        return self.__fecha_creacion
    
    def set_fecha_creacion(self, fecha_creacion_nuevo:str):
        self.__fecha_creacion = fecha_creacion_nuevo

    #STR
    def __str__(self):
        return (f'CUENTA BANCARIA \nID Cuenta: {self.__id_cuenta}, DNI Titular: {self.__dni_titular}, Teléfono: {self.__telefono}, Saldo: {self.__saldo}, Fecha de Creación: {self.__fecha_creacion}.')
    
