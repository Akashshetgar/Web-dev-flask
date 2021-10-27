from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.fields.core import Label
from wtforms.fields.simple import SubmitField
from wtforms.validators import Length,DataRequired,Email,EqualTo, ValidationError
from Bonfire.models import User

class RegistrationForm(FlaskForm):
    def validate_username(self,check_username):
        user = User.query.filter_by(username = check_username.data).first()
        if user:
            raise ValidationError("Username already exists")
    def validate_email(self,check_email):
        user = User.query.filter_by(emailId = check_email.data).first()
        if user:
            raise ValidationError("E-mail already exists")
    username = StringField(label='Username',validators = [Length(min=2,max=30),DataRequired()])
    email = StringField(label='E-mail', validators = [Email(),DataRequired()])
    password = PasswordField(label='Password', validators = [Length(min=6),DataRequired()])
    conpassword = PasswordField(label='Confirm Password', validators = [EqualTo('password'),DataRequired()])
    register = SubmitField(label='Register')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators= [DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    login = SubmitField(label='Login')
