from flask import Flask, render_template, request, redirect, url_for, session, flash
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')


if __name__== '__main__':
    app.run()

