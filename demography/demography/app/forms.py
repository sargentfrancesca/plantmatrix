from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


# class NameForm(Form):
#     name = StringField('What is your name?', validators=[Required()])
#     submit = SubmitField('Submit')
