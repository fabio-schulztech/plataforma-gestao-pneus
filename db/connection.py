# db/connection.py
import mysql.connector
from mysql.connector import Error

def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="34.68.169.112",      # Ou o IP/hostname do seu servidor MySQL
            user="root",
            passwd="adminpass!!",
            database="tire_management_db"
        )
        print("Conexão com o banco de dados MySQL bem-sucedida")
    except Error as err:
        print(f"Erro: '{err}'")
    return connection

# Exemplo de uso (não necessário para a aplicação, mas útil para testar a conexão)
if __name__ == "__main__":
    conn = create_db_connection()
    if conn:
        conn.close()