from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from mqtt import send_option 
from flaskext.mysql import MySQL
import paho.mqtt.client as mqtt
import time

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABAS_PASSWORD'] = 'l44bvmg2001'
app.config['MYSQL_DATABASE_DB'] = 'lab_movil'
mysql.init_app(app)

selector = None
selecMult = None
'''
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
'''


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
        cur = mysql.get_db().cursor()
        query = 'INSERT INTO tabla_lgjr (nombre, apellido, ID, celular, correo, password) VALUES (%s, %s, %s, %s, %s, %s)'
        cur.execute(query, (nombre, apellido, ID, celular, correo, password))
        cur.close()

        return render_template('registro_exitoso.html')

@app.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['Correo']
        password = request.form['pass']
        
        cur = mysql.get_db().cursor()
        query = "SELECT correo, password FROM tabla_lgjr WHERE correo = '{}'".format(usuario)
        cur.execute(query)
        row = cur.fetchone()
        cur.close()
        if row != None:
            if check_password_hash(row[1], password):
                return redirect(url_for('usuario'))
        else:
            return render_template('Inicio2.html')

    else:
        return render_template('Inicio2.html')

@app.route('/usuario')
def usuario():
    print(selector)
    global selecMult
    selecMult = "NADA"
    usuario = {
        "frecuencia": 1,
        "duty": 0,
        "voltPuerto1": 0,
        "voltPuerto2": 0,
        "enable": False,
        "tipoMult": None
    }
    send_option(selector, **usuario)
    return render_template('usuario.html')

@app.route('/osciloscopio')
def osciloscopio():
    osciloscopio = {
        "enable" : True
    }
    global selector
    selector = "osciloscopio"
    send_option("osciloscopio", **osciloscopio)
    return render_template('osciloscopio.html')

@app.route('/generador', methods=['GET','POST'])
def generador():
    if request.method == 'POST':
        global selector
        selector = "generador"
        
        send_option("generador",frecuencia = request.form['frecuencia'], duty = request.form['duty'], enable = True)
        
    return render_template('generador.html')

@app.route('/fuente', methods=['GET', 'POST'])
def fuente():
    if request.method == 'POST':
        global selector
        selector = "fuente"
        send_option("fuente", voltPuerto1= request.form['voltPuerto1'], voltPuerto2= request.form['voltPuerto2'], enable = True)
        
    return render_template('fuente.html')



@app.route('/multimetro')
def multimetro():
    multimetro = {
        "tipoMult": selecMult,
        "enable": True
    }
    send_option("multimetro",**multimetro)
    print(selecMult)
    global selector
    selector = "multimetro"
    return render_template('multimeterOption.html')

@app.route('/multimetro-voltaje')
def multimetro_voltaje():
    global selecMult
    selecMult = "voltMult"
    cur = mysql.get_db().cursor()
    query = 'SELECT voltaje FROM voltMult BY id DESC LIMIT 1'
    cur.execute(query)
    voltajeSQL = cur.fetchone()
    print(voltajeSQL)
    return redirect(url_for('multimetro'))

@app.route('/multimetro-corriente')
def multimetro_corriente():
    global selecMult
    selecMult = "corrienteMult"
    return redirect(url_for('multimetro'))

@app.route('/multimetro-continuidad')
def multimetro_continuidad():
    global selecMult
    selecMult = "continuidadMult"
    return redirect(url_for('multimetro'))


if __name__ == '__main__':
    app.run(debug=True)