from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo,Email

class regform (FlaskForm):
    username= StringField('Username',validators=[DataRequired(),Length(min=3,max=15)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password= PasswordField('Password', validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(),Length(min=4),EqualTo('password')])
    submit= SubmitField('Sign Up')

class logform (FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password= PasswordField('Password', validators=[DataRequired(),Length(min=4)])
    remember_me=BooleanField('Remember Me')
    submit= SubmitField('Log In')