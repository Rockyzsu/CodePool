from flask import jsonify
from exceptions import ValidationError
from api import api

def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
