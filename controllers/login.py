from flask import jsonify, request
from conections.db_conector import conn, mysql


def verify_usuario():
    credenciales = request.get_json()
    usuarios = get_usuarios()
    for usuario in usuarios:
        if usuario["nombre"] == credenciales["nombre"] and usuario["clave"] == credenciales["clave"]:
            return {"success": True,
                    "id": usuario['id']}
    return {"success": False}


def get_usuarios():
    cur = conn.cursor()
    try:
        sql_query = 'SELECT id, nombre, clave FROM usuario'
        cur.execute(sql_query)
        columns = [column[0] for column in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"})
    finally:
        if cur:
            cur.close()
