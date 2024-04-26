import hashlib

from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user

from user.forms import RegisterForm, LoginForm
from models import User, db

user = Blueprint('accounts', __name__,
                 template_folder='templates',
                 static_folder='../assets')


@user.route('/login')
def login():
    pass


@user.route('/logout')
def logout():
    pass


@user.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@user.route('/mine')
def mine():
    return render_template('mine.html')
