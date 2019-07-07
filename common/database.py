from common.anime import Anime
import mysql.connector

class Database:
    def __init__(self):
        self.database = None
        self.cursor = None
        self.table = None
        self.db = []

    def connect(self, host, user, password, database):
        self.database = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        
        self.cursor = self.database.cursor()

    def read(self, table):
        self.table = table
        self.db = []
        self.cursor.execute('SELECT * FROM ' + table)
        results = self.cursor.fetchall()

        for anime in results:
            self.db.append(Anime(
                anime[1],
                [anime[2], anime[3]],
                anime[5],
                anime[4],
                self.getNextId()
            ))

    def insert(self, anime):
        sql = 'INSERT INTO ' + self.table + ' (title, japaneseTitle, romajiTitle, score, description) VALUES (%s, %s, %s, %s, %s)'
        values = (anime.title, anime.japaneseTitles[0], anime.japaneseTitles[1], anime.score, anime.description)

        self.db.append(anime)

        self.cursor.execute(sql, values)
        self.database.commit()

    def delete(self, anime):
        sql = 'DELETE FROM ' + self.table + ' WHERE title = %s'
        
        self.db.remove(anime)

        self.cursor.execute(sql, (anime.title, ))
        self.database.commit()

    def getNextId(self):
        if self.db:
            return self.db[-1].id + 1
        return 1
