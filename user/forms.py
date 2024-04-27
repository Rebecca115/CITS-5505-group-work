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
    FORM_CLASS = 'form-control'

    username = StringField(label='username', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter username'
    }, validators=[DataRequired('Please enter username')])
    nickname = StringField(label='nickname', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter nickname'
    }, validators=[DataRequired('Please enter nickname'),
                   Length(min=2, max=20, message='Length of nickname is between 2 and 20')])
    password = PasswordField(label='password', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter password'
    }, validators=[DataRequired('Please enter password')])
    confirm_password = PasswordField(label='confirm password', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter confirm password'
    }, validators=[DataRequired('Please enter confirm password'),
                   EqualTo('password', message='passwords do not match')])

    def validate_username(self, field):
        # if the username already exists, raise an error
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('The username already exists')
        return field

    def register(self):

        # 1. Get form information
        username = self.username.data
        password = self.password.data
        nickname = self.nickname.data
        # 2. Add to db.session
        print(username, password, nickname)

        try:
            # Encrypt the password before storing it
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, password=password, nickname=nickname)
            db.session.add(user_obj)
            db.session.commit()
            return user_obj
        except Exception as e:
            print(e)
        return None


class LoginForm(FlaskForm):
    FORM_CLASS = 'form-group'

    username = StringField(label='username', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter username',
        'id': 'username'

    }, validators=[DataRequired('Please enter username')])
    password = PasswordField(label='password', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter password',
        'id': 'password'

    }, validators=[DataRequired('Please enter password')])

    def validate_username(self, username):
        # print(username.data)
        user = User.query.filter_by(username=username.data).first()
        # print("database: ", user)
        if user is None:
            raise ValidationError('username or password is incorrect')

    def do_login(self):
        username = self.username.data
        password = self.password.data

        # print(username, password)
        try:
            password = hashlib.sha256(password.encode()).hexdigest()
            print(username,password)
            user = User.query.filter_by(username=username, password=password).first()
            login_user(user)

            return user
        except Exception as e:
            print(e)

        return None
