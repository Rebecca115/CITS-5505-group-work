from flask import Blueprint, render_template, request, abort, redirect, url_for, flash, jsonify
from flask_ckeditor import CKEditor
from flask_login import login_required, current_user

import app
from models import Question, Answer
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
        print(data)

        return {'code': 0, 'data': data}
    except Exception as e:
        print(e)
        data = ''
    return {'code': 1, 'data': ''}


@quest.route('/detail/<int:q_id>', methods=['GET', 'POST'])
def detail(q_id):


    question = Question.query.get(q_id)
    print(question, q_id)

    answer = question.answer_list.filter_by().first()
    print(answer)

    return render_template('detail.html',
                           question=question,
                           answer=answer,
                           )


