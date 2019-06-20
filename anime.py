from flask import url_for
class Anime:
    def __init__(self, t, jt, d, s, i=None):
        self.title = t
        self.japaneseTitles = jt
        self.description = d
        self.score = s
        self.id = i

    def toDict(self, endpoint=''):
        dictionary = {
            'title': self.title,
            'japanese titles': self.japaneseTitles,
            'description': self.description,
            'score': self.score,
        }
        
        if self.id:
            dictionary['id'] = self.id
            
            if endpoint:
                dictionary['links'] = {
                    'self': url_for(endpoint, anime_id=self.id, _external=True)
                }
        
        return dictionary
    
    def __eq__(self, other):
        return self.title == other.title