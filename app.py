from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.database import BaseDatos
from datetime import date
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = 'clave secreta'

bd = BaseDatos()

usuarios_col = bd.obtener_colecciones('usuarios')
cuentas_col = bd.obtener_colecciones('cuenta_bancaria')
transacciones_col = bd.obtener_colecciones('transaccion')


@app.route('/', methods=['GET','POST'])
def login():

    if len(session) > 0:

        if session['rol'] == 'admin':
            return redirect(url_for('dashboard_admin'))
        
        elif session['rol'] == 'cliente':
            return redirect(url_for('dashboard_cliente'))
        
        elif session['rol'] == 'empleado':
            return redirect(url_for('dashboard_empleado'))    
    
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

        # Sacar nombre y apellidos desde la lista de usuarios

        lista_usuarios = bd.lista_usuarios(usuarios_col)

        for usuario in lista_usuarios:
            if usuario['dni'] == dni:
                nombre = usuario['nombre']
                apellidos = usuario['apellidos']

        cuentas_cliente = []
        saldo_total = 0.0

        cuentas = bd.lista_cuentas(cuentas_col)

        for cuenta in cuentas:
            if cuenta['dni_titular'] == dni:
                cuentas_cliente.append(cuenta)
                saldo_total += float(cuenta['saldo'])
                saldo_total = round(saldo_total,2)

        return render_template('usuario/dashboard_cliente.html',nombre=nombre,apellidos=apellidos,cuentas_cliente=cuentas_cliente,num_cuentas=len(cuentas_cliente),saldo_total=saldo_total)
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))
    
@app.route('/transferencias')
def transferencias():

    if 'username' in session and session.get('rol') == 'cliente':
        dni = session.get('dni')

        # Obtener transferencias realizadas desde cuentas del cliente

        lista_transfer = bd.lista_transacciones(transacciones_col)

        user_transfer = []

        for transfer in lista_transfer:
            if transfer['dni_ordena'] == dni:
                user_transfer.append(transfer)

        return render_template('usuario/transferencia.html', user_transfer=user_transfer)
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))
    
@app.route('/transferencias/<dni>', methods=['GET','POST'])
def crear_transfer(dni):

    cuentas_cliente = list(cuentas_col.find({'dni_titular': dni.upper()}))

    if request.method == 'POST':
        cuenta_origen_id = int(request.form.get('cuenta_origen'))
        cuenta_destino_id = int(request.form.get('cuenta_destino'))
        concepto = request.form.get('concepto')
        monto = float(request.form.get('monto'))

        cuenta_origen = cuentas_col.find_one({'id_cuenta' : cuenta_origen_id})
        cuenta_destino = cuentas_col.find_one({'id_cuenta' : cuenta_destino_id})

        if not cuenta_origen or not cuenta_destino:
            flash('La cuenta de origen o destino es inválida')
            return render_template('usuario/transferencia.html')
        
        if cuenta_origen['saldo'] < monto:
            flash('Saldo insuficiente')
            return redirect(url_for('transferencias'))
        
        # Actualizar saldos
        cuentas_col.update_one(
            {'id_cuenta' : cuenta_origen_id},
            {'$inc' : {'saldo' : -monto}}
        )

        cuentas_col.update_one(
            {'id_cuenta' : cuenta_destino_id},
            {'$inc' : {'saldo' : +monto}}
        )

        # Registrar transferencias
        lista_transfers = bd.lista_transacciones(transacciones_col)

        if lista_transfers:
            # Sacamos el último id_transfer de la lista y le sumamos 1, así es autonumérico
            next_id = lista_transfers[-1]['id_transfer'] + 1
        else:
            next_id = 1

        nueva_transfer = {
            'id_transfer' : next_id,
            'cuenta_origen' : cuenta_origen_id,
            'cuenta_destino' : cuenta_destino_id,
            'dni_ordena' : dni,
            'concepto' : concepto,
            'monto' : monto,
            'fecha' : date.today().strftime('%d/%m/%Y')
        }

        transacciones_col.insert_one(nueva_transfer)
        flash('Transferencia realizada correctamente')
        return redirect(url_for('transferencias'))
    
    return render_template('usuario/crear_transferencia.html', cuentas=cuentas_cliente, transfer={})

@app.route('/efectivo', methods=['GET', 'POST'])
def efectivo():

    if 'username' in session and session.get('rol') == 'cliente':
        dni = session.get('dni')

        cuentas_cliente = cuentas_col.find({'dni_titular': dni})

        if request.method == 'POST':
            cuenta_id = int(request.form.get('cuenta_origen'))
            monto = float(request.form.get('monto'))

            cuenta_origen = cuentas_col.find_one({'id_cuenta' : cuenta_id})
            
            if not cuenta_origen:
                flash('La cuenta de origen es inválida')
                return render_template('usuario/efectivo.html')
            
            if cuenta_origen['saldo'] > 0:
            
                if monto > cuenta_origen['saldo']:
                    flash('Saldo insuficiente')
                    return redirect(url_for('efectivo'))

                else:           
                    # Actualizar saldos

                    cuentas_col.update_one(
                        {'id_cuenta' : cuenta_id},
                        {'$inc' : {'saldo' : +monto}}
                    )

                    flash('Operación de efectivo realizada correctamente')
                    return redirect(url_for('efectivo'))
            
            else:
                # Actualizar saldos

                cuentas_col.update_one(
                    {'id_cuenta' : cuenta_id},
                    {'$inc' : {'saldo' : +monto}}
                )

                flash('Operación de efectivo realizada correctamente')
                return redirect(url_for('efectivo'))
        
        return render_template('usuario/efectivo.html', cuentas=cuentas_cliente)
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))


# END POINTS ADMINISTRADOR #

@app.route('/dashboard_admin')
def dashboard_admin():

    if 'username' in session and session.get('rol') == 'admin':
        fecha = date.today()
        fecha_norm = fecha.strftime('%d/%m/%Y')

        return render_template('admin/dashboard_admin.html',fecha=fecha_norm)

    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout')) 
    
@app.route('/admin_users')
def admin_user():
    
    if 'username' in session and session.get('rol') == 'admin':        
        usuarios = bd.lista_usuarios(usuarios_col)
        lista_usuarios = []

        for usuario in usuarios:
            if usuario['rol'] != 'admin':
                lista_usuarios.append(usuario)

        return render_template('admin/admin_users.html',lista_usuarios=lista_usuarios)

    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout')) 
    
@app.route('/admin_users/<user>/edit', methods=['GET','POST'])
def admin_editar_usuario(user):

    if 'username' in session and session.get('rol') == 'admin':
        
        if request.method == 'POST':
            edit_user = {
                'nombre' : request.form.get('nombre').title(),
                'apellidos' : request.form.get('apellidos').title(),
                'rol' : request.form.get('rol').lower()
            }
            
            usuarios_col.update_one(
                {'dni' : user},
                {'$set' :
                    {   'nombre': edit_user['nombre'].title(),
                        'apellidos' : edit_user['apellidos'].title(),
                        'rol' : edit_user['rol'].lower()}
                }
            )

            flash('Usuario actualizado correctamente')
            return redirect(url_for('admin_user', usuario=user))
        
        datos_usuario = usuarios_col.find_one({'dni' : user})        
        return render_template('admin/editar_usuario.html', usuario=datos_usuario)

    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))
    
@app.route('/admin_users/<user>/delete', methods=['POST'])
def eliminar_usuario(user):

        if 'username' in session and session.get('rol') == 'admin':
            usuarios_col.delete_one({'dni' : user})
            flash('Usuario eliminado con éxito')
            return redirect(url_for('admin_user'))
    
        else:
            flash('Acceso no autorizado')
            return redirect(url_for('logout'))


# END POINTS EMPLEADOS #

@app.route('/dashboard_empleado')
def dashboard_empleado():    

    if 'username' in session and session.get('rol') == 'empleado':
        
        dni = session.get('dni')
        user =usuarios_col.find_one({'dni':dni})
        usuarios = bd.lista_usuarios(usuarios_col)
        clientes = []
        for cliente in usuarios:
                if cliente['rol'] == 'cliente':
                    clientes.append(cliente)

        return render_template('empleado/dashboard_empleado.html',dni=dni,clientes = clientes,user=user)
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))

@app.route('/cuentas_cliente/<cliente>')
def mostrar_cuentas(cliente):
    
    if 'username' in session and session.get('rol') == 'empleado':
        dni = session.get('dni')
        user =usuarios_col.find_one({'dni':dni})
        usuarios = bd.lista_usuarios(usuarios_col)
        cuentas = bd.lista_cuentas(cuentas_col)
        cuentas_cliente=[]
        cliente_found = None
        total_saldo =0

        for elemento in usuarios:
            if elemento['dni'] == cliente:
                cliente_found = elemento
                break
        if cliente_found:
            for cuenta in cuentas:
                if cliente_found['dni'] ==cuenta['dni_titular']:
                    cuentas_cliente.append(cuenta)

        for saldo in cuentas_cliente:
            total_saldo+=saldo['saldo']
            return render_template('empleado/cuentas_cliente.html', cuentas=cuentas_cliente,cliente_found=cliente_found,total_saldo=total_saldo,user=user)
        else:
            return render_template('404.html')
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))    

    
@app.route('/crear_cuenta/<dni>')
def crear_cuenta(dni):
    datos_cliente = usuarios_col.find_one({'dni' : dni})    
        
    cuentas = bd.lista_cuentas(cuentas_col)
    fecha = date.today()
    fecha_norm = fecha.strftime('%d/%m/%Y')
    
    if not cuentas:
        cuenta_nueva={
        'id_cuenta':1,
        'dni_titular':datos_cliente['dni'].upper(),
        'telefono' : datos_cliente['telefono'],
        'saldo':0,
        'fecha_titular':fecha_norm        
        }
        bd.insertar_cuenta(cuenta_nueva)
        flash('Cuenta creada correctamente') 
    
    else:
        cuenta_nueva={
            'id_cuenta':cuentas[-1]['id_cuenta']+1,
            'dni_titular':datos_cliente['dni'].upper(),
            'telefono' : datos_cliente['telefono'],
            'saldo':0,
            'fecha_titular':fecha_norm        
        }
        bd.insertar_cuenta(cuenta_nueva)
        flash('Cuenta creada correctamente')

    return redirect(url_for('mostrar_cuentas',cliente=dni))


@app.route('/editar_cuenta/<id_cuenta>',methods=['GET','POST'])
def editar_cuenta(id_cuenta):    

    if 'username' in session and session.get('rol') == 'empleado':
        dni = session.get('dni')
        user =usuarios_col.find_one({'dni':dni})
        if request.method == 'POST':
            
            fecha = date.today()
            fecha_norm = fecha.strftime('%d/%m/%Y')
            datos_cuenta ={
                'dni_titular':request.form.get('dni_nuevo').upper(),
                'telefono':request.form.get('telefono_nuevo'),
                'fecha_titular':fecha_norm
            }
            cuentas_col.update_one(
                {'id_cuenta' : int(id_cuenta)},
                {'$set' :
                    {   'dni_titular': datos_cuenta['dni_titular'].upper(),
                        'telefono' : datos_cuenta['telefono'],
                        'fecha_titular' : datos_cuenta['fecha_titular']}
                }
            )
            
            flash('Usuario actualizado correctamente')
            return redirect(url_for('mostrar_cuentas', cliente=datos_cuenta['dni_titular']))
        
        
        cuenta_cliente=cuentas_col.find_one({'id_cuenta':int(id_cuenta)})
        cliente_found=usuarios_col.find_one({'dni':cuenta_cliente['dni_titular']})
        return render_template('empleado/editar_cuenta.html', id_cuenta=id_cuenta,cliente_found=cliente_found,user=user)
        
        
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))

@app.route('/borrar_cuenta/<id_cuenta>',methods=['POST'])
def eliminar_cuenta(id_cuenta):

    if 'username' in session and session.get('rol') == 'empleado':
        datos_cuenta = cuentas_col.find_one({'id_cuenta' :int(id_cuenta)})
        cuentas_col.delete_one({'id_cuenta' : int(id_cuenta)})
        flash('Cuenta eliminada con éxito')
        return redirect(url_for('mostrar_cuentas',cliente=datos_cuenta['dni_titular']))
    
    else:
        flash('Acceso no autorizado')
        return redirect(url_for('logout'))
        
# END POINT LOGOUT #

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__== '__main__':
    
    BaseDatos.inicializar_colecciones(BaseDatos())
    BaseDatos.insertar_admin(BaseDatos())
    app.run()

