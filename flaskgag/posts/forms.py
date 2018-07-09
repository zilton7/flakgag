from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    post_picture = FileField('Select Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif']), DataRequired()])
    content = TextAreaField('Description')
    submit = SubmitField('Post')