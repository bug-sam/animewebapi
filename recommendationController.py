from flask import Blueprint, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from anime import Anime
import database as db

api = Blueprint('recommendationapi', __name__, url_prefix='/animewebapi/recommendations')
cors = CORS(api, origins='https://www.cs.drexel.edu')
auth = HTTPBasicAuth()
idEndpoint = 'recommendationapi.get_recommendation_byid'

@api.route('/', methods=['GET'])
def get_recommendation():
    payload = []
    for a in db.recommendations:
        payload.append(a.toDict(idEndpoint))
    return jsonify({'anime': payload})

@api.route('/<int:anime_id>', methods=['GET'])
def get_recommendation_byid(anime_id):
    payload = [anime for anime in db.recommendations if anime.id == anime_id]
    if payload:
        payload = payload[0].toDict(idEndpoint)
        return jsonify({'anime': payload})
    abort(404)

@api.route('/<string:title>', methods=['GET'])
def get_recommendation_bytitle(title):
    payload = [anime for anime in db.recommendations if anime.title.lower() == title.lower()]
    if payload:
        payload = payload[0].toDict(idEndpoint) 
        return jsonify({'anime': payload})
    abort(404)

@api.route('/', methods=['POST'])
#@auth.login_required
def create_recommendation():
    if not request.json or not 'title' in request.json:
        abort(400)
    anime = Anime(
        request.json['title'],
        request.json['japanese titles'],
        request.json['description'],
        request.json['score'],
        db.getNextId())
    if anime in db.recommendations:
        abort(400)
    db.insert(anime)
    return jsonify({'anime': anime.toDict(idEndpoint)}), 201

@api.route('/<string:title>', methods=['DELETE'])
def delete_recommendation(title):
    anime = [anime for anime in db.recommendations if anime.title.lower() == title.lower()]
    if not anime:
        abort(404)
    db.delete(anime[0])
    return jsonify({'Result': 'Deleted'})

########## Authentication ##########
@auth.get_password
def get_password(username):
    if username == 'username':
        return 'password'
    return None

########## Error Handling ##########
@api.errorhandler(404)
def notfound(self):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@api.errorhandler(400)
def badrequest(Self):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)