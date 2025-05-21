class CuentaBancaria:
    def __init__(self,id_cuenta,dni_titular,telefono,saldo,fecha_creacion):
        self.__id_cuenta = id_cuenta
        self.__dni_titular = dni_titular
        self.__telefono = telefono
        self.__saldo = saldo
        self.__fecha_creacion = fecha_creacion