from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.historial_precio import obtener_historial_precio_moneda
from controllers.top_monedas import obtener_top_monedas
from controllers.register import registrar_perfil
from controllers.login import get_perfiles
from conections.db_conector import conn

app = Flask(__name__)
CORS(app)

API_KEY = '3bb16e1c01fbcfe31c6a854789ca81e14fed82ab0b0a69afeeb0c9db849fb6b8'

@app.route('/login', methods=['POST'])
def verify_usuario():
    perfiles = get_perfiles()
    credenciales = request.get_json()
    for perfil in perfiles:
        if perfil == credenciales:
            return {"success": True}
    return {"success": False}

@app.route('/register', methods=['POST'])
def registrar():
    credenciales = request.get_json()
    registro = registrar_perfil(credenciales)
    print(registro)
    return registro

@app.route('/top_monedas')
def mostrar_top_monedas():
    top_monedas = obtener_top_monedas(API_KEY)
    if top_monedas is not None:
        return jsonify(top_monedas)
    else:
        return 'Error al consultar los datos de CryptoCompare'

@app.route('/historial_precio/<symbol>')
def obtener_historial_precio(symbol):
    historial_precio = obtener_historial_precio_moneda(symbol, API_KEY)
    if historial_precio is not None:
        return jsonify(historial_precio)
    else:
        return 'Error al consultar el historial de precio'



if __name__ == '__main__':
    app.run(debug=True)
