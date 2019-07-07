from flask import Blueprint, jsonify, abort, make_response, request
from flask_cors import CORS
from common.anime import Anime
from common.database import Database

api = Blueprint('recommendationapi', __name__, url_prefix='/animewebapi/recommendations')
cors = CORS(api, origins='https://www.cs.drexel.edu')
idEndpoint = 'recommendationapi.get_recommendation_byid'
database = Database()

# Get a list of recommended anime
@api.route('/', methods=['GET'])
def get_recommendation():
    payload = []
    for a in database.db:
        payload.append(a.toDict(idEndpoint))
    return jsonify({'anime': payload})

# Get a recommended anime by ID
@api.route('/<int:anime_id>', methods=['GET'])
def get_recommendation_byid(anime_id):
    payload = [anime for anime in database.db if anime.id == anime_id]
    if payload:
        payload = payload[0].toDict(idEndpoint)
        return jsonify({'anime': payload})
    abort(404)

# Get a recommended anime by title
@api.route('/<string:title>', methods=['GET'])
def get_recommendation_bytitle(title):
    payload = [anime for anime in database.db if anime.title.lower() == title.lower()]
    if payload:
        payload = payload[0].toDict(idEndpoint) 
        return jsonify({'anime': payload})
    abort(404)

# Add a new recommendation
@api.route('/', methods=['POST'])
def create_recommendation():
    if not request.json or not 'title' in request.json:
        abort(400)
    anime = Anime(
        request.json['title'],
        request.json['japanese titles'],
        request.json['description'],
        request.json['score'],
        database.getNextId())
    if anime in database.db:
        abort(400)
    database.insert(anime)
    return jsonify({'anime': anime.toDict(idEndpoint)}), 201

# Delete a recommendation by title
@api.route('/<string:title>', methods=['DELETE'])
def delete_recommendation(title):
    anime = [anime for anime in database.db if anime.title.lower() == title.lower()]
    if not anime:
        abort(404)
    database.delete(anime[0])
    return jsonify({'Result': 'Deleted'})

########## Authentication ##########
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