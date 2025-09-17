# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.tire_controller import get_all_tires, create_tire, update_tire, delete_tire, swap_tires
from controllers.vehicle_controller import get_all_vehicles, create_vehicle, update_vehicle, delete_vehicle
from controllers.event_controller import get_all_events, create_event, delete_event
import os

def validate_client_id():
    """Valida e extrai o cliente_id da requisição"""
    cliente_id = request.args.get('cliente_id') or (request.json.get('cliente_id') if request.is_json else None)
    if not cliente_id:
        return None, jsonify({"message": "cliente_id é obrigatório"}), 400
    return cliente_id, None, None

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Tire Routes ---
@app.route('/api/tires', methods=['GET'])
def api_get_all_tires():
    """API endpoint to get all tires."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    return get_all_tires(cliente_id)

@app.route('/api/tires', methods=['POST'])
def api_create_tire():
    """API endpoint to create a new tire."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    data = request.json
    return create_tire(data, cliente_id)

@app.route('/api/tires/<string:tire_id>', methods=['PUT'])
def api_update_tire(tire_id):
    """API endpoint to update an existing tire."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    data = request.json
    return update_tire(tire_id, data, cliente_id)

@app.route('/api/tires/<string:tire_id>', methods=['DELETE'])
def api_delete_tire(tire_id):
    """API endpoint to delete a tire."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    return delete_tire(tire_id, cliente_id)

# --- Vehicle Routes ---
@app.route('/api/vehicles', methods=['GET'])
def api_get_all_vehicles():
    """API endpoint to get all vehicles."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    return get_all_vehicles(cliente_id)

@app.route('/api/vehicles', methods=['POST'])
def api_create_vehicle():
    """API endpoint to create a new vehicle."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    data = request.json
    return create_vehicle(data, cliente_id)

@app.route('/api/vehicles/<string:vehicle_id>', methods=['PUT'])
def api_update_vehicle(vehicle_id):
    """API endpoint to update an existing vehicle."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    data = request.json
    return update_vehicle(vehicle_id, data, cliente_id)

@app.route('/api/vehicles/<string:vehicle_id>', methods=['DELETE'])
def api_delete_vehicle(vehicle_id):
    """API endpoint to delete a vehicle."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    return delete_vehicle(vehicle_id, cliente_id)

# --- Event Routes ---
@app.route('/api/events', methods=['GET'])
def api_get_all_events():
    """API endpoint to get all events."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    return get_all_events(cliente_id)

@app.route('/api/events', methods=['POST'])
def api_create_event():
    """API endpoint to create a new event."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    data = request.json
    return create_event(data, cliente_id)

@app.route('/api/events/<string:event_id>', methods=['DELETE'])
def api_delete_event(event_id):
    """API endpoint to delete an event."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    return delete_event(event_id, cliente_id)

# --- Swap Tires Route ---
@app.route('/api/swap-tires', methods=['POST'])
def api_swap_tires():
    """API endpoint to swap two tires' positions."""
    cliente_id, error_response, status_code = validate_client_id()
    if error_response:
        return error_response, status_code
    data = request.json
    tire1_id = data.get('tire1Id')
    tire2_id = data.get('tire2Id')
    if not tire1_id or not tire2_id:
        return jsonify({"message": "IDs dos pneus são necessários para a permuta."}), 400
    return swap_tires(tire1_id, tire2_id, cliente_id)

if __name__ == '__main__':
    # For local development, use this:
    # app.run(debug=True, host='0.0.0.0', port=7766)
    # For production, Gunicorn or similar WSGI server will manage the app execution.
    # The `if __name__ == '__main__':` block is not executed when using gunicorn.
    # It's kept here for direct execution during development.
    app.run(debug=True, host='0.0.0.0', port=7766)
