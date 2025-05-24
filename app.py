from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.database import BaseDatos
from datetime import date
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

            login_user = None   # Inicializar
            hashed_password = None
            
            for usuario in usuarios:
                if usuario['username'] == username:

                    login_user = usuario                    
                    hashed_password = usuario['password']
                    break

            # Validar si existe el usuario y la contraseña
            
            if login_user and hashed_password and pbkdf2_sha256.verify(password, hashed_password):

                # Guardar datos en session

                session['username'] = login_user['username']
                session['rol'] = login_user['rol']
                session['dni'] = login_user.get('dni')

                # Redirección según el rol 

                if login_user['rol'] == 'cliente':            
                    return redirect (url_for('dashboard_cliente'))
                
                elif login_user['rol'] == 'empleado':            
                    return redirect (url_for('dashboard_empleado'))
                
                elif login_user['rol'] == 'admin':            
                    return redirect (url_for('dashboard_admin'))
            
            else:
                flash('Nombre de usuario o contraseña incorrecta.')

    return render_template('register.html')

# END POINTS CLIENTES #

@app.route('/dashboard_cliente')
def dashboard_cliente():
   
    
   
    if 'username' in session and session.get('rol') == 'cliente':
        dni = session.get('dni')
        return render_template('usuario/dashboard_cliente.html',dni=dni)
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('login'))

    
# END POINTS ADMINISTRADOR #

@app.route('/dashboard_admin')
def dashboard_admin():

    if 'username' in session and session.get('rol') == 'admin':
        fecha = date.today()
        fecha_norm = fecha.strftime('%d/%m/%Y')

        return render_template('admin/dashboard_admin.html',fecha=fecha_norm)

    else:
        flash('Acceso no autorizado')
        return redirect(url_for('login')) 
    
@app.route('/admin_users')
def admin_user():


# END POINTS EMPLEADOS #

@app.route('/dashboard_empleado')
def dashboard_empleado():
    usuarios = bd.lista_usuarios(usuarios_col)
    clientes = []
    for cliente in usuarios:
            if cliente['rol'] == 'cliente':
                clientes.append(cliente)

    if 'username' in session and session.get('rol') == 'empleado':
        dni = session.get('dni')
        return render_template('empleado/dashboard_empleado.html',dni=dni,clientes = clientes)
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('login'))

# END POINT LOGOUT #

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__== '__main__':
    
    BaseDatos.inicializar_colecciones(BaseDatos())
    BaseDatos.insertar_admin(BaseDatos())
    app.run()

