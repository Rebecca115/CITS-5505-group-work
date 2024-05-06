import os

from flask import Blueprint, render_template, flash, redirect, url_for, session, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer
from werkzeug.utils import secure_filename

from user.forms import RegisterForm, LoginForm
from models import User, db, Question

user = Blueprint('user', __name__, template_folder='templates', static_folder='../assets')

@user.route('/login', methods=['GET', 'POST'])
def login():
    """Route for logging in the user"""
    form = LoginForm()

    # Process the form submission
    if form.validate_on_submit():
        user = form.do_login()
        if user:
            # Successful login
            return redirect("/")
        else:
            # Login failed, show message
            flash('Login failed, please try again.', 'danger')
    else:
        # Form validation failed, show message
        flash('Login failed, please try again.', 'danger')

    # Render the login template on GET or failed form submission
    return render_template('login.html', form=form)

# Route for handling logout
@user.route('/logout')
@login_required
def logout():
    """Route for logging out the user"""
    logout_user()  # Logout the current user
    flash('You have been logged out.', 'success')
    return redirect("/")

# Route for handling registration
@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # Process the form submission
    if form.validate_on_submit():
        user_obj = form.register()

        if user_obj:
            # Registration successful

            flash('Registration successful!', 'success')

            return redirect(url_for('user.login'))
        else:
            # Registration failed
            flash('Registration failed, please try again.', 'danger')
    else:
        # Form errors handling
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f'Error in {fieldName}: {err}', 'danger')

    # Render the registration template on GET or failed form submission
    return render_template('register.html', form=form)

@user.route('/<int:id>/mine')
@login_required
def mine(id):
    """Route for displaying user profile information"""
    # Fetch user by ID
    user = User.query.filter_by(id=id).first_or_404(description='User not found.')
    # Render the user profile template
    return render_template('mine.html', user=user)

@user.route('/<int:id>/questions')
@login_required
def my_questions(id):
    """Retrieve and display questions posted by the current logged-in user."""
    try:
        user_id = id

        questions = Question.query.filter_by(user_id=user_id).all()
        questions_data = [
            {'title': question.title, 'description': question.content, 'id': question.id}
            for question in questions
        ]
        return jsonify(questions_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """Route for changing the user's password"""

    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # Verify and update password logic
    if not current_user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect.'}), 400

    if current_user.check_password(new_password):
        return jsonify({'error': 'New password cannot be the same as current password.'}), 400

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200

@user.route('/confirm-email/<token>')
def confirm_email(token):
    """Route for confirming the user's email address"""
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='email-confirm', max_age=3600)

        user = User.query.filter_by(email=email).first_or_404(description='User not found.')

        if user.email_verified:
            return jsonify(message="This email is already confirmed."), 200
        else:
            user.email_verified = True
            db.session.commit()
            return jsonify(message="You have successfully confirmed your email."), 200

    except SignatureExpired:
        return jsonify({'error': "The confirmation link has expired."}), 400
    except BadSignature:

        return jsonify({'error': "Invalid confirmation link."}), 400
        return 'Invalid confirmation link.'

    return 'You have successfully confirmed your email.'
