from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import logout_user, login_required, current_user
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer
from sqlalchemy import func
from app.user.forms import RegisterForm, LoginForm, RestPassForm, ForgotPassForm
from models import User, db, Task, Answer

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
            flash(f'Welcome back,{user.nickname}.','success')
            return redirect("/")
        else:
            # Login failed, show message
            flash('Login failed, please try again.', 'danger')
            return render_template('login.html', form=form)


    # Render the login template on GET or failed form submission
    return render_template('login.html', form=form)


# Route for handling logout
# @user.route('/logout')
# @login_required
# def logout():
#     """Route for logging out the user"""
#     logout_user()  
#     flash('You have been logged out.', 'success')
#     redirect_url = url_for('quest.index_page')
#     print(redirect_url) 
#     return redirect(url_for('quest.index_page'))

@user.route('/logout')
@login_required
def logout():
    """Route for logging out the user"""
    logout_user()  # Logout the current user
    flash('You have been logged out.', 'success')
    return redirect(url_for('task.index_page')) 


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
    return render_template('templates/register.html', form=form)


@user.route('/info/<int:id>/')
# @login_required
def profile(id):
    """Route for displaying user profile information"""
    # Fetch user by ID
    user = User.query.filter_by(id=id).first_or_404(description='User not found.')
    # Render the user profile template
    return render_template('user-info.html', user=user)


@user.route('/<int:id>/tasks')
# @login_required
def my_tasks(id):
    """Retrieve and display tasks posted by the current logged-in user."""
    try:
        user_id = id
        tasks = Task.query.filter_by(user_id=user_id).all()
        return render_template('templates/mytask.html', tasks=tasks, current_user=current_user)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')


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


@user.route('/forgot-password', methods=['POST', 'GET'])
def forgot_password():
    """Route for handling forgot password request"""
    form = ForgotPassForm()
    if form.validate_on_submit():
        user = form.forgot_password()
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


@user.route('/get_top_users')
def get_top_users():
    """Route for getting top users"""
    top_user_ids_subquery = (db.session.query(
        Answer.user_id,
        func.count(Answer.id).label('answer_count'))
                             .join(User)
                             .group_by(Answer.user_id)
                             .order_by(func.count(Answer.id).desc())
                             .limit(10)
                             .subquery())

    top_users = db.session.query(
        User,
        top_user_ids_subquery.c.answer_count
    ).join(
        top_user_ids_subquery, User.id == top_user_ids_subquery.c.user_id
    ).all()

    users_data = []
    for user, answer_count in top_users:
        user_dict = user.to_dict()
        user_dict['answer_count'] = answer_count
        users_data.append(user_dict)

    return jsonify({"users": users_data}), 200

@user.route('/change_email/<int:id>')
@login_required
def change_email(id):
    """Route for changing the user's email address"""
    if id != current_user.id:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    data = request.get_json()
    new_email = data.get('new_email')
    age = data.get('age')
    current_user.email = new_email
    db.session.commit()
    return jsonify({'message': 'Email updated successfully'}), 200


@user.route('/change_nickname/<int:id>')
@login_required
def change_nickname(id):
    """Route for changing the user's nickname"""

    if id != current_user.id:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    data = request.get_json()
    if 'new_nickname' in data:
        user.nickname = data['username']


    db.session.commit()
    return jsonify({'message': 'Nickname updated successfully'}), 200



# @user.route('/upload/<int:id>', methods=['POST'])
# @login_required
# def upload(id):
#     """Route for uploading user profile picture"""
#     if current_user.id != id:
#         return jsonify({'error': 'You are not authorized to perform this action'}), 403
#     user = User.query.filter_by(id=id).first_or_404(description='User not found.')
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
#         user.profile_picture = filename
#         db.session.commit()
#         return jsonify({'message': 'Profile picture uploaded successfully'}), 200
#     return jsonify({'error': 'Invalid file type'}), 400

@user.route('/<int:t_id>/answer', methods=['GET'])
@login_required
def task_answer(t_id):
    """ Route to get answer by user. """
    user_id = current_user.id
    answers = Answer.query.filter_by(user_id=user_id).all()

    if not answers:
        return jsonify({'message': 'No answers found'}), 404
    return jsonify({'message': 'Success', 'data': [ans.to_dict() for ans in answers]}), 200


@user.route('/<int:id>/change_profile', methods=['POST'])
@login_required
def change_profile(id):
    """ Route to change user profile. """
    if id != current_user.id:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

    data = request.get_json()
    user = User.query.filter_by(id=id).first_or_404(description='User not found.')

    if 'new_nickname' in data:
        user.nickname = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'avatar' in data:
        user.profile_picture = data['avatar']
    if 'gender' in data:
        user.gender = data['gender']



    if 'username' in data:
        user.nickname = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'avatar' in data:
        user.profile_picture = data['avatar']
    if 'gender' in data:
        user.gender = data['gender']

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@user.route('/<int:id>/answered', methods=['GET', 'POST'])
def answered(id):
    """ Route to get answered questions by user. """
    user_id = id
    answers = Answer.query.filter_by(user_id=user_id).all()

    if not answers:
        return jsonify({'message': 'No answers found'}), 404
    return jsonify({'message': 'Success', 'data': [ans.to_dict() for ans in answers]}), 200