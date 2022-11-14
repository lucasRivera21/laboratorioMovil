from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from mqtt import send_option
from flaskext.mysql import MySQL

app = Flask(__name__)
'''
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABAS_PASSWORD'] = 'l44bvmg2001'
app.config['MYSQL_DATABASE_DB'] = 'lab_movil'
mysql.init_app(app)
'''
selector = ""
selecMult = ""

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
    send_option(selector, 0, 0, False)
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
        global selector
        selector = "generador"
        send_option("generador", frec, duty)
        
    return render_template('generador.html')

@app.route('/fuente', methods=['GET', 'POST'])
def fuente():
    if request.method == 'POST':
        volt1 = request.form['voltPuerto1']
        volt2 = request.form['voltPuerto2']
        global selector
        selector = "fuente"
        send_option("fuente", volt1, volt2)
    else:
        volt1 = 0
        volt2 = 0
        
    return render_template('fuente.html')



@app.route('/multimetro')
def multimetro():
    send_option("multimetro",selecMult,...,True)
    print(selecMult)
    global selector
    selector = "multimetro"
    return render_template('multimeterOption.html')

@app.route('/multimetro-voltaje')
def multimetro_voltaje():
    global selecMult
    selecMult = "voltMult"
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