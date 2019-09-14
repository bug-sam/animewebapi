from flask import Flask
from controllers.recommendationController import database
import controllers.recommendationController as rc
import controllers.anilistController as ac
import configuration.configuration as configuration

app = Flask(__name__, static_url_path='')
app.register_blueprint(rc.api)
app.register_blueprint(ac.api)

config = configuration.loadConfiguration()

database.connect(
    config['database host'], 
    config['username'], 
    config['password'],
    config['database'],
    config['table']
)

if __name__ == '__main__':
    app.run(debug=True)