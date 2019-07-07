from flask import Flask
import json
import controllers.recommendationController as rc
from controllers.recommendationController import database
import controllers.kitsuController as kc

def loadConfiguration(filepath):
    f = open(filepath)
    return json.loads(f.read())

app = Flask(__name__, static_url_path="")
app.register_blueprint(rc.api)
app.register_blueprint(kc.api)
config = loadConfiguration("./configuration/configuration.json")
database.connect(
    config["database host"], 
    config["username"], 
    config["password"],
    config["database"]
)
database.read("anime")
    
if __name__ == "__main__":
    app.run(debug=True)
