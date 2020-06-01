from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    post = TextAreaField("What is on your mind!", validators=[DataRequired()], id="summernote")
    submit = SubmitField("Submit")


class EditPostForm(FlaskForm):
    post = TextAreaField("What is on your mind!", validators=[DataRequired()], id="summernote")
    submit = SubmitField("Submit")
    cancel = SubmitField("Cancel")