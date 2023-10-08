# 'e2d7b3c1-269d-4c70-8b67-dd3864708f02'
from flask import Flask, render_template
import requests

app = Flask(__name__)

# Configura tu API Key de CoinMarketCap
API_KEY = 'e2d7b3c1-269d-4c70-8b67-dd3864708f02'

@app.route('/latest')
def top_coins():
    # Consulta las 5 criptomonedas con mayor market cap
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start': 1,
        'limit': 5,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        return data['data']
    else:
        return 'Error al consultar los datos de CoinMarketCap'

if __name__ == '__main__':
    app.run(debug=True)
