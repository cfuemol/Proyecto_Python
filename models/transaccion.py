class Transaccion:
    def __init__(self,id_transaccion,id_cuenta_origen,id_cuenta_destino,fecha,concepto,monto):
        self.__id_transaccion = id_transaccion
        self.__id_cuenta_origen = id_cuenta_origen
        self.__id_cuenta_destino = id_cuenta_destino
        self.__fecha = fecha
        self.__concepto = concepto
        self.__monto = monto