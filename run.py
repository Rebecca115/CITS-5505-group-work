import os

from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer

from app.question.views import quest
from models import db, User
from app.user.views import user
# from utils import initialize_database


app = Flask(__name__, static_folder='/app/static', static_url_path='/../static')
app.config.from_object('app.conf.Config')

ckeditor = CKEditor()
ckeditor.init_app(app)

# init database
db.init_app(app)
migrate = Migrate(app, db)

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
app.config['WTF_CSRF_ENABLED'] = True

app.register_blueprint(quest, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')

# Login
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = 'Please login'
login_manager.login_message_category = "danger"
login_manager.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
