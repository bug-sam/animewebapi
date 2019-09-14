from flask import make_response, jsonify

class error:
    def __init__(self, statusCode, message):
        self.statusCode = statusCode
        self.message = message
    
    def toResponse(self):
        return make_response(
            jsonify({'error': self.message}),
            self.statusCode
        )
