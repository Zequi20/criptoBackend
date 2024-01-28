from flask import jsonify
from conections.db_conector import conn, mysql

def get_alertas():
    cur = conn.cursor()
    try:
        sql_query = 'SELECT * FROM seguimiento'
        cur.execute(sql_query)
        columns = [column[0] for column in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"})
    finally:
        if cur:
            cur.close()

def registrar_seguimiento(seguimiento):
    if 'moneda' not in seguimiento:
        return {"error": "Faltan credenciales"}
    try:
        cur = conn.cursor()
        sql_query = "INSERT INTO seguimiento (moneda, usuario, monto, fecha_hora) VALUES (%s, %s, %s, %s);"
        cur.execute(sql_query, (seguimiento['moneda'], seguimiento['usuario'], seguimiento['monto'], seguimiento['fecha_hora']))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return {"error": str(e)}
    finally:
        if cur:
            cur.close()

    return {"success": True}

def eliminar_seguimiento(seguimiento):
    if 'id' not in seguimiento:
        return {"error": "Faltan credenciales"}
    try:
        cur = conn.cursor()
        sql_query = "DELETE FROM seguimiento WHERE id = %s;"
        cur.execute(sql_query, (seguimiento['id'],))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return {"error": str(e)}
    finally:
        if cur:
            cur.close()
    return {"success": True}
