from flask import Flask, jsonify
import requests
import datetime

API_KEY = '3bb16e1c01fbcfe31c6a854789ca81e14fed82ab0b0a69afeeb0c9db849fb6b8'
app = Flask(__name__)

@app.route('/top_monedas')
def mostrar_top_monedas():
    top_monedas = obtener_top_monedas()

    if top_monedas is not None:
        return jsonify(top_monedas)
    else:
        return 'Error al consultar los datos de CryptoCompare'

def obtener_top_monedas():
    url = 'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=5&tsym=USD'
    
    headers = {
        'Apikey': API_KEY
    }
    respuesta = requests.get(url, headers=headers)
    
    if respuesta.status_code == 200:
        respuesta_json = respuesta.json()
        respuesta_filtrada = map(filtrar_datos, respuesta_json["Data"])
        return list(respuesta_filtrada)  # Convierte el resultado de map en una lista
    else:
        return None

def filtrar_datos(elem):
    
    return {
        "name": elem["CoinInfo"]["FullName"],
        "symbol": elem["CoinInfo"]["Internal"],
        "price": elem["RAW"]["USD"]["PRICE"],
        "market_cap": elem["RAW"]["USD"]["MKTCAP"],
        "volume": elem["RAW"]["USD"]["VOLUME24HOUR"],
    }


@app.route('/historial_precio/<symbol>')
def obtener_historial_precio(symbol):
    historial_precio = obtener_historial_precio_moneda(symbol)

    if historial_precio is not None:
        return jsonify(historial_precio)
    else:
        return 'Error al consultar el historial de precio'

def obtener_historial_precio_moneda(symbol):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    
    # Calcular la fecha de inicio y fin para los últimos 30 días
    fecha_fin = datetime.datetime.now()
    
    
    parametros = {
        'fsym': symbol,                 # Símbolo de la criptomoneda
        'tsym': 'USD',                  # Moneda de cotización (USD)
        'limit': 30,                    # Número de puntos de datos históricos (últimos 30 días)
        'toTs': int(fecha_fin.timestamp()),     # Fecha de finalización en formato Unix timestamp
        'e': 'CCCAGG'                   # Intercambio de referencia (CryptoCompare Aggregate)
    }
    
    headers = {
        'Apikey': API_KEY
    }
    
    respuesta = requests.get(url, params=parametros, headers=headers)
    
    if respuesta.status_code == 200:
        data = respuesta.json()
        return data['Data']['Data']  # Devolver los datos de precio histórico
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
