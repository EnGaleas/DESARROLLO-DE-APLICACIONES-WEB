import os
import psycopg2
import psycopg2.extras


def obtener_conexion():
    try:
        database_url = os.environ.get("DATABASE_URL")
        if database_url:
            conexion = psycopg2.connect(database_url)
        else:
            conexion = psycopg2.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                user=os.environ.get("DB_USER", "postgres"),
                password=os.environ.get("DB_PASSWORD", ""),
                dbname=os.environ.get("DB_NAME", "maquillaje_db"),
                port=os.environ.get("DB_PORT", "5432"),
            )
        return conexion
    except psycopg2.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None