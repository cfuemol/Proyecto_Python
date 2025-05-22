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
        
        ### REGISTRO DE USUARIO ###        

        if formulario =='registro':
            passwd = request.form.get('passwd')

            # Hash de la contraseña #
            passwd_hash = pbkdf2_sha256.hash(passwd)

            # Crear diccionario con los datos de registro #
            dict_usuario = {
                'dni' : request.form.get('dni'),
                'nombre' : request.form.get('nombre'),
                'apellidos' : request.form.get('apellidos'),
                'telefono' : request.form.get('telefono'),
                'email' : request.form.get('email'),
                'username' : request.form.get('username'),
                'password' : passwd_hash,
                'rol' : 'cliente'
            }

            # Usuarios en formato lista
            usuarios = bd.lista_usuarios(usuarios_col)

            verifica = bd.comprueba_registro(usuarios,dict_usuario)

            match verifica:
                case 1:
                    flash('Ya existe un usuario con ese DNI')
                
                case 2:
                    flash('Ya existe un usuario con ese telefono')
                
                case 3:
                    flash('Ya existe un usuario con ese email')

                case 4:
                    flash('Ya existe un usuario con ese username')
                
                case 0:
                    flash('Usuario registrado correctamente')
                    bd.insertar_user(dict_usuario)
                    redirect(url_for('dashboard_cliente'))



                
            
        elif formulario == 'log-in':
            username = request.form.get['Username']
            password = request.form.get['Password']


    return render_template('login.html')

# END POINTS CLIENTES #

@app.route('/dashboard_cliente')
def dashboard_cliente():
    return render_template('dashboard_cliente.html', cliente=cliente)

# END POINTS ADMINISTRADOR #

@app.route('/dashboard_admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')

# END POINTS EMPLEADOS #

@app.route('/dashboard_empleado')
def dashboard_empleado():
    return render_template('dashboard_empleado.html')
    
if __name__== '__main__':
    app.run()
    BaseDatos.inicializar_colecciones()
    BaseDatos.insertar_admin()

