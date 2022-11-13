from flask import Flask, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

def registro(nombre, apellido, ID, celular, correo, password):
    '''cur = mysql.get_db().cursor()
    query = 'INSERT INTO tabla_lgjr (nombre, apellido, ID, celular, correo, password) VALUES (%s, %s, %s, %s, %s, %s)'
    cur.execute(query, (nombre, apellido, ID, celular, correo, password))
    cur.close()'''
    print("CAMBIÓ")

def inicioSesion(usuario, password):
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
