from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField


class ChangeIngoForm(FlaskForm):
    name = StringField('Name')
    info = TextAreaField('Info')
    avatar = FileField()
    submit = SubmitField('Submit')