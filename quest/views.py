from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_

from models import Question, Answer, db, AnswerLike
from quest.form import WriteQuestionForm, WriteAnswerForm

quest = Blueprint('quest', __name__,
                  template_folder='templates',
                  static_folder='../static')



@quest.route('/')
def indexPage():
    """ Home page route, display a list of paginated questions. """
    per_page = 5
    page = request.args.get('page', 1, type=int)
    page_data = Question.query.order_by(Question.created_at.desc()).paginate(
        page=page, per_page=per_page)
    return render_template('index.html', page_data=page_data)

@quest.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    """ Route to post a new question, requires user to be logged in. """
    form = WriteQuestionForm()

    if form.validate_on_submit():
        try:
            que_obj = form.save()
            if que_obj:
                flash('Quest has been posted successfully', 'success')
                return redirect(url_for('quest.indexPage'))
        except Exception as e:
            flash('Error posting Quest: {}'.format(e), 'danger')
    return render_template('post.html', form=form)

@quest.route('/q/list')
def question_list():
    """ Route to list questions in a paginated manner and return as JSON. """
    try:
        per_page = 5  # Define the number of items per page.
        page = request.args.get('page', 1, type=int)
        page_data = Question.query.paginate(page=page, per_page=per_page)
        data = render_template('qa_list.html', page_data=page_data)
        return jsonify(code=0, data=data)
    except Exception as e:
        return jsonify(code=1, data=str(e)), 400

@quest.route('/detail/<int:q_id>', methods=['GET', 'POST'])
def detail(q_id):
    """ Route for question details and posting answers to the question. """
    question = Question.query.get_or_404(q_id)

    answers = Answer.query.filter_by(q_id=q_id).order_by(Answer.created_at.desc()).all()
    print(answers)

    # Check if the answer is liked by the current user
    if not current_user.is_anonymous:
        for ans in answers:
            ans.already_liked = AnswerLike.query.filter_by(
                user_id=current_user.id,
                answer_id=ans.id
            ).first() is not None

    form = WriteAnswerForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please login', 'danger')
            return redirect(url_for('user.login'))
        try:
            form.save(question=question)
            flash('Answer posted successfully', 'success')
            return redirect(url_for('quest.detail', q_id=q_id))
        except Exception as e:
            flash('Error posting answer: {}'.format(e), 'danger')

    return render_template('detail.html',
                           question=question,
                           answers=answers,
                           form=form)

@quest.route('/answer/like/<int:answer_id>', methods=['POST'])
def answer_like(answer_id):
    """ Route to like an answer, requires user to be logged in. """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please login'}), 401

    try:
        # Check for existing like
        existing_like = AnswerLike.query.filter_by(user_id=current_user.id,
                                                   answer_id=answer_id).first()
        if existing_like:
            return jsonify({'error': 'You have already liked this answer'}), 409

        # Create new like
        new_like = AnswerLike(user_id=current_user.id, answer_id=answer_id)
        db.session.add(new_like)
        db.session.commit()

        # Fetch the new like count
        like_count = Answer.query.get(answer_id).like_count + 1 # Assuming like_count is a field
        return jsonify({'message': 'Success', 'like_count': like_count}), 201
    except Exception as e:
        return jsonify({'error': 'Unknown error: {}'.format(e)}), 500


@quest.route('/answer/unlike/<int:answer_id>', methods=['POST'])
def answer_unlike(answer_id):
    """ Route to unlike an answer, requires user to be logged in. """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please login'}), 401

    try:
        # Check for existing like
        existing_like = AnswerLike.query.filter_by(user_id=current_user.id,
                                                   answer_id=answer_id).first()
        if not existing_like:
            return jsonify({'error': 'You have not liked this answer'}), 409

        # Remove the like
        db.session.delete(existing_like)
        db.session.commit()

        # Fetch the new like count
        like_count = Answer.query.get(answer_id).like_count - 1 # Assuming like_count is a field
        return jsonify({'message': 'Success', 'like_count': like_count}), 200
    except Exception as e:
        return jsonify({'error': 'Unknown error: {}'.format(e)}), 500

@quest.route('/answer/delete/<int:answer_id>', methods=['POST'])
def answer_delete(answer_id):
    """ Route to delete an answer, requires user to be logged in. """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please login'}), 401

    try:
        # Check if the answer exists
        answer = Answer.query.get(answer_id)
        if not answer:
            return jsonify({'error': 'Answer not found'}), 404

        # Check if the user owns the answer
        if answer.user_id != current_user.id:
            return jsonify({'error': 'You do not own this answer'}), 403

        # Delete the answer
        db.session.delete(answer)
        db.session.commit()

        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        return jsonify({'error': 'Unknown error: {}'.format(e)}), 500

@quest.route('/answer/edit/<int:answer_id>', methods=['GET', 'POST'])
def answer_edit(answer_id):
    """ Route to edit an answer, requires user to be logged in. """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please login'}), 401

    answer = Answer.query.get(answer_id)
    if not answer:
        return jsonify({'error': 'Answer not found'}), 404

    if answer.user_id != current_user.id:
        return jsonify({'error': 'You do not own this answer'}), 403

    form = WriteAnswerForm(obj=answer)

    if form.validate_on_submit():
        try:
            answer.content = form.content.data
            db.session.commit()
            return jsonify({'message': 'Success'}), 200
        except Exception as e:
            return jsonify({'error': 'Unknown error: {}'.format(e)}), 500

    return render_template('edit_answer.html', form=form, answer=answer)

@quest.route('/answer/<int:answer_id>')
def answer_detail(answer_id):
    """ Route to get details of an answer. """
    answer = Answer.query.get(answer_id)
    if not answer:
        return jsonify({'error': 'Answer not found'}), 404

    return jsonify({'message': 'Success', 'data': answer.to_dict()}), 200

@quest.route('/answer/list/<int:q_id>')
def answer_list(q_id):
    """ Route to list answers to a question. """
    answers = Answer.query.filter_by(q_id=q_id).all()
    return jsonify({'message': 'Success', 'data': [ans.to_dict() for ans in answers]}), 200

@quest.route('/answer/like/list/<int:answer_id>')
def answer_like_list(answer_id):
    """ Route to list users who liked an answer. """
    likes = AnswerLike.query.filter_by(answer_id=answer_id).all()
    return jsonify({'message': 'Success', 'data': [like.to_dict() for like in likes]}), 200


@quest.route('/search', methods=['GET'])
def search():
    """ Route to globally search within all question titles, question contents, and all answers. """
    query = request.args.get('query', '')

    if not query:
        return jsonify({'error': 'Empty search query'}), 400

    try:
        matched_questions = Question.query.filter(
            or_(
                Question.title.ilike(f'%{query}%'),
                Question.content.ilike(f'%{query}%')
            )
        ).all()

        matched_answers = Answer.query.filter(
            Answer.content.ilike(f'%{query}%')
        ).all()

        question_results = [
            {
                'type': 'question',
                'id': question.id,
                'title': question.title,
                'content': question.content
            }
            for question in matched_questions
        ]

        answer_results = [
            {
                'type': 'answer',
                'id': answer.id,
                'content': answer.content,
                'question_id': answer.q_id
            }
            for answer in matched_answers
        ]

        results = question_results + answer_results

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': f'Unknown error: {e}'}), 500

@quest.route('/question/delete/<int:q_id>', methods=['POST'])
def question_delete(q_id):
    """ Route to delete a question, requires user to be logged in. """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please login'}), 401

    try:
        # Check if the question exists
        question = Question.query.get(q_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404

        # Check if the user owns the question
        if question.user_id != current_user.id:
            return jsonify({'error': 'You do not own this question'}), 403

        # Delete the question
        db.session.delete(question)
        db.session.commit()

        return jsonify({'message': 'Success'}), 200

    except Exception as e:
        return jsonify({'error': f'Unknown error: {e}'}), 500

@quest.route('/question/edit/<int:q_id>', methods=['GET', 'POST'])
def question_edit(q_id):
    """ Route to edit a question, requires user to be logged in. """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please login'}), 401

    question = Question.query.get(q_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    if question.user_id != current_user.id:
        return jsonify({'error': 'You do not own this question'}), 403

    form = WriteQuestionForm(obj=question)
    if form.validate_on_submit():
        try:
            form.save(question=question)
            return jsonify({'message': 'Success'}), 200
        except Exception as e:
            return jsonify({'error': f'Unknown error: {e}'}), 500

@quest.route('/question/<int:q_id>')
def question_detail(q_id):
    """ Route to get details of a question. """
    question = Question.query.get(q_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    return jsonify({'message': 'Success', 'data': question.to_dict()}), 200

@quest.route('/question/category/<category>')
def question_by_category(category):
    """ Route to list questions by category. """
    questions = Question.query.filter_by(category=category).all()
    return jsonify({'message': 'Success', 'data': [q.to_dict() for q in questions]}), 200




    #TODO
    # questions list for the user
    # question category
    # Scoreborad for the top 10 users who achieved the highest score
    #
    #