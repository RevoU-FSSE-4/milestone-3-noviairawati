from flask import jsonify

def handle_error(error):
    response = jsonify({'message': str(error)})
    response.status_code = 500
    return response
