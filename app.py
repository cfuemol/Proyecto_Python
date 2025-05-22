from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.database import BaseDatos
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

bd = BaseDatos()

usuarios_col = bd.obtener_colecciones('usuarios')
cuentas_col = bd.obtener_colecciones('cuenta_bancaria')
transacciones_col = bd.obtener_colecciones('transacciones')

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        formulario = request.form.get['formulario']
        if formulario =='sign-up':
            username = request.form.get['Username']
            nombre = request.form.get['nombre']
            apellidos = request.form.get['apellidos']
            dni = request.form.get['DNI']
            telefono = request.form.get['phone']
            email = request.form.get['Email']
            password = request.form.get['Password']
            conf_password = request.form.get['Conf_password']
            if password == conf_password:
                password_hash= pbkdf2_sha256.hash(password)

                dict_usuario = {
                    'dni' : dni,
                    'nombre' : nombre,
                    'apellidos' : apellidos,
                    'telefono' : telefono,
                    'email' : email,
                    'username' : username,
                    'password' : password_hash,
                    'rol' : 'cliente'
                }
                
            
        elif formulario == 'log-in':
            username = request.form.get['Username']
            password = request.form.get['Password']
        

        bd.insertar_user(dict_usuario)
    

    return render_template('login.html')

@app.route('/dashboard_cliente')
def dashboard_cliente():
    return render_template('dashboard_cliente.html')

@app.route('/dashboard_admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')

@app.route('/dashboard_empleado')
def dashboard_empleado():
    return render_template('dashboard_empleado.html')
    
if __name__== '__main__':
    app.run()
    BaseDatos.inicializar_colecciones()
    BaseDatos.insertar_admin()

