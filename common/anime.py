from flask import url_for
class Anime:
    def __init__(self, title, romaji, native, description, score, anilistLink, malLink, image, userId=None, i=None):
        self.title = title
        self.romaji = romaji
        self.native = native
        self.description = description
        self.score = score
        self.anilistLink = anilistLink
        self.malLink = malLink
        self.image = image
        self.userId = userId
        self.id = i

    def toDict(self, endpoint=''):
        dictionary = {
            'title': self.title,
            'japaneseTitles': {
                'romaji': self.romaji,
                'native': self.native
            },
            'description': self.description,
            'score': self.score,
            'links': {
                'anilist': self.anilistLink,
                'mal': self.malLink
            },
            'image': self.image
        }
        
        if self.userId:
            dictionary['userId'] = self.userId

        if self.id:
            dictionary['id'] = self.id
            
            if endpoint:
                dictionary['links'].update({
                    'self': url_for(endpoint, recommendationId=self.id, _external=True)
                })
        
        return dictionary
    
    def __eq__(self, other):
        return self.title == other.title