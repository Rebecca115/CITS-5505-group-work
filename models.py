import hashlib
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    # User Model
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    DOB = db.Column(db.String(64))
    password = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(256))
    gender = db.Column(db.String(16))
    email = db.Column(db.String(64), unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    school = db.Column(db.String(64))

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

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        return {

            'avatar': self.avatar,
            'gender': self.gender,
            'answer_count': self.answer_list.count(),
        }


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    img = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=True)

    category = db.Column(db.String(64))

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # relation with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # one to many
    user = db.relationship('User', backref=db.backref('question_list', lazy='dynamic'),
                           foreign_keys=[user_id])


    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'id': self.id,
        }

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
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)

    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # relation with question
    q_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    # one to many with user
    user = db.relationship('User', backref=db.backref('answer_list', lazy='dynamic'))
    # one to many with question
    question = db.relationship('Question', backref=db.backref('answer_list', lazy='dynamic'))

    @property
    def like_count(self):
        return self.answer_like_list.count()

    def to_dict(self):
        return {
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user': self.user.username,
            'question': self.question.title,
            'like_count': self.like_count,
            'q_id': self.q_id,
        }


class AnswerLike(db.Model):
    __tablename__ = 'answer_like'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    # one to many with user
    user = db.relationship('User', backref=db.backref('answer_like_list', lazy='dynamic'))
    # one to many with answer
    answer = db.relationship('Answer', backref=db.backref('answer_like_list', lazy='dynamic'))
    # one to many with question
    question = db.relationship('Question', backref=db.backref('question_like_list', lazy='dynamic'))
