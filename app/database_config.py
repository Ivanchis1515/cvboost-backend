#configuracion de la base de datos
import mysql.connector #conector de la base de datos

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "cvboost_db"
}

def get_database_connection():
    #establece la conexion
    return mysql.connector.connect(
        host=DATABASE_CONFIG["host"], #host
        user=DATABASE_CONFIG["user"], #user
        password=DATABASE_CONFIG["password"], #pass
        database=DATABASE_CONFIG["database"] #database
    )