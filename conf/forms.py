from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, FileField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    recaptcha = RecaptchaField()

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=16)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=3, max=320)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    recaptcha = RecaptchaField()

class DeleteForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    recaptcha = RecaptchaField()

class AccountForm(FlaskForm):
    newsletter = BooleanField('newsletter')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    title = StringField('title', validators=[InputRequired()])