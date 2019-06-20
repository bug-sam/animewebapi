from flask import Flask
import recommendationController as rc
import kitsuController as kc

app = Flask(__name__, static_url_path="")
app.register_blueprint(rc.api)
app.register_blueprint(kc.api)

if __name__ == "__main__":
    app.run(debug=True)