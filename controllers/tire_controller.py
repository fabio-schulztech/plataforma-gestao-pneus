# controllers/tire_controller.py
from db.connection import create_db_connection
from flask import jsonify
import mysql.connector
import json

def get_all_tires(cliente_id):
    """Fetches all tires from the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tires WHERE cliente_id = %s", (cliente_id,))
        tires = cursor.fetchall()
        return jsonify(tires), 200
    except Exception as e:
        print(f"Erro ao buscar pneus: {e}")
        return jsonify({"message": "Erro ao buscar pneus."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def create_tire(data, cliente_id):
    """Creates a new tire in the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO tires (id, numeroFogo, marca, modelo, tipoPneu, medida, capacidadeCarga,
                           desenhoBanda, profundidadeSulcoInicial, custoAquisicao, dataAquisicao,
                           fornecedor, numeroNF, statusInicial, numeroRecapagens,
                           quilometragemTotalPercorrida, ultimaLeituraHodometroRegistrada,
                           profundidadeSulcoAtual, cliente_id, createdAt, updatedAt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        values = (
            data['id'], data['numeroFogo'], data['marca'], data['modelo'], data.get('tipoPneu'),
            data['medida'], data.get('capacidadeCarga'), data.get('desenhoBanda'),
            data.get('profundidadeSulcoInicial'), data['custoAquisicao'], data['dataAquisicao'],
            data['fornecedor'], data.get('numeroNF'), data['statusInicial'],
            data.get('numeroRecapagens', 0),
            data.get('quilometragemTotalPercorrida', 0),
            data.get('ultimaLeituraHodometroRegistrada', 0),
            data.get('profundidadeSulcoAtual', data.get('profundidadeSulcoInicial')),
            cliente_id
        )
        cursor.execute(sql, values)
        connection.commit()
        return jsonify({"message": "Pneu cadastrado com sucesso!", "id": data['id']}), 201
    except mysql.connector.Error as err:
        print(f"Erro MySQL ao cadastrar pneu: {err}")
        return jsonify({"message": f"Erro ao cadastrar pneu: {err.msg}"}), 500
    except Exception as e:
        print(f"Erro geral ao cadastrar pneu: {e}")
        return jsonify({"message": "Erro interno ao cadastrar pneu."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_tire(tire_id, data, cliente_id):
    """Updates an existing tire in the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor()
        # Build the SET part of the SQL query dynamically
        set_clauses = []
        values = []
        for key, value in data.items():
            if key not in ['id', 'numeroFogo', 'createdAt', 'cliente_id']: # Prevent updating immutable fields
                set_clauses.append(f"{key} = %s")
                values.append(value)
        set_clauses.append("updatedAt = NOW()")
        
        if not set_clauses:
            return jsonify({"message": "Nenhum dado para atualizar."}), 400

        sql = f"UPDATE tires SET {', '.join(set_clauses)} WHERE id = %s AND cliente_id = %s"
        values.extend([tire_id, cliente_id])

        cursor.execute(sql, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Pneu não encontrado ou não pertence ao cliente."}), 404
        return jsonify({"message": "Pneu atualizado com sucesso!"}), 200
    except mysql.connector.Error as err:
        print(f"Erro MySQL ao atualizar pneu: {err}")
        return jsonify({"message": f"Erro ao atualizar pneu: {err.msg}"}), 500
    except Exception as e:
        print(f"Erro geral ao atualizar pneu: {e}")
        return jsonify({"message": "Erro interno ao atualizar pneu."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_tire(tire_id, cliente_id):
    """Deletes a tire from the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tires WHERE id = %s AND cliente_id = %s", (tire_id, cliente_id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Pneu não encontrado ou não pertence ao cliente."}), 404
        return jsonify({"message": "Pneu excluído com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao excluir pneu: {e}")
        return jsonify({"message": "Erro ao excluir pneu."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def swap_tires(tire1_id, tire2_id, cliente_id):
    """Swaps the positions of two tires for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get current data for both tires (only from the same client)
        cursor.execute("SELECT id, numeroFogo, currentVehicleId, currentVehiclePlaca, currentAxle, currentPosition, statusInicial FROM tires WHERE id IN (%s, %s) AND cliente_id = %s", (tire1_id, tire2_id, cliente_id))
        tires_data = {t['id']: t for t in cursor.fetchall()}

        tire1 = tires_data.get(tire1_id)
        tire2 = tires_data.get(tire2_id)

        if not tire1 or not tire2:
            return jsonify({"message": "Um ou ambos os pneus não foram encontrados ou não pertencem ao cliente."}), 404
        
        if tire1['statusInicial'] != 'Em Uso' or tire2['statusInicial'] != 'Em Uso':
            return jsonify({"message": "Ambos os pneus devem estar 'Em Uso' para realizar a permuta."}), 400

        # Store original positions
        original_tire1_location = {
            "vehicleId": tire1['currentVehicleId'],
            "vehiclePlaca": tire1['currentVehiclePlaca'],
            "axle": tire1['currentAxle'],
            "position": tire1['currentPosition'],
        }
        original_tire2_location = {
            "vehicleId": tire2['currentVehicleId'],
            "vehiclePlaca": tire2['currentVehiclePlaca'],
            "axle": tire2['currentAxle'],
            "position": tire2['currentPosition'],
        }

        # Update tire1 with tire2's original location
        cursor.execute("""
            UPDATE tires SET
                currentVehicleId = %s,
                currentVehiclePlaca = %s,
                currentAxle = %s,
                currentPosition = %s,
                updatedAt = NOW()
            WHERE id = %s
        """, (original_tire2_location['vehicleId'], original_tire2_location['vehiclePlaca'],
              original_tire2_location['axle'], original_tire2_location['position'], tire1_id))

        # Update tire2 with tire1's original location
        cursor.execute("""
            UPDATE tires SET
                currentVehicleId = %s,
                currentVehiclePlaca = %s,
                currentAxle = %s,
                currentPosition = %s,
                updatedAt = NOW()
            WHERE id = %s
        """, (original_tire1_location['vehicleId'], original_tire1_location['vehiclePlaca'],
              original_tire1_location['axle'], original_tire1_location['position'], tire2_id))

        # Add swap events for both tires
        from controllers.event_controller import create_event_internal # Import here to avoid circular dependency

        # Event for tire1
        event1_data = {
            "id": generate_unique_id(),
            "tireId": tire1_id,
            "tipo": "Rodízio/Permutação (Swap)",
            "data": datetime.now().strftime("%Y-%m-%d"),
            "observacoes": f"Permutado com o pneu {tire2['numeroFogo']}. Nova posição: {original_tire2_location['vehiclePlaca']} - {original_tire2_location['axle']} {original_tire2_location['position']}.",
            "detalhes": {
                "veiculoId": original_tire2_location['vehicleId'],
                "veiculoPlaca": original_tire2_location['vehiclePlaca'],
                "eixo": original_tire2_location['axle'],
                "posicao": original_tire2_location['position'],
                "pneuPermutadoId": tire2_id,
                "pneuPermutadoNumeroFogo": tire2['numeroFogo'],
            },
            "cliente_id": cliente_id
        }
        create_event_internal(connection, event1_data)

        # Event for tire2
        event2_data = {
            "id": generate_unique_id(),
            "tireId": tire2_id,
            "tipo": "Rodízio/Permutação (Swap)",
            "data": datetime.now().strftime("%Y-%m-%d"),
            "observacoes": f"Permutado com o pneu {tire1['numeroFogo']}. Nova posição: {original_tire1_location['vehiclePlaca']} - {original_tire1_location['axle']} {original_tire1_location['position']}.",
            "detalhes": {
                "veiculoId": original_tire1_location['vehicleId'],
                "veiculoPlaca": original_tire1_location['vehiclePlaca'],
                "eixo": original_tire1_location['axle'],
                "posicao": original_tire1_location['position'],
                "pneuPermutadoId": tire1_id,
                "pneuPermutadoNumeroFogo": tire1['numeroFogo'],
            },
            "cliente_id": cliente_id
        }
        create_event_internal(connection, event2_data)

        connection.commit()
        return jsonify({"message": "Permuta de pneus realizada com sucesso!"}), 200
    except Exception as e:
        connection.rollback() # Rollback on error
        print(f"Erro ao permutar pneus: {e}")
        return jsonify({"message": f"Erro ao permutar pneus: {e}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Helper to generate unique IDs (same logic as frontend)
def generate_unique_id():
    import time
    import random
    return str(int(time.time() * 1000)) + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))

from datetime import datetime # Import datetime for timestamping events
