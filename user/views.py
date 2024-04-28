import hashlib
import time

from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user

from user.forms import RegisterForm, LoginForm
from models import User, db

user = Blueprint('user', __name__,
                 template_folder='templates',
                 static_folder='../assets')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # print("form.is_submitted()",form.is_submitted())
    # print("form.validate_on_submit()",form.validate_on_submit())
    next_url = "index"
    if form.validate_on_submit():
        user = form.do_login()
        if user is not None:
            flash('You have been successfully logged in.', 'success')
            return redirect("/")
        else:
            flash('Login failed, please try again.', 'danger')
            print('Login failed')
            return redirect("login")
    else:
        print(form.errors)
    return render_template('login.html', form=form, next_url=next_url)



@user.route('/logout')
def logout():
    logout_user()
    flash('You have logout.', 'success')
    return redirect("/")





@user.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register()
        # print(user_obj)

        if user_obj:
            # register successful, redirect to login page
            flash('Registration successful!', 'success')
            return redirect(url_for('user.login'))
        else:
            # register failed, redirect to register page
            flash('Registration failed, please try again', 'danger')
    return render_template('register.html', form=form)


@user.route('/mine')
def mine():
    return render_template('mine.html')
