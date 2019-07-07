from flask import Blueprint, jsonify, abort, make_response, request
from flask_cors import CORS
from common.anime import Anime
import requests

api = Blueprint('kitsu', __name__, url_prefix='/kitsu')
cors = CORS(api, origins='https://www.cs.drexel.edu')

session = requests.Session()
session.headers = {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/vnd.api+json'
}


@api.route('/<string:title>', methods=['GET'])
def get_recomendation_bytitle(title):
    response = session.get('https://kitsu.io/api/edge/anime?filter[text]=' + title, timeout=4)
    response.raise_for_status()

    result = parse(response.json()['data'])

    if result:
        return jsonify({'anime': result.toDict()})
    abort(404)


def parse(response):
    anime = response[0]

    title_romaji = get_title_by_language_codes(
        anime['attributes']['titles'],
        ['en_jp']
    )
    title_english = get_title_by_language_codes(
        anime['attributes']['titles'],
        ['en', 'en_us']
    )
    title_japanese = get_title_by_language_codes(
        anime['attributes']['titles'],
        ['ja_jp']
    )

    rating = anime['attributes']['averageRating']

    description = anime['attributes']['synopsis']

    return Anime(
        title_english,
        [title_japanese, title_romaji],
        description,
        rating
    )


def get_title_by_language_codes(titles, codes):
    for language_code in codes:
        if language_code in titles:
            return titles[language_code]
    return None