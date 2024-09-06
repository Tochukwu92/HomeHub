from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import Optional, ValidationError
from email_validator import validate_email, EmailNotValidError
from flask_login import current_user
from app import db
from app.models import User

class RegistrationForm(FlaskForm):
    """
    A registration form
    """
    first_name = StringField(
        'First name', validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField(
        'Last name', validators=[DataRequired(), Length(min=2, max=20)])
    
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    repeat_pwd = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    phone_number = StringField('Phone number 1', validators=[DataRequired()])
    
    phone_number_2 = StringField('Phone number 2', validators=[Optional()])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        function to validate user's username
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('username already exist, choose a different username')
    
    def validate_email(self, email):
        """
        function that validate user's email
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exist, choose a different email')



class EditAcountForm(FlaskForm):
    """
    Edit user profile
    """
    first_name = StringField('First name')

    last_name = StringField('Last name')
    
    username = StringField('Username')
    
    phone_number = StringField('Phone number 1')
    
    phone_number_2 = StringField('Phone number 2')

    submit = SubmitField('Edit account')
    
    def validate_username(self, new_username):
        if new_username.data != current_user.username:
            user = User.query.filter_by(username=new_username.data).first()
            if user:
                raise ValidationError('Username already exist!')


class LoginForm(FlaskForm):
    """
    A login form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    """
    A post form
    """
    description = StringField(
        'Description', validators=[DataRequired(), Length(min=2, max=200)])
    
    country = StringField(
        'Country', validators=[Length(min=2, max=30), Optional()])
    
    state = StringField('State', validators=[Length(min=2, max=30)])
    
    city = StringField('City', validators=[DataRequired()])
    
    address = StringField('Address', validators=[DataRequired()])

    status = SelectField(
        'Satus',
        choice=['Vacant', 'Rented'],
        validators=[DataRequired()])
    
    photos = MultipleFileField('Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only')])

    submit = SubmitField('Create post')



class EditPostForm(FlaskForm):
    """
    class enable edition of posts
    """
    description = StringField(
        'Description', validators=[Length(min=2, max=200)])
    
    country = StringField(
        'Country', validators=[Length(min=2, max=30)])
    
    state = StringField('State', validators=[Length(min=2, max=30)])
    
    city = StringField('City')
    
    address = StringField('Address')

    status = SelectField(
        'Satus',
        choice=['Vacant', 'No vacant'])
    
    photos = MultipleFileField('Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only')])

    submit = SubmitField('Edit post')
