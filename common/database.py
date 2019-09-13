from common.anime import Anime
import mysql.connector

class Database:
    def __init__(self):
        self.database = None
        self.cursor = None
        self.table = None

    def connect(self, host, user, password, database):
        self.database = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        
        self.cursor = self.database.cursor()

    def get(self, table, params):
        query = 'SELECT * FROM ' + table
        i = 1
        last = len(params)

        for key, val in params:
            if i == 1:
                query += ' WHERE '
            
            query += key + ' = ' + val

            if i != last:
                query += ' AND'

        self.cursor.execute(query)
        results = self.cursor.fetchall()

        for anime in results:
            self.db.append(Anime(
                anime[1],
                [anime[2], anime[3]],
                anime[5],
                anime[4],
                anime[0]
            ))

    def insert(self, anime):
        sql = 'INSERT INTO ' + self.table + ' (title, japaneseTitle, romajiTitle, score, description) VALUES (%s, %s, %s, %s, %s)'
        values = (anime.title, anime.japaneseTitles[0], anime.japaneseTitles[1], anime.score, anime.description)

        self.cursor.execute(sql, values)
        self.database.commit()

    def delete(self, anime):
        sql = 'DELETE FROM ' + self.table + ' WHERE title = %s'

        self.cursor.execute(sql, (anime.title, ))
        self.database.commit()
