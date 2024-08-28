from flask_wtf import FlaskForm
from wtforms import StringFieldd, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


class RegistrationForm(FlaskForm):
    """
    A registration form
    """
    first_name = StringFieldd(
        'First name', validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringFieldd(
        'Last name', validators=[DataRequired(), Length(min=2, max=20)])
    
    username = StringField(
        'Username', validators=(DataRequired(), Length(min=2, max=20)))
    
    email = StringField('Email', validators=(DataRequired(), Email()))
    
    password = PasswordField('Password', validators=[DataRequired()])
    
     repeat_pwd = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    phone_number = StringField('Phone number 1', validators=(DataRequired()))
    
    phone_number_2 = StringField('Phone number 2', Optional())

    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):
    """
    A login form
    """
    email = StringField('Email', validators=(DataRequired(), Email()))
    
    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Login')