from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro-exitoso')
def registro_exitoso():
    return render_template('registro_exitoso.html')

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')
if __name__ == '__main__':
    app.run(debug=True)