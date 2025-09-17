# controllers/event_controller.py
from db.connection import create_db_connection
from flask import jsonify
import mysql.connector
import json
from datetime import datetime

def get_all_events(cliente_id):
    """Fetches all tire events from the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tire_events WHERE cliente_id = %s", (cliente_id,))
        events = cursor.fetchall()
        # Ensure 'detalhes' field is parsed from JSON string if necessary
        for event in events:
            if isinstance(event.get('detalhes'), str):
                try:
                    event['detalhes'] = json.loads(event['detalhes'])
                except json.JSONDecodeError:
                    event['detalhes'] = {} # Handle invalid JSON
        return jsonify(events), 200
    except Exception as e:
        print(f"Erro ao buscar eventos: {e}")
        return jsonify({"message": "Erro ao buscar eventos."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def create_event(data, cliente_id):
    """Creates a new event and updates the associated tire for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        # Add cliente_id to the event data
        data['cliente_id'] = cliente_id
        create_event_internal(connection, data)
        connection.commit()
        return jsonify({"message": "Evento adicionado com sucesso!", "id": data['id']}), 201
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Erro MySQL ao cadastrar evento: {err}")
        return jsonify({"message": f"Erro ao cadastrar evento: {err.msg}"}), 500
    except Exception as e:
        connection.rollback()
        print(f"Erro geral ao cadastrar evento: {e}")
        return jsonify({"message": "Erro interno ao cadastrar evento."}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()

def create_event_internal(connection, data):
    """
    Internal function to create an event and update tire.
    Assumes an open connection is passed. Does not commit or close.
    """
    cursor = connection.cursor()
    
    # Insert the event
    sql_event = """
    INSERT INTO tire_events (id, tireId, tipo, data, observacoes, detalhes, cliente_id, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """
    event_details_json = json.dumps(data.get('detalhes', {}))
    event_values = (
        data['id'], data['tireId'], data['tipo'], data['data'],
        data.get('observacoes'), event_details_json, data.get('cliente_id')
    )
    cursor.execute(sql_event, event_values)

    # Update tire properties based on event type
    tire_id = data['tireId']
    tire_updates = {}

    # Fetch current tire data to calculate new values (e.g., total mileage)
    cursor.execute("SELECT * FROM tires WHERE id = %s AND cliente_id = %s", (tire_id, data.get('cliente_id')))
    current_tire = cursor.fetchone()
    if not current_tire:
        raise Exception(f"Pneu com ID {tire_id} não encontrado ou não pertence ao cliente.")

    if data['tipo'] == 'Retorno da Recapagem':
        tire_updates['numeroRecapagens'] = current_tire[14] + 1 # Assuming index 14 is numeroRecapagens
        tire_updates['statusInicial'] = 'Em Estoque - Recapado'
        tire_updates['profundidadeSulcoAtual'] = data['detalhes']['novaProfundidadeSulco']
    elif data['tipo'] == 'Descarte (Fim de Vida)':
        tire_updates['statusInicial'] = 'Descartado'
        tire_updates['currentVehicleId'] = None
        tire_updates['currentVehiclePlaca'] = None
        tire_updates['currentAxle'] = None
        tire_updates['currentPosition'] = None
    elif data['tipo'] == 'Envio para Recapagem':
        tire_updates['statusInicial'] = 'Em Recapagem'
        tire_updates['currentVehicleId'] = None
        tire_updates['currentVehiclePlaca'] = None
        tire_updates['currentAxle'] = None
        tire_updates['currentPosition'] = None
    elif data['tipo'] in ['Montagem em Veículo', 'Rodízio/Permutação']:
        tire_updates['statusInicial'] = 'Em Uso'
        tire_updates['currentVehicleId'] = data['detalhes']['veiculoId']
        tire_updates['currentVehiclePlaca'] = data['detalhes']['veiculoPlaca']
        tire_updates['currentAxle'] = data['detalhes']['eixo']
        tire_updates['currentPosition'] = data['detalhes']['posicao']
    elif data['tipo'] == 'Remoção de Veículo':
        tire_updates['statusInicial'] = 'Em Estoque - Usado'
        tire_updates['currentVehicleId'] = None
        tire_updates['currentVehiclePlaca'] = None
        tire_updates['currentAxle'] = None
        tire_updates['currentPosition'] = None
    elif data['tipo'] == 'Registro de Quilometragem e Sulco':
        nova_leitura_hodometro = float(data['detalhes']['quilometragemVeiculo'])
        ultima_leitura = float(current_tire[16] or 0) # Assuming index 16 is ultimaLeituraHodometroRegistrada

        if nova_leitura_hodometro > ultima_leitura:
            km_rodados = nova_leitura_hodometro - ultima_leitura
            tire_updates['quilometragemTotalPercorrida'] = float(current_tire[15] or 0) + km_rodados # Assuming index 15 is quilometragemTotalPercorrida
            tire_updates['ultimaLeituraHodometroRegistrada'] = nova_leitura_hodometro
        elif ultima_leitura == 0 and nova_leitura_hodometro > 0:
            tire_updates['quilometragemTotalPercorrida'] = 0 # Reset for this tire's accumulated mileage
            tire_updates['ultimaLeituraHodometroRegistrada'] = nova_leitura_hodometro

        tire_updates['profundidadeSulcoAtual'] = data['detalhes']['profundidadeSulcoAtual']

    if tire_updates:
        set_clauses = []
        values = []
        for key, value in tire_updates.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        set_clauses.append("updatedAt = NOW()")
        
        sql_tire_update = f"UPDATE tires SET {', '.join(set_clauses)} WHERE id = %s"
        values.append(tire_id)
        cursor.execute(sql_tire_update, values)
    
    cursor.close()


def delete_event(event_id, cliente_id):
    """Deletes an event from the database for a specific client."""
    connection = create_db_connection()
    if connection is None:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tire_events WHERE id = %s AND cliente_id = %s", (event_id, cliente_id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Evento não encontrado ou não pertence ao cliente."}), 404
        return jsonify({"message": "Evento excluído com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao excluir evento: {e}")
        return jsonify({"message": "Erro ao excluir evento."}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
