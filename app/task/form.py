import os
import uuid
from uuid import uuid4

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

from models import Task, db, Answer


class WriteTaskForm(FlaskForm):
    img = FileField(
        'Upload Picture',
        render_kw={'accept': ".jpeg, .jpg, .png"},
        validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Images only!')]
    )
    title = StringField(
        'Title',
        render_kw={
            'class': "form-group",
            'placeholder': "Enter title (up to 50 characters)"
        },
        validators=[
            DataRequired('Title is required'),
            Length(min=3, max=50, message='Title must be between 3 and 50 characters')
        ]
    )

    content = CKEditorField(
        'Content',
        render_kw={
            'class': "form-group",
            'placeholder': "Enter your content"
        },
        validators=[
            DataRequired('Content is required'),
            Length(min=5, message='Content must be at least 5 characters')
        ]
    )

    def save(self):
        """ Save the posted task with image if provided.
            The function returns the task object after saving it to the database.
        """
        # Get the image if uploaded
        img = self.img.data
        img_name = ''
        if img:
            filename_base, file_extension = os.path.splitext(secure_filename(img.filename))
            img_name = secure_filename(f"{uuid.uuid4()}{file_extension}")
            img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img_name)
            img.save(img_path)

            # file_extension = os.path.splitext(avatar_file.filename)[1]
            # random_filename = str(uuid.uuid4()) + file_extension
            # secure_random_filename = secure_filename(random_filename)
            #
            # save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_random_filename)
            # avatar_file.save(save_path)

        # Save the task details
        task = Task(
            title=self.title.data,
            img=img_name,
            content=self.content.data,
            user=current_user
        )
        db.session.add(task)
        db.session.commit()

        return task


class WriteAnswerForm(FlaskForm):
    content = CKEditorField(
        'Answer Content',
        validators=[
            DataRequired('Content is required'),
            Length(min=5, message='Content must be at least 5 characters')
        ]
    )

    def save(self, task):
        """ Save the provided answer to a task.
            Requires passing the associated task object.
            Returns the answer object after saving it to the database.
        """
        answer = Answer(
            content=self.content.data,
            user=current_user,
            task=task
        )
        db.session.add(answer)
        db.session.commit()

        return answer