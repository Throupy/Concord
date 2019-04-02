from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from functional.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email makes sure it's a valid email
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    subscribe = BooleanField('Subscribe to recieve cool information')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):  # pass in input field to be validated (username in this case)
        user = User.query.filter_by(username=username.data).first()  # if there is no user already in the database with these credentials. then this variable will be None.
        if user:  # if the entered crentials are taken
            raise ValidationError('That username is taken. Please use a different one!')  # raise an error
            # this error will be the 'gucci' one that is displayed underneath the input box in a nice red text! (I <3 Bootstrap!)

    def validate_email(self, email):  # pass in input field to be validated (username in this case)
        user = User.query.filter_by(email=email.data).first()  # if there is no user already in the database with these credentials. then this variable will be None.
        if user:  # if the entered crentials are taken
            raise ValidationError('That email is taken. Please use a different one!')  # raise an error
            # this error will be the 'gucci' one that is displayed underneath the input box in a nice red text! (I <3 Bootstrap!)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'HEIC'])])
    banner = FileField('Update Banner', validators=[FileAllowed(['jpg', 'png', 'HEIC'])])
    submit = SubmitField('Update')


class SendEmailForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', widget=TextArea(), validators=[DataRequired(), Length(min=20)])
    submit = SubmitField('Send')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email() makes sure it's a valid email
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):  # pass in input field to be validated (username in this case)
        user = User.query.filter_by(email=email.data).first()  # if there is no user already in the database with these credentials. then this variable will be None.
        if user is None:  # if the entered crentials are taken
            raise ValidationError('There is no account with that email, you must register first!')  # raise an error
            # this error will be the 'gucci' one that is displayed underneath the input box in a nice red text! (I <3 Bootstrap!)


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
