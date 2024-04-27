import os

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

from models import Question, db, Answer


class WriteQuestionForm(FlaskForm):
    img = FileField(label='upload picture', render_kw={
        'accept': ".jpeg, .jpg, .png"
    }, validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Please select the appropriate image type')
    ])
    title = StringField(label='title', render_kw={
        'class': "form-group",
        'placeholder': "Enter title (up to 50 characters)"
    }, validators=[DataRequired('Please enter the title'),
                   Length(min=3, max=50, message='Title length is 1-50 characters')])

    desc = TextAreaField(label='description', render_kw={
        'class': "form-group",
        'placeholder': "简述"
    }, validators=[Length(max=150, message='Description is up to 150 characters')])
    content = CKEditorField(label='content', render_kw={
        'class': "form-group",
        'placeholder': "Enter the text"
    }, validators=[DataRequired('Please enter the text'),
                   Length(min=5, message='Cannot be less than 5 characters')])

    def save(self):
        # 1. Get the image
        img = self.img.data
        img_name = ''
        if img:
            img_name = secure_filename(img.filename)
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        # 2. Save the question
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        que_obj = Question(
            title=title,
            desc=desc,
            img=img_name,
            content=content,
            user=current_user
        )
        db.session.add(que_obj)
        db.session.commit()
        return que_obj

#
class WriteAnswerForm(FlaskForm):

    content = CKEditorField(label='answer_content', validators=[
        DataRequired('Please enter the text'),
        Length(min=5, message='Cannot be less than 5 characters')
    ])

    def save(self, question):


        content = self.content.data
        user = current_user
        answer_obj = Answer(content=content, user=user, question=question)
        db.session.add(answer_obj)
        db.session.commit()
        return answer_obj
