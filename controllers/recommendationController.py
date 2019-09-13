from flask import Blueprint, jsonify, abort, make_response, request
from flask_cors import CORS
from common.anime import Anime
from common.database import Database
from common.error import error

api = Blueprint('recommendationapi', __name__, url_prefix='/animewebapi')
cors = CORS(api, origins='https://www.cs.drexel.edu')
idEndpoint = 'recommendationapi.get_recommendation_byid'
database = Database()

# Get a list of recommended anime
@api.route('/recommendations', methods=['GET'])
def get_recommendation():
    params = {}
    
    title = request.args.get('title', default=None, type=str)
    userId = request.args.get('userId', default=None, type=int)

    if title:
        params.update({'title': title})
    if userId:
        params.update({'userId': userId})

    payload = []
    for a in database.get('anime', params=params):
        payload.append(a.toDict(idEndpoint))
    return jsonify({'anime': payload})

# Get a list of recommended anime
@api.route('/recommendations/<int:recommendationId>', methods=['GET'])
def get_recommendation_byid(recommendationId):
    payload = []
    for a in database.get('anime', {'id': recommendationId}):
        payload.append(a.toDict(idEndpoint))
    return jsonify({'anime': payload})

# Add a new recommendation
@api.route('/recommendations', methods=['POST'])
def create_recommendation():
    if not request.json or not 'title' in request.json or not 'userId' in request.json:
        e = error(400, 'Must include a title and a userId')
        return e.toResponse()
    anime = Anime(
        request.json['title'],
        request.json['japaneseTitles']['romaji'],
        request.json['japaneseTitles']['native'],
        request.json['description'],
        request.json['score'],
        request.json['links']['anilist'],
        request.json['links']['mal'],
        request.json['image'],
        request.json['userId']
    )
    code = database.insert(anime)
    if code == 201:
        return jsonify({'anime': anime.toDict(idEndpoint)}), 201
    else:
        e = error(code, 'The anime already exists')
        return e.toResponse()

# Delete a recommendation by title
@api.route('/recommendations', methods=['DELETE'])
def delete_recommendation(title):
    title = request.args.get('title', default=None, type=str)
    userId = request.args.get('userId', default=None, type=int)
    database.delete(title, userId)
    return jsonify({'Result': 'Deleted'})

########## Error Handling ##########
@api.errorhandler(404)
def notfound(self):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@api.errorhandler(400)
def badrequest(Self):
    return make_response(jsonify({'error': 'Bad Request'}), 400)