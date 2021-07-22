from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from . import db


class regform (FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), Length(min=4), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if db.does_username_exist(username.data):
            raise ValidationError("Username already exists.")

    def validate_email(self, email):
        if db.does_email_exist(email.data):
            raise ValidationError("This email is already registered.")


class logform (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    def validate_email_and_password(self, email,password):
        if not db.does_email_exist(email.data):
            raise ValidationError("This email is not registered.")
        elif not db.does_email_and_password_match(email.data, password.data):
            raise ValidationError("Incorrect Password")
