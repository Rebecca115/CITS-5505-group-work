import hashlib

from flask import request
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from models import User, db
from utils import constants
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    pass

    def validate_username(self, field):
        pass

    def register(self):
        pass


class LoginForm(FlaskForm):
    pass

    def validate(self):
        pass

    def do_login(self):
        pass
