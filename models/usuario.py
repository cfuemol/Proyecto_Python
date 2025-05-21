class Usuario:
    #Contructor de la clase
    def __init__(self,dni:str,nombre:str,apellidos:str,telefono:str,email:str,user_name:str,password:str,rol:str):
        self.__dni = dni
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__telefono = telefono
        self.__email = email
        self.__user_name = user_name
        self.__password = password
        self.__rol = rol

    #Getter y Setter
    #DNI
    def get_dni(self):
        return self.__dni
    
    def set_dni(self,dni_nuevo:str):
        self.__dni = dni_nuevo

    #Nombre
    def get_nombre(self):
        return self.__nombre
    
    def set_nombre(self, nombre_nuevo:str):
        self.__nombre = nombre_nuevo

    #Apellidos
    def get_apellidos(self):
        return self.__apellidos
    
    def set_apellidos(self,apellidos_nuevos:str):
        self.__apellidos = apellidos_nuevos

    #Telefono
    def get_telefono(self):
        return self.__telefono
    
    def set_telefono(self, telefono_nuevo:str):
        self.__telefono = telefono_nuevo

    #E-mail
    def get_email(self):
        return self.__email
    
    def set_email(self, email_nuevo:str):
        self.__email = email_nuevo

    #User Name
    def get_user_name(self):
        return self.__user_name
    
    def set_user_name(self, user_name_nuevo:str):
        self.__user_name = user_name_nuevo

    #Password
    def get_password(self):
        return self.__password
    
    def set_password(self, password_nuevo:str):
        self.__password = password_nuevo

    #Rol
    def get_rol(self):
        return self.__rol
    
    def set_rol(self, rol_nuevo:str):
        self.__rol = rol_nuevo

    def __str__(self):
        return (f'USUARIO \nDNI: {self.__dni}, Nombre: {self.__nombre}, Apellidos: {self.__apellidos}, Teléfono: {self.__telefono}, E-mail: {self.__email}, User Name: {self.__user_name}, Password: {self.__password}, Rol: {self.__rol}')
    
