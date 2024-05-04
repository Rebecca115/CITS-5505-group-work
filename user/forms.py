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
    """Form for user registration with validations and email confirmation."""
    FORM_CLASS = 'form-control'

    username = StringField(
        'Username',
        render_kw={'class': FORM_CLASS, 'placeholder': 'Please enter username'},
        validators=[DataRequired('Please enter username')]
    )

    nickname = StringField(
        'Nickname',
        render_kw={'class': FORM_CLASS, 'placeholder': 'Please enter nickname'},
        validators=[
            DataRequired('Please enter nickname'),
            Length(min=2, max=20, message='Length of nickname is between 2 and 20')
        ]
    )

    email = StringField(
        'Email',
        render_kw={'class': FORM_CLASS, 'placeholder': 'Please enter email'},
        validators=[DataRequired('Please enter email')]
    )

    password = PasswordField(
        'Password',
        render_kw={'class': FORM_CLASS, 'placeholder': 'Please enter password'},
        validators=[DataRequired('Please enter password')]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        render_kw={'class': FORM_CLASS, 'placeholder': 'Please enter confirm password'},
        validators=[
            DataRequired('Please enter confirm password'),
            EqualTo('password', message='Passwords do not match')
        ]
    )

    def validate_username(self, field):
        """Validate the uniqueness of username."""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username already exists')

    def validate_email(self, field):
        """Validate the uniqueness of email."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email address already exists')

    def register(self):
        """Registers a new user with email confirmation."""
        username, password, nickname, email = (self.username.data, self.password.data,
                                               self.nickname.data, self.email.data)
        password = hashlib.sha256(password.encode()).hexdigest()  # Encrypt the password
        user_obj = User(username=username, password=password, nickname=nickname,
                        email=email, email_verified=False)

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='email-confirm')
        confirm_url = url_for('user.confirm_email', token=token, _external=True)

        msg = Message('Confirm Your Email', recipients=[email])
        msg.body = f'Please click on the link to confirm your email: {confirm_url}'
        Mail(current_app).send(msg)

        db.session.add(user_obj)
        db.session.commit()
        return user_obj


class LoginForm(FlaskForm):
    """Form for user login with validations."""
    FORM_CLASS = 'form-group'

    username = StringField('Username', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter username',
        'id': 'username'
    }, validators=[DataRequired('Please enter username')])

    password = PasswordField('Password', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter password',
        'id': 'password'
    }, validators=[DataRequired('Please enter password')])

    def validate_username(self, username):
        """Validate the existence of username."""
        if not User.query.filter_by(username=username.data).first():
            raise ValidationError('Username or password is incorrect')

    def do_login(self):
        """Performs user login."""
        username, password = self.username.data, self.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return user
        return None
