from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from mqtt import send_option
from registroSesionUsuario import registro, inicioSesion

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('Registro.html')

@app.route('/registro-exitoso', methods=['POST'])
def registro_exitoso():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        apellido = request.form['Apellidos']
        ID = request.form['Identificación']
        celular = request.form['celular']
        correo = request.form['Correo']
        password = generate_password_hash(request.form['password'])
        registro(nombre, apellido, ID, celular, correo, password)
        return render_template('registro_exitoso.html')

@app.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['Correo']
        password = request.form['pass']
        inicioSesion(usuario, password)
    else:
        return render_template('Inicio2.html')

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/osciloscopio')
def osciloscopio():
    send_option("osciloscopio")
    return render_template('osciloscopio.html')

@app.route('/generador', methods=['GET','POST'])
def generador():
    if request.method == 'POST':
        frec = request.form['frecuencia']
        duty = request.form['duty'] 
        send_option("generador", frec, duty)
    return render_template('generador.html')

if __name__ == '__main__':
    app.run(debug=True)