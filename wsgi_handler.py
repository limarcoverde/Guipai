from flask import Flask, jsonify, request, make_response
from authentication.auth import *
from service.guipaiService import *

app = Flask(__name__)

@app.route('/prova/correcao', methods=['POST'])
def provaGuipaicorrecao():
    if not authenticate():
        return jsonify({"Error": "Unauthorized"}), 401
    
    data = request.get_json()

    statuscode, response = callingGuipAICorrecao(data)
    
    return jsonify(response), statuscode

@app.route('/prova/recorrecao', methods=['POST'])
def provaGuipairecorrecao():
    if not authenticate():
        return jsonify({"Error": "Unauthorized"}), 401
    
    data = request.get_json()

    statuscode, response = callingGuipAIRecorrecao(data)
    
    return jsonify(response), statuscode

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Route not found!"), 404)

def handler(event, context):
    return awsgi.response(app, event, context)
