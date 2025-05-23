from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.database import BaseDatos
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = 'clave secreta'

bd = BaseDatos()

usuarios_col = bd.obtener_colecciones('usuarios')
cuentas_col = bd.obtener_colecciones('cuenta_bancaria')
transacciones_col = bd.obtener_colecciones('transacciones')

@app.route('/', methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        formulario = request.form.get('action')
        print(formulario)
        
        ### REGISTRO DE USUARIO ###        

        if formulario =='registro':
            passwd = request.form.get('password')

            # Hash de la contraseña #
            passwd_hash = pbkdf2_sha256.hash(passwd)

            # Crear diccionario con los datos de registro #
            dict_usuario = {
                'dni' : request.form.get('dni').upper(),
                'nombre' : request.form.get('nombre').title(),
                'apellidos' : request.form.get('apellidos').title(),
                'telefono' : request.form.get('telefono'),
                'email' : request.form.get('email').lower(),
                'username' : request.form.get('username').lower(),
                'password' : passwd_hash,
                'rol' : 'cliente'
            }

            print(dict_usuario)

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
                    bd.insertar_user(dict_usuario)
                    flash('Usuario registrado correctamente')
                    return redirect(url_for('login'))

                
            
        elif formulario == 'log-in':
            usuarios = bd.lista_usuarios(usuarios_col)
            username = request.form.get('username2')
            password = request.form.get('password2')
            for usuario in usuarios:
                if usuario['username'] == username:
                    
                    hashed_password = usuario['password']
            if hashed_password and pbkdf2_sha256.verify(password, hashed_password):

                session['user'] = username
            
            return redirect (url_for('dashboard_cliente'))
            #else:
              #  return print('Nombre de usuario o contraseña incorrecta.')
            
            

    return render_template('register.html')

# END POINTS CLIENTES #

@app.route('/dashboard_cliente')
def dashboard_cliente():
    user=  session.get('user')
    return render_template('usuario/dashboard_cliente.html')

# END POINTS ADMINISTRADOR #

@app.route('/dashboard_admin')
def dashboard_admin():
    return render_template('admin/dashboard_admin.html')

# END POINTS EMPLEADOS #

@app.route('/dashboard_empleado')
def dashboard_empleado():
    return render_template('empleado/dashboard_empleado.html')
    
if __name__== '__main__':
    
    BaseDatos.inicializar_colecciones(BaseDatos())
    BaseDatos.insertar_admin(BaseDatos())
    app.run()

