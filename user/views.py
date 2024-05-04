import hashlib
import time

from flask import Blueprint, render_template, flash, redirect, url_for, session, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer

from user.forms import RegisterForm, LoginForm
from models import User, db

user = Blueprint('user', __name__,
                 template_folder='templates',
                 static_folder='../assets')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    next_url = "index"

    if form.validate_on_submit():
        user = form.do_login()
        if user is not None:
            # flash('You have been successfully logged in.', 'success')
            return redirect("/")
        else:
            flash('Login failed, please try again.', 'danger')

    else:
        flash(f'Login failed, please try again.', 'danger')


    return render_template('login.html', form=form, next_url=next_url)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logout.', 'success')
    return redirect("/")


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Register form data", form.data)
        user_obj = form.register()
        # print(user_obj)

        if user_obj:
            # register successful, redirect to login page
            flash('Registration successful!', 'success')
            return redirect(url_for('user.login'))
        else:
            # register failed, redirect to register page
            flash('Registration failed, please try again', 'danger')
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f'Error in {fieldName}: {err}')
    return render_template('register.html', form=form)


@user.route('/mine/<int:id>')
@login_required
def mine(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return 'User not found!', 404
    return render_template('mine.html', user=user)


@user.route('/change_password', methods=['POST'])
@login_required  # Ensure the user is logged in
def change_password():
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    print(current_password)
    print(new_password)

    # Verify current password is correct
    if not current_user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect.'}), 400

    if current_user.check_password(new_password):
        return jsonify({'error': 'New password can not be the same current password.'}), 400

    # Update the user's password
    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200


@user.route('/send-confirmation')
def send_confirmation_email():
    pass


@user.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if not user:
            return 'User not found.', 404
        else:
            user.email_verified = True
            db.session.commit()
    except SignatureExpired:
        return 'The confirmation link has expired.'
    except BadSignature:
        return 'Invalid confirmation link.'

    # 这里添加验证逻辑
    return 'You have successfully confirmed your email.'
