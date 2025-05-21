class Transaccion:
    def __init__(self,id_transaccion:int,id_cuenta_origen:int,id_cuenta_destino:int,fecha:str,concepto:str,monto:float):
        self.__id_transaccion = id_transaccion
        self.__id_cuenta_origen = id_cuenta_origen
        self.__id_cuenta_destino = id_cuenta_destino
        self.__fecha = fecha
        self.__concepto = concepto
        self.__monto = monto

    #Getter y Setter
    #ID Transaccion
    def get_id_transaccion(self):
        return self.__id_transaccion
    
    def set_id_transaccion(self,id_transaccion_nuevo:int):
        self.__id_transaccion = id_transaccion_nuevo

    #ID Cuenta Origen
    def get_id_cuenta_origen(self):
        return self.__id_cuenta_origen
    
    def set_id_cuenta_origen(self, id_cuenta_origen_nuevo:int):
        self.__id_cuenta_origen = id_cuenta_origen_nuevo

    #ID Cuenta Destino
    def get_id_cuenta_destino(self):
        return self.__id_cuenta_destino
    
    def set_id_cuenta_destino(self,id_cuenta_destino_nuevo:int):
        self.__id_cuenta_destino = id_cuenta_destino_nuevo

    #Fecha
    def get_fecha(self):
        return self.__fecha
    
    def set_fecha(self, fecha_nuevo:str):
        self.__fecha = fecha_nuevo

    #Concepto
    def get_concepto(self):
        return self.__concepto
    
    def set_concepto(self,concepto_nuevo:str):
        self.__concepto = concepto_nuevo

    #Monto
    def get_monto(self):
        return self.__monto
    
    def set_monto(self, monto_nuevo:float):
        self.__monto = monto_nuevo

    def __str__(self):
        return (f'TRANSACCIÓN \nID Transacción: {self.__id_transaccion}, ID Cuenta Origen: {self.__id_cuenta_origen}, ID Cuenta Destino: {self.__id_cuenta_destino}, Fecha: {self.__fecha}, Concepto: {self.__concepto}, Monto: {self.__monto}.')
    
