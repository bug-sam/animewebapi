from anime import Anime
import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="state",
    passwd="senorST15",
    database="AnimeTestDB"
)

cursor = database.cursor()

recommendations = []

def read():
    cursor.execute('SELECT * FROM anime')
    results = cursor.fetchall()

    for anime in results:
        recommendations.append(Anime(
            anime[1],
            [anime[2], anime[3]],
            anime[5],
            anime[4],
            getNextId()
        ))

def insert(anime):
    sql = 'INSERT INTO anime (title, japaneseTitle, romajiTitle, score, description) VALUES (%s, %s, %s, %s, %s)'
    values = (anime.title, anime.japaneseTitles[0], anime.japaneseTitles[1], anime.score, anime.description)

    recommendations.append(anime)

    cursor.execute(sql, values)
    database.commit()

def delete(anime):
    sql = 'DELETE FROM anime WHERE title = %s'
    
    recommendations.remove(anime)

    cursor.execute(sql, (anime.title, ))
    database.commit()

def getNextId():
    if recommendations:
        return recommendations[-1].id + 1
    return 1