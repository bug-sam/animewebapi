from common.anime import Anime
import mysql.connector

class Database:
    def __init__(self):
        self.database = None
        self.cursor = None

    def connect(self, host, user, password, database):
        self.database = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        
        self.cursor = self.database.cursor()

    def get(self, table='anime', params=None):
        query = 'SELECT * FROM ' + table
        
        if params:
            i = 1
            last = len(params)
            for key, val in params.items():
                try:
                    val = int(val)
                    val = str(val)
                except ValueError:
                    val = "'" + val + "'"

                if i == 1:
                    query += ' WHERE '
                
                query += key + ' = ' + val

                if i != last:
                    query += ' AND '
                
                i += 1

        print(query)

        self.cursor.execute(query)
        results = self.cursor.fetchall()

        animes = []

        for anime in results:
            animes.append(Anime(
                anime[1], # title
                anime[2], # romaji
                anime[3], # native
                anime[4], # description
                anime[5], # score
                anime[6], # anilistLink
                anime[7], # malLink
                anime[8], # image
                anime[9], # userId
                anime[0]  # id
            ))
        
        return animes

    def insert(self, anime, table='anime'):
        exists = self.get(params={'title': anime.title, 'userId': anime.userId})
        if exists:
            return 400
        query = 'INSERT INTO ' + table + ' (title, romaji, native, description, score, anilistLink, malLink, image, userId) '
        query += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = (anime.title, anime.romaji, anime.native, anime.description, anime.score, anime.anilistLink, anime.malLink, anime.image, anime.userId)

        self.cursor.execute(query, values)
        self.database.commit()

        return 201

    def delete(self, title, userId, table='anime'):
        sql = 'DELETE FROM ' + table + ' WHERE title = %s AND userId = %s'

        self.cursor.execute(sql, (title, userId, ))
        self.database.commit()
