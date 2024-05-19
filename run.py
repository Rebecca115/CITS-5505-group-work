
from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate


from app.question.views import quest
from app.user.views import user
from models import db, User


def create_app(config_class='app.conf.Config'):
    app = Flask(__name__, static_folder='/app/static', static_url_path='/../static')
    app.config.from_object(config_class)

    # Initialize extensions
    ckeditor = CKEditor(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    mail = Mail(app)

    # Register blueprints
    app.register_blueprint(quest, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')

    # Setup login manager
    login_manager = LoginManager(app)
    login_manager.login_view = "user.login"
    login_manager.login_message = 'Please login'
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # CSRF protection
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
