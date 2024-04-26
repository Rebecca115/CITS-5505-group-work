from flask import Blueprint, render_template, request, abort

from models import Question

index = Blueprint('index', __name__,
               template_folder='templates',
               static_folder='../static')


@index.route('/')
def indexPage():

    return render_template('index.html')


# @index.route('/write')
# def write():
#
#     return render_template('write.html')


# @index.route('/detail/<int:q_id>')
# def detail(q_id):
#     # question detail
#     question = Question.query.get(q_id)
#     if not question.is_valid:
#         abort(404)
#
#     answer = question.answer_list.filter_by(is_valid=True).first()
#     return render_template('detail.html', question=question, answer=answer)
