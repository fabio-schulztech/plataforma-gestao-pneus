# controllers/vehicle_controller.py
from db.connection import create_db_connection
from flask import jsonify
import mysql.connector

def get_all_vehicles(cliente_id):
    """Fetches all vehicles from the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles WHERE cliente_id = %s", (cliente_id,))
        vehicles = cursor.fetchall()
        return jsonify(vehicles), 200
    except Exception as e:
        print(f"Erro ao buscar veículos: {e}")
        return jsonify({"message": "Erro ao buscar veículos."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def create_vehicle(data, cliente_id):
    """Creates a new vehicle in the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO vehicles (id, placa, modelo, ano, eixos, cliente_id, createdAt, updatedAt)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        values = (
            data['id'], data['placa'], data['modelo'], data.get('ano'), data.get('eixos'), cliente_id
        )
        cursor.execute(sql, values)
        connection.commit()
        return jsonify({"message": "Veículo cadastrado com sucesso!", "id": data['id']}), 201
    except mysql.connector.Error as err:
        print(f"Erro MySQL ao cadastrar veículo: {err}")
        return jsonify({"message": f"Erro ao cadastrar veículo: {err.msg}"}), 500
    except Exception as e:
        print(f"Erro geral ao cadastrar veículo: {e}")
        return jsonify({"message": "Erro interno ao cadastrar veículo."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_vehicle(vehicle_id, data, cliente_id):
    """Updates an existing vehicle in the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor()
        set_clauses = []
        values = []
        for key, value in data.items():
            if key not in ['id', 'createdAt', 'cliente_id']: # Prevent updating immutable fields
                set_clauses.append(f"{key} = %s")
                values.append(value)
        set_clauses.append("updatedAt = NOW()")

        if not set_clauses:
            return jsonify({"message": "Nenhum dado para atualizar."}), 400

        sql = f"UPDATE vehicles SET {', '.join(set_clauses)} WHERE id = %s AND cliente_id = %s"
        values.extend([vehicle_id, cliente_id])

        cursor.execute(sql, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Veículo não encontrado ou não pertence ao cliente."}), 404
        return jsonify({"message": "Veículo atualizado com sucesso!"}), 200
    except mysql.connector.Error as err:
        print(f"Erro MySQL ao atualizar veículo: {err}")
        return jsonify({"message": f"Erro ao atualizar veículo: {err.msg}"}), 500
    except Exception as e:
        print(f"Erro geral ao atualizar veículo: {e}")
        return jsonify({"message": "Erro interno ao atualizar veículo."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_vehicle(vehicle_id, cliente_id):
    """Deletes a vehicle from the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id = %s AND cliente_id = %s", (vehicle_id, cliente_id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Veículo não encontrado ou não pertence ao cliente."}), 404
        return jsonify({"message": "Veículo excluído com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao excluir veículo: {e}")
        return jsonify({"message": "Erro ao excluir veículo."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
