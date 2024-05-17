import hashlib
import os
import uuid

from flask import request, current_app, url_for
from flask_login import login_user
from flask_mail import Message, Mail
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, ValidationError
from wtforms.fields.core import DateField, RadioField
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

from models import User, db
from utils import constants


class RegisterForm(FlaskForm):
    """Form for user registration with validations and email confirmation."""
    FORM_CLASS = 'form-control'

    username = StringField(
        'Username',
        render_kw={'class': FORM_CLASS, 'placeholder': 'Please enter username'},
        validators=[DataRequired('Please enter username'),
        Length(min=2, max=20, message='Length of username is between 2 and 20')]
    )

    avatar = FileField(
        'Avatar',
        render_kw={'class': FORM_CLASS, 'placeholder': 'Please upload avatar'},
        validators=[
            FileAllowed(['jpg', 'png'], 'Images only!')
        ]
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
        if self.avatar.data is None:
            # self.avatar.data = request.files[constants.DEFAULT_AVATAR]
            self.avatar.data = 'None'
        username, password, nickname, email, avatar_file = (self.username.data, self.password.data,
                                                            self.nickname.data, self.email.data, self.avatar.data)
        password = hashlib.sha256(password.encode()).hexdigest()

        file_extension = os.path.splitext(avatar_file.filename)[1]
        random_filename = str(uuid.uuid4()) + file_extension
        secure_random_filename = secure_filename(random_filename)

        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_random_filename)
        avatar_file.save(save_path)

        user_obj = User(username=username, password=password, nickname=nickname,
                        email=email, email_verified=False, avatar=secure_random_filename)

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


class RestPassForm(FlaskForm):
    """Form for resetting password with validations."""
    FORM_CLASS = 'form-group'

    new_password = PasswordField('Password', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter new password',
        'id': 'new_password'
    }, validators=[DataRequired('Please enter new password')])

    confirm_password = PasswordField('Confirm Password', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please confirm new password',
        'id': 'confirm_password'
    }, validators=[DataRequired('Please confirm new password'),
                   EqualTo('new_password', message='Passwords must match')])

    def reset_password(self, token):
        """Reset user's password."""

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='reset-password', max_age=3600)

        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashlib.sha256(self.new_password.data.encode()).hexdigest()
            db.session.commit()
            return user


class ForgotPassForm(FlaskForm):
    """Form for forgot password with validations."""
    FORM_CLASS = 'form-group'

    email = StringField('Email', render_kw={
        'class': FORM_CLASS,
        'placeholder': 'Please enter email',
        'id': 'email'
    }, validators=[DataRequired('Please enter email')])

    def validate_email(self, email):
        """Validate the existence of email."""
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError('Email does not exist')

    def forgot_password(self):
        """Sends reset password link to user's email."""
        email = self.email.data
        user = User.query.filter_by(email=email).first()

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='reset-password')

        reset_url = url_for('user.reset_password', token=token, _external=True)
        msg = Message('Reset Your Password', recipients=[email])
        msg.body = f'Please click on the link to reset your password: {reset_url}'
        Mail(current_app).send(msg)
        return user



class UserProfileForm(FlaskForm):
    nickname = StringField('Nickname', validators=[Optional(), Length(max=64)])
    username = StringField('Username', render_kw={'readonly': True})
    signature = TextAreaField('Signature', validators=[Optional(), Length(max=200)])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('secret', 'Secret')], validators=[Optional()])
    dob = DateField('DOB', validators=[Optional()])
    school_info = StringField('School', validators=[Optional(), Length(max=64)])
    submit = SubmitField('Save')

class UpdateAvatarForm(FlaskForm):
    avatar = FileField('Upload new avatar', validators=[DataRequired()])
    submit = SubmitField('Update')