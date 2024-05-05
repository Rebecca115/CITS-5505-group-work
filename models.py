import hashlib
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    # User Model
    __tablename__ = 'accounts_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(64))
    password = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(256))
    gender = db.Column(db.String(16))
    email = db.Column(db.String(64), nullable=False, unique=True)
    sex = db.Column(db.String(16))
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return self.email_verified

    def get_id(self):
        return '{}'.format(self.id)

    def __str__(self):
        return self.nickname

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()


class Question(db.Model):
    __tablename__ = 'qa_question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    img = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=False)

    view_count = db.Column(db.Integer, default=0)
    reorder = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # relation with user
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # one to many
    user = db.relationship('User', backref=db.backref('question_list', lazy='dynamic'))

    @property
    def get_img_url(self):
        return 'statics/' + self.img if self.img else ''

    @property
    def comment_count(self):
        return self.question_comment_list.filter_bycount()

    @property
    def answer_count(self):
        return self.answer_list.count()

    @property
    def like_count(self):
        return self.question_like_list.count()


class Answer(db.Model):
    __tablename__ = 'qa_answer'
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)

    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))

    # relation with question
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # one to many with user
    user = db.relationship('User', backref=db.backref('answer_list', lazy='dynamic'))
    # one to many with question
    question = db.relationship('Question', backref=db.backref('answer_list', lazy='dynamic'))

    @property
    def like_count(self):
        return self.answer_like_list.count()

    def comment_list(self, reply_id=None):
        return self.answer_comment_list.filter_by(reply_id=reply_id)

    @property
    def comment_count(self):
        return self.answer_comment_list.count()


class AnswerLike(db.Model):
    __tablename__ = 'qa_answer_like'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    # one to many with user
    user = db.relationship('User', backref=db.backref('answer_like_list', lazy='dynamic'))
    # one to many with answer
    answer = db.relationship('Answer', backref=db.backref('answer_like_list', lazy='dynamic'))
    # one to many with question
    question = db.relationship('Question', backref=db.backref('question_like_list', lazy='dynamic'))
