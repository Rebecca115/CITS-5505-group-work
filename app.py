from flask import Flask

from index.view import index
from models import db

app = Flask(__name__, static_folder='static')
app.config.from_object('conf.Config')

# init database
db.init_app(app)

app.register_blueprint(index, url_prefix='/')


#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)
