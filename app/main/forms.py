from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, Email, Length
# from flask_ckeditor import CKEditorField
from flask_login import current_user
from app.models import User



class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("Bio", validators=[Length(min=0, max=200)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError("Please use a different email address.")


class PostForm(FlaskForm):
    #post = CKEditorField("What is on your mind!", validators=[DataRequired()])
    post = TextAreaField("What is on your mind!", validators=[DataRequired()], id="summernote")
    submit = SubmitField("Submit")
