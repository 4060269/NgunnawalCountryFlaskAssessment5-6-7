from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError                     # from prototypes or framework, create an instance
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from models import User

class ContactForm (FlaskForm):                                          # create a py class, it will be used as flask form
    name = StringField("Name", validators=[DataRequired()])             # defined as stringfield, to indicate string data
    email = StringField("Email", validators=[DataRequired(), Email()])  # text in double quotes are displayed on form by using jinja block
    message = StringField("Message", validators=[DataRequired()])       # validators make it a requirement to put infomation in all boxes, email() makes it to be a vaild one
    submit = SubmitField('Submit')                                      # Submit text would be inside button
class RegistrationForm(FlaskForm):
    email_address = StringField("Email Address (Username)", validators=[DataRequired(), Email()])
    name = StringField("Full Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")
def validate_email_address(self, email_address_to_register):
  user = User.query.filter_by(email_address=email_address_to_register.data).first()
  if user is not None:
      raise ValidationError("Please Use a Different Email Address)")

class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')