import requests
from flask import Blueprint, jsonify, abort, make_response, request
from flask_cors import CORS
from common.anime import Anime
from common.error import error

api = Blueprint('anilist', __name__, url_prefix='/anilist')
cors = CORS(api, origins='https://www.cs.drexel.edu')

session = requests.Session()
session.headers = {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/vnd.api+json'
}

req = requests.Session()

url = 'https://graphql.anilist.co'

search_query = '''query ($search: String) {
    Page {
        media(search: $search type: ANIME) {
            title {
                english
                romaji
            }
            startDate {
                year
            }
            id
        }
    }
}'''

anime_query = '''query ($id: Int) {
    Media(id: $id) {
        title {
            english
            romaji
            native
        }
        averageScore
        description
        id
        idMal
        coverImage {
            medium
        }
    }
}'''

@api.route('/search', methods=['GET'])
def search_animes_bytitle():
    title = request.args.get('title', default=None, type=str)

    if not title:
        e = error(400, "title url parameter is required")
        return e.toResponse()

    search_variables = {
        'search': title
    }
    payload = {
        'query': search_query,
        'variables': search_variables
    }

    response = req.post(url, json=payload).json()
    req.close()

    result = parseSearch(response)

    return jsonify({'anime': result})

@api.route('/anime', methods=['GET'])
def get_anime_byId():
    Id = request.args.get('id', default=None, type=int)

    if not Id:
        e = error(400, "id url parameter is required")
        return e.toResponse()
    
    search_variables = {'id': Id}
    payload = {
        'query': anime_query,
        'variables': search_variables
    }

    response = req.post(url, json=payload).json()
    req.close()

    anime = parse(response)

    return jsonify({'anime': anime.toDict()})

def parseSearch(rawResponse):
    data = rawResponse['data']['Page']['media']
    response = []
    i = 0

    for d in data:
        if i == 10:
            break

        title = d['title']['english']
        if not title:
            title = d['title']['romaji']

        response.append({
            'title': title,
            'year': d['startDate']['year'],
            'id': d['id']
        })
        
        i += 1

    return response

def parse(rawResponse):
    data = rawResponse['data']['Media']
    print(data)
    title = data['title']['english']

    japaneseTitles = [
        data['title']['romaji'],
        data['title']['native']
    ]

    links = [
        'https://anilist.co/anime/' + str(data['id']),
        'https://myanimelist.net/anime/' + str(data['idMal'])
    ]

    score = data['averageScore']

    description = data['description']

    image = data['coverImage']['medium']

    anime = Anime(title, japaneseTitles, description, score, links, image)

    return anime