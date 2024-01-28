from flask import jsonify
from conections.db_conector import conn, mysql

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