import sys
sys.path.insert(0, '../')

import unittest
import json
import uuid
import controllers.recommendationController as rc
from controllers.recommendationController import database
from common.database import Database
from flask import Flask

class RecommendationTests(unittest.TestCase):
    testTable = None
    session = None
    client = None

    @classmethod
    def setUpClass(cls):
        app = Flask(__name__, static_url_path="")
        app.register_blueprint(rc.api)

        config = loadConfiguration("../configuration/configuration.json")
        database.connect(
            config["database host"], 
            config["username"], 
            config["password"],
            config["database"]
        )

        cursor = database.cursor
        db = database.database
        cls.testTable = uuid.uuid1().hex
        cursor.execute("CREATE TABLE " + cls.testTable + 
            " (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), japaneseTitle VARCHAR(255), romajiTitle VARCHAR(255), score VARCHAR(255), description TEXT)")
        
        sql = 'INSERT INTO ' + cls.testTable + ' (title, japaneseTitle, romajiTitle, score, description) VALUES (%s, %s, %s, %s, %s)'
        values1 = ("title1", "romaji1", "japanese1", "score1", "description1")
        values2 = ("title2", "romaji2", "japanese2", "score2", "description2")
        cursor.execute(sql, values1)
        cursor.execute(sql, values2)
        db.commit()
        database.read(cls.testTable)

        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        cursor = database.cursor
        sql = "DROP TABLE " + cls.testTable
        cursor.execute(sql)
    
    def test_get_recommendations_success(self):
        response = self.client.get('animewebapi/recommendations/')

        result = response.json['anime']

        self.assertEqual(result[0]['title'], 'title1')
        self.assertEqual(result[0]['japanese titles'], ['romaji1', 'japanese1'])
        self.assertEqual(result[0]['score'], 'score1')
        self.assertEqual(result[0]['description'], 'description1')

        self.assertEqual(result[1]['title'], 'title2')
        self.assertEqual(result[1]['japanese titles'], ['romaji2', 'japanese2'])
        self.assertEqual(result[1]['score'], 'score2')
        self.assertEqual(result[1]['description'], 'description2')

    def test_get_recommendation_byID_success(self):
        response = self.client.get('/animewebapi/recommendations/1')

        result = response.json['anime']

        self.assertEqual(result['title'], 'title1')
        self.assertEqual(result['japanese titles'], ['romaji1', 'japanese1'])
        self.assertEqual(result['score'], 'score1')
        self.assertEqual(result['description'], 'description1')

    def test_get_recommendation_byID_failure(self):
        response = self.client.get('/animewebapi/recommendations/3')

        self.assertEqual(response.status_code, 404)

    def test_get_recommendation_byTitle_success(self):
        response = self.client.get('/animewebapi/recommendations/title1')

        result = response.json['anime']

        self.assertEqual(result['title'], 'title1')
        self.assertEqual(result['japanese titles'], ['romaji1', 'japanese1'])
        self.assertEqual(result['score'], 'score1')
        self.assertEqual(result['description'], 'description1')

    def test_get_recommendation_byTitle_failure(self):
        response = self.client.get('/animewebapi/recommendations/bad_title')

        self.assertEqual(response.status_code, 404)


def loadConfiguration(filepath):
        f = open(filepath)
        parsed = json.loads(f.read())
        f.close()
        return parsed

if __name__ == '__main__':
    unittest.main()
        

