from flask import Blueprint, render_template, request, abort, redirect, url_for, flash, jsonify
from flask_ckeditor import CKEditor
from flask_login import login_required, current_user

import app
from models import Question, Answer, db, AnswerLike
from quest.form import WriteQuestionForm, WriteAnswerForm

quest = Blueprint('quest', __name__,
               template_folder='templates',
               static_folder='../static')


@quest.route('/')
def indexPage():
    per_page = 5
    page = int(request.args.get('page', 1))
    page_data = Question.query.order_by(Question.created_at.desc()).paginate(
        page=page, per_page=per_page)
    return render_template('index.html', page_data=page_data)


@quest.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = WriteQuestionForm()

    if form.validate_on_submit():
        try:
            que_obj = form.save()
            if que_obj:
                flash('Quest has been post successfully ', 'success')
                return redirect("/")
        except Exception as e:
            print(e)
        flash('Quest post failed', 'danger')
    return render_template('post.html', form=form)

@quest.route('/q/list')
def question_list():
    """
    // json
    {
        'code': 0,
        'data': ''
    }
    """
    try:
        per_page = 5  #
        page = int(request.args.get('page', 1))
        page_data = Question.query.paginate(
            page=page, per_page=per_page)
        data = render_template('qa_list.html', page_data=page_data)
        # print(data)

        return {'code': 0, 'data': data}
    except Exception as e:
        print(e)
        data = ''
    return {'code': 1, 'data': ''}


@quest.route('/detail/<int:q_id>', methods=['GET', 'POST'])
def detail(q_id):


    question = Question.query.get(q_id)

    answer = Answer.query.filter_by(q_id=q_id).order_by(Answer.created_at.desc()).all()

    # check if the answer is liked by the current user
    for ans in answer:
        ans.already_liked = AnswerLike.query.filter_by(
            user_id=current_user.id,
            answer_id=ans.id
        ).first() is not None

    form = WriteAnswerForm()

    if form.validate_on_submit():
        try:
            if not current_user.is_authenticated:
                flash('Please login', 'danger')
                return redirect(url_for('user.login'))
            form.save(question=question)
            flash('Answer successfully', 'success')
            return redirect(url_for('quest.detail', q_id=q_id))
        except Exception as e:
            print(e)

    return render_template('detail.html',
                           question=question,
                           answer=answer,
                           form=form

                           )


from flask import jsonify


@quest.route('/answer/like/<int:answer_id>', methods=['POST'])
# @login_required
def answer_like(answer_id):
    if not current_user.is_authenticated:

        return jsonify({'error': 'Please login'}), 401

    try:

        existing_like = AnswerLike.query.filter_by(user_id=current_user.id,
                                                   answer_id=answer_id).first()
        if existing_like:
            return jsonify({'error': 'You have liked this answer'}), 409

        new_like = AnswerLike(user_id=current_user.id, answer_id=answer_id)
        db.session.add(new_like)
        db.session.commit()

        # 正常的处理逻辑, 返回新的点赞计数
        like_count = Answer.query.get(answer_id).like_count  # 假设存在like_count计算逻辑
        return jsonify({'message': '点赞成功', 'like_count': like_count}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': '服务器错误'}), 500