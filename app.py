import os

from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer

from task.views import quest
from models import db, User
from user.views import user
from utils import initialize_database

app = Flask(__name__, static_folder='static')
app.config.from_object('conf.Config')

ckeditor = CKEditor()
ckeditor.init_app(app)

# init database
db.init_app(app)
migrate = Migrate(app, db)

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

app.register_blueprint(quest, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')

# Login
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = 'Please login'
login_manager.login_message_category = "danger"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if not os.path.exists('instance/data.db'):
    initialize_database.create_local_db(app,db)

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=8080, debug=True)

