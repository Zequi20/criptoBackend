from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import datetime
import mysql.connector

API_KEY = '3bb16e1c01fbcfe31c6a854789ca81e14fed82ab0b0a69afeeb0c9db849fb6b8'

app = Flask(__name__)
CORS(app)

# Configure MySQL connection
db_config = {
    'user': 'zequi',
    'password': 'Zequi!-2000',
    'host': 'localhost',
    'database': 'coin',
    'autocommit': True
}

conn = mysql.connector.connect(**db_config)

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
        'fsym': symbol,                 
        'tsym': 'USD',                 
        'limit': 30,                   
        'toTs': int(fecha_fin.timestamp()),     
        'e': 'CCCAGG'                   
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

@app.route('/login', methods=['POST'])
def verify_usuario():
    perfiles = get_perfiles()
    credenciales = request.get_json()
    for perfil in perfiles:
        if perfil == credenciales:
            return {"success": True}
    return {"success": False}

def get_perfiles():
    cur = conn.cursor()
    try:
        sql_query = 'SELECT nombre, clave FROM usuario'
        cur.execute(sql_query)
        columns = [column[0] for column in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"})
    finally:
        if cur:
            cur.close()

@app.route('/register', methods=['POST'])
def registrar():
    credenciales = request.get_json()
    registro = registrar_perfil(credenciales)
    print(registro)
    return registro

def registrar_perfil(credencial):
    if 'nombre' not in credencial or 'clave' not in credencial:
        return {"error": "Faltan credenciales"}

    # Verificar si el usuario ya existe
    if usuario_existe(credencial['nombre']):
        return {"error": "El usuario ya existe"}

    try:
        cur = conn.cursor()
        sql_query = "INSERT INTO usuario (nombre, clave) VALUES (%s, %s);"
        cur.execute(sql_query, (credencial['nombre'], credencial['clave']))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return {"error": str(e)}
    finally:
        if cur:
            cur.close()

    return {"success": True}

def usuario_existe(nombre_usuario):
    try:
        cur = conn.cursor()
        sql_query = "SELECT COUNT(*) FROM usuario WHERE nombre = %s"
        cur.execute(sql_query, (nombre_usuario,))
        count = cur.fetchone()[0]
        return count > 0
    except mysql.connector.Error as e:
        print(f"Error al verificar si el usuario existe: {e}")
        return False
    finally:
        if cur:
            cur.close()


if __name__ == '__main__':
    app.run(debug=True)
