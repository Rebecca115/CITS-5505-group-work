import os

from flask import Flask, session, g
from flask_login import LoginManager

from quest.view import index
from models import db, User
from user.views import user
from utils import database_creator

app = Flask(__name__, static_folder='static')
app.config.from_object('conf.Config')

# create database
database_creator.create_local_db(app, db)

# init database
db.init_app(app)

app.register_blueprint(index, url_prefix='/')
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


@app.before_request
def before_request():
    """ if there is a user id, set it to the global object"""
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.get(user_id)
        print(user)
        g.current_user = user

    #
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)
