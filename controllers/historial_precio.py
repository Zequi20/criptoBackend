import datetime
import requests

def obtener_historial_precio_moneda(symbol, key):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    # Calcular la fecha de inicio y fin para los últimos 10 días
    fecha_fin = datetime.datetime.now()
    parametros = {
        'fsym': symbol,                 
        'tsym': 'USD',                 
        'limit': 29,                   
        'toTs': int(fecha_fin.timestamp()),     
        'e': 'CCCAGG'                   
    }
    headers = {
        'Apikey': key
    }
    respuesta = requests.get(url, params=parametros, headers=headers)
    if respuesta.status_code == 200:
        data = respuesta.json()
        return data['Data']['Data']  # Devolver los datos de precio histórico
    else:
        return None