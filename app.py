from flask import Flask, render_template, request, redirect, url_for, session, flash
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

@app.route('/')
def login():
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

