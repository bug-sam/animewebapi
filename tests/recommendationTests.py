import sys
sys.path.insert(0, '../')

import unittest
import json
import uuid
import controllers.recommendationController as rc
import configuration.configuration as configuration
from controllers.recommendationController import database
from common.anime import Anime
from flask import Flask

class RecommendationTests(unittest.TestCase):
    testTable = None
    cursor = None
    client = None
    db = None

    @classmethod
    def setUpClass(cls):
        app = Flask(__name__, static_url_path='')
        app.register_blueprint(rc.api)

        cls.testTable = uuid.uuid1().hex

        config = configuration.loadConfiguration()
        database.connect(
            config['database host'], 
            config['username'], 
            config['password'],
            config['database'],
            cls.testTable
        )
        
        cls.cursor = database.cursor
        cls.db = database.database
        cls.cursor.execute('CREATE TABLE ' + cls.testTable + ' (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(40), romaji VARCHAR(40), native VARCHAR(40), description TEXT, score float, anilistLink VARCHAR(40), malLink VARCHAR(40), image VARCHAR(40), userId int)')
        
        query = 'INSERT INTO ' + cls.testTable + ' (title, romaji, native, description, score, anilistLink, malLink, image, userId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values1 = ('title1', 'romaji1', 'native1', 'description1', 1.0, 'anilist1', 'mal1', 'image1', 1)
        values2 = ('title2', 'romaji2', 'native2', 'description2', 2.0, 'anilist2', 'mal2', 'image2', 2)
        cls.cursor.execute(query, values1)
        cls.cursor.execute(query, values2)
        cls.db.commit()

        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        sql = 'DROP TABLE ' + cls.testTable
        cls.cursor.execute(sql)
    
    def test_get_recommendations_success(self):
        response = self.client.get('animewebapi/recommendations')

        result = response.json['anime']

        self.assertEqual(result[0]['title'], 'title1')
        self.assertEqual(result[0]['japaneseTitles'], {'romaji': 'romaji1', 'native': 'native1'})
        self.assertEqual(result[0]['description'], 'description1')
        self.assertEqual(result[0]['score'], 1.0)
        self.assertEqual(result[0]['links']['anilist'], 'anilist1')
        self.assertEqual(result[0]['links']['mal'], 'mal1')
        self.assertEqual(result[0]['image'], 'image1')
        self.assertEqual(result[0]['userId'], 1)

        self.assertEqual(result[1]['title'], 'title2')
        self.assertEqual(result[1]['japaneseTitles'], {'romaji': 'romaji2', 'native': 'native2'})
        self.assertEqual(result[1]['description'], 'description2')
        self.assertEqual(result[1]['score'], 2.0)
        self.assertEqual(result[1]['links']['anilist'], 'anilist2')
        self.assertEqual(result[1]['links']['mal'], 'mal2')
        self.assertEqual(result[1]['image'], 'image2')
        self.assertEqual(result[1]['userId'], 2)

    def test_get_recommendation_byID_success(self):
        response = self.client.get('/animewebapi/recommendations/1')

        result = response.json['anime'][0]

        self.assertEqual(result['title'], 'title1')
        self.assertEqual(result['japaneseTitles'], {'romaji': 'romaji1', 'native': 'native1'})
        self.assertEqual(result['description'], 'description1')
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(result['links']['anilist'], 'anilist1')
        self.assertEqual(result['links']['mal'], 'mal1')
        self.assertEqual(result['image'], 'image1')
        self.assertEqual(result['userId'], 1)

    def test_get_recommendation_byID_failure(self):
        response = self.client.get('/animewebapi/recommendations/69')

        self.assertEqual(response.status_code, 404)

    def test_get_recommendation_byTitle_success(self):
        response = self.client.get('/animewebapi/recommendations?title=title1')

        result = response.json['anime'][0]

        self.assertEqual(result['title'], 'title1')
        self.assertEqual(result['japaneseTitles'], {'romaji': 'romaji1', 'native': 'native1'})
        self.assertEqual(result['description'], 'description1')
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(result['links']['anilist'], 'anilist1')
        self.assertEqual(result['links']['mal'], 'mal1')
        self.assertEqual(result['image'], 'image1')
        self.assertEqual(result['userId'], 1)

    def test_get_recommendation_byUserId_success(self):
        response = self.client.get('/animewebapi/recommendations?userId=1')

        result = response.json['anime'][0]

        self.assertEqual(result['title'], 'title1')
        self.assertEqual(result['japaneseTitles'], {'romaji': 'romaji1', 'native': 'native1'})
        self.assertEqual(result['description'], 'description1')
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(result['links']['anilist'], 'anilist1')
        self.assertEqual(result['links']['mal'], 'mal1')
        self.assertEqual(result['image'], 'image1')
        self.assertEqual(result['userId'], 1)

    def test_get_recommendation_byTitle_failure(self):
        response = self.client.get('/animewebapi/recommendations?title=bad_title')

        self.assertEqual(response.status_code, 404)

    def test_post_recommendation_success(self):
        expected = Anime(
            'title3', 
            'romaji3',
            'native3',
            'description3',
            3.0,
            'anilist3',
            'mal3',
            'image3',
            3
        )

        response = self.client.post(
            '/animewebapi/recommendations',
            json=expected.toDict()
        )
        
        self.cursor.execute('SELECT * FROM ' + self.testTable + ' WHERE title = "title3"')
        result = self.cursor.fetchall()[0]

        actual = Anime(
            result[1], # title
            result[2], # romaji
            result[3], # native
            result[4], # description
            result[5], # score
            result[6], # anilistLink
            result[7], # malLink
            result[8], # image
            result[9], # userId
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(actual.toDict(), expected.toDict())

    def test_delete_recommendation_sucess(self):
        query = 'INSERT INTO ' + self.testTable + ' (title, romaji, native, description, score, anilistLink, malLink, image, userId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = ('title4', 'romaji4', 'native4', 'description4', 4.0, 'anilist4', 'mal4', 'image4', 4)
        self.cursor.execute(query, values)
        self.db.commit()

        response = self.client.delete('animewebapi/recommendations?title=title4&userId=4')

        self.assertEqual(response.status_code, 200)
        with self.assertRaises(IndexError):
            self.cursor.execute('SELECT * FROM ' + self.testTable + ' WHERE title = "title4"')
            self.cursor.fetchall()[0]


if __name__ == '__main__':
    unittest.main()