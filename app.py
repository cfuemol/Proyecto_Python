from flask import Flask, render_template, request, redirect, url_for, session, flash
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        formulario = request.form.get('formulario')
        if formulario =='sign-up':
            username = request.form.get('Username')
            dni = request.form.get('DNI')
            telefono = request.form.get('phone')
            email = request.form.get('Email')
            password = pbkdf2_sha256.hash(request.form.get('Password'))
            conf_password = pbkdf2_sha256.hash (request.form.get('Conf_password'))

        
        elif formulario == 'log-in':
            username = request.form.get('Username')
            password = request.form.get('Password')
        

        
    

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

