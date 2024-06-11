from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DiaryEntryForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Add Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class UpdateEntryForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Update Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

