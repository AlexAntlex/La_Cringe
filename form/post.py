from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField


class PostForm(FlaskForm):
    file_url = FileField()
    submit = SubmitField('Publicate')