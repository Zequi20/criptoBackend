from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/top_monedas')
def mostrar_top_monedas():
    top_monedas = obtener_top_monedas()

    if top_monedas is not None:
        return jsonify(top_monedas)
    else:
        return 'Error al consultar los datos de CoinMarketCap'






API_KEY = 'e2d7b3c1-269d-4c70-8b67-dd3864708f02'

def obtener_top_monedas():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parametros = {
        'start': 1,
        'limit': 5,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY
    }
    respuesta = requests.get(url, params=parametros, headers=headers)

    if respuesta.status_code == 200:
        datos = respuesta.json()["data"]
        monedas = [filtrar_datos(elem) for elem in datos]
        return monedas
    else:
        return None

def filtrar_datos(elem):
    return {
        "name": elem["name"],
        "symbol": elem["symbol"],
        "price": elem["quote"]["USD"]["price"],
        "market_cap": elem["quote"]["USD"]["market_cap"],
        "market_cap_percentage": elem["quote"]["USD"]["percent_change_24h"],
        "volume": elem["quote"]["USD"]["volume_24h"],
        "volume_percentage": elem["quote"]["USD"]["volume_change_24h"]
    }


if __name__ == '__main__':
    app.run(debug=True)
