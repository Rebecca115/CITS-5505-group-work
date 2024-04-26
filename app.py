from flask import Flask
from models import db

app = Flask(__name__, static_folder='static')
app.config.from_object('conf.Config')
db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
