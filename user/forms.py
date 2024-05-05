import hashlib

from flask import request, current_app, url_for
from flask_login import login_user
from flask_mail import Message, Mail
from flask_wtf import FlaskForm
from itsdangerous import URLSafeTimedSerializer
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from models import User, db
from utils import constants



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
    email = StringField(label='email', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter email'
    }, validators=[DataRequired('Please enter email')])
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

    def validate_email(self, field):
        # if the username already exists, raise an error
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('The email address already exists')
        return field

    def register(self):

        # 1. Get form information
        username = self.username.data
        password = self.password.data
        nickname = self.nickname.data
        email = self.email.data


        try:
            # Encrypt the password before storing it
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, password=password, nickname=nickname, email=email, email_verified=False)
            print(user_obj)

            user_email = email

            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(user_email, salt='email-confirm')

            confirm_url = url_for('user.confirm_email', token=token, _external=True)

            msg = Message('Confirm Your Email', recipients=[user_email])
            msg.body = f'Please click on the link to confirm your email: {confirm_url}'

            mail = Mail(current_app)
            mail.send(msg)


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
        user = User.query.filter_by(username=username.data).first()
        # print("database: ", user)
        if user is None:
            print('username or password is incorrect')
            raise ValidationError('username or password is incorrect')

    def validate_email(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user.is_active is False:
            raise ValidationError('Email not verified.')


    def do_login(self):
        username = self.username.data
        password = self.password.data

        try:
            user = User.query.filter_by(username=username).first()

            if user.check_password(password) is False:
                return None
            login_user(user)

            return user
        except Exception as e:
            print(e)

        return None
