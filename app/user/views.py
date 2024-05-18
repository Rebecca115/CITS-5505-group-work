import os

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import logout_user, login_required, current_user
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer
from sqlalchemy import func
from werkzeug.utils import secure_filename

from app.user.forms import RegisterForm, LoginForm, RestPassForm, ForgotPassForm, UserProfileForm, UpdateAvatarForm, \
    ChangePasswordForm
from models import User, db, Question, Answer

user = Blueprint('user', __name__, template_folder='../templates')


@user.route('/login', methods=['GET', 'POST'])
def login():
    """Route for logging in the user"""
    form = LoginForm()

    # Process the form submission
    if form.validate_on_submit():
        user = form.do_login()
        if user:
            # Successful login
            flash(f'Welcome back,{user.username}.', 'success')
            return redirect("/")
        else:
            # Login failed, show message
            flash('Login failed, please try again.', 'danger')
            return render_template('login.html', form=form)

    # Render the login template on GET or failed form submission
    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    """Route for logging out the user"""
    logout_user()  # Logout the current user
    flash('You have been logged out.', 'success')
    return redirect(url_for('question.index'))


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


@user.route('/<int:id>/info/')
# @login_required
def info(id):
    """Route for displaying user profile information"""
    # Fetch user by ID
    if id != current_user.id:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    user = User.query.filter_by(id=id).first_or_404(description='User not found.')
    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('user.change_profile', id=user.id))

    return render_template('user-info.html', form=form, user=user)


@user.route('/<int:id>/posted')
@login_required
def user_posted_questions(id):
        user = User.query.get_or_404(id)
        print(f"User ID: {user.id}, Type: {type(user.id)}")

        questions = Question.query.filter_by(user_id=user.id).all()

        return render_template('posted-questions.html', user=user, questions=questions)


@user.route('/change_password')
@login_required
def change_password():
    """Route for changing the user's password"""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Check if the current password matches
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('user.change_password'))

        # Check if new password and confirm password match
        if form.new_password.data != form.confirm_password.data:
            flash('New password and confirm password do not match.', 'danger')
            return redirect(url_for('user.change_password'))


        # Update the user's password
        current_user.set_password(form.current_password.data)
        db.session.commit()

        flash('Your password has been successfully updated.', 'success')
        return redirect(url_for('user.info', id=current_user.id))

    return render_template('change_password.html', form=form)

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


@user.route('/forget-password', methods=['POST', 'GET'])
def forget_password():
    """Route for handling forget password request"""
    form = ForgotPassForm()
    if form.validate_on_submit():
        user = form.forget_password()
        if user:
            return redirect(url_for('user.login'))
        else:
            flash('Password reset failed, please try again.', 'danger')
    return render_template('forget_password.html', form=form)


@user.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Route for handling password reset"""
    form = RestPassForm()
    if form.validate_on_submit():
        user = form.reset_password(token)
        if user:
            return redirect(url_for('user.login'))
        else:
            flash('Password reset failed, please try again.', 'danger')

    return render_template('templates/reset_password.html', form=form, token=token)



@user.route('/<int:id>/answers', methods=['GET'])
@login_required
def user_answers(id):
    if id != current_user.id:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    answers = Answer.query.filter_by(user_id=user.id).all()

    return render_template('user_answers.html', user=user, answers=answers)


@user.route('/<int:id>/change_profile', methods=['GET', 'POST'])
@login_required
def change_profile(id):
    """Route to change user profile."""
    if id != current_user.id:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    user = User.query.filter_by(id=id).first_or_404(description='User not found.')
    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('user.change_profile', id=user.id))

    return render_template('user-info.html', form=form, user=user)


@user.route('/<int:id>/answered', methods=['GET', 'POST'])
def answered(id):
    """ Route to get answered questions by user. """
    user_id = id
    answers = Answer.query.filter_by(user_id=user_id).all()

    if not answers:
        return jsonify({'message': 'No answers found'}), 404
    return jsonify({'message': 'Success', 'data': [ans.to_dict() for ans in answers]}), 200


@user.route('/<int:id>/update-avatar', methods=['GET', 'POST'])
@login_required
def update_avatar(id):
    if id != current_user.id:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    form = UpdateAvatarForm()

    if form.validate_on_submit():
        file = form.avatar.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        user.avatar = filename
        db.session.commit()

        flash('Your avatar has been updated!', 'success')
        return redirect(url_for('user_profile', id=user.id))

    return render_template('update_avatar.html', user=user, form=form)
