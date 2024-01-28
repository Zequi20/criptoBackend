import requests

def obtener_top_monedas(key):
    url = 'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=5&tsym=USD'
    headers = {
        'Apikey': key
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