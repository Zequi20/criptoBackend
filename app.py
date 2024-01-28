from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.alertas import registrar_seguimiento, get_alertas, eliminar_seguimiento
from controllers.historial_precio import obtener_historial_precio_moneda
from controllers.top_monedas import obtener_top_monedas
from controllers.register import registrar_usuario
from controllers.login import verify_usuario

app = Flask(__name__)
CORS(app)

API_KEY = '3bb16e1c01fbcfe31c6a854789ca81e14fed82ab0b0a69afeeb0c9db849fb6b8'

@app.route('/del_alerta', methods=['POST'])
def del_alerta():
    alert_data = request.get_json()
    return eliminar_seguimiento(alert_data)

@app.route('/add_alerta', methods=['POST'])
def add_alerta():
    alert_data = request.get_json()
    return registrar_seguimiento(alert_data)

@app.route('/alertas')
def alertas():
    return get_alertas()

@app.route('/login', methods=['POST'])
def login():
    return verify_usuario()

@app.route('/register', methods=['POST'])
def registrar():
    credenciales = request.get_json()
    registro = registrar_usuario(credenciales)
    return registro

@app.route('/top_monedas')
def mostrar_top_monedas():
    top_monedas = obtener_top_monedas(API_KEY)
    if top_monedas is not None:
        return jsonify(top_monedas)
    else:
        return 'Error al consultar los datos de CryptoCompare'

@app.route('/historial_precio/<coin_symbol>')
def historial_precio(coin_symbol):
    historial_precio_moneda = obtener_historial_precio_moneda(coin_symbol, API_KEY)
    if historial_precio_moneda is not None:
        return jsonify(historial_precio_moneda)
    else:
        return 'Error al consultar el historial de precio'


if __name__ == '__main__':
    app.run(debug=True)
