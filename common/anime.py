from flask import url_for
class Anime:
    def __init__(self, title, japaneseTitles, description, score, links, image, userId=None, i=None):
        self.title = title
        self.japaneseTitles = japaneseTitles
        self.description = description
        self.score = score
        self.links = links
        self.image = image
        self.userId = userId
        self.id = i

    def toDict(self, endpoint=''):
        dictionary = {
            'title': self.title,
            'japanese titles': self.japaneseTitles,
            'description': self.description,
            'score': self.score,
            'links': self.links
        }
        
        if self.userId:
            dictionary['userId'] = self.userId

        if self.id:
            dictionary['id'] = self.id
            
            if endpoint:
                dictionary['links'] = {
                    'self': url_for(endpoint, anime_id=self.id, _external=True)
                }
        
        return dictionary
    
    def __eq__(self, other):
        return self.title == other.title