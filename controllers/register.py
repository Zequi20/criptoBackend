from conections.db_conector import conn, mysql

def registrar_usuario(credencial):
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