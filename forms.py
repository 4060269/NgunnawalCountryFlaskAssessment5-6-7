# Forms.py is where all the form code goes
# To keep it easily maintainable and editable

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, IntegerField, PasswordField, FileField
from flask_wtf.file import FileRequired
from models import User


# Using flask's integrated form class's from, flask_wtf called wtforms,
# to easily send forms in the one object request of the website
# Need the user information from models to associate users to forms


class ContactForm(FlaskForm):
    # create a py class, it will be used as flask form
    name = StringField("Name", validators=[DataRequired()], render_kw={"class": "text-box"})
    # defined as string-field, to indicate string data
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"class": "text-box"})
    # text in double quotes are displayed on form by using jinja block
    message = StringField("Message", validators=[DataRequired()], render_kw={"class": "text-box"})
    # validators make it a requirement to put information in all boxes, email() makes it to be a valid one
    submit = SubmitField('Submit', render_kw={"class": "btn"})
    # render_kw used to keep the UI of the website consistent


class RegistrationForm(FlaskForm):
    email_address = StringField("Email Address (Username)", validators=[DataRequired(), Email()],
                                render_kw={"class": "text-box"})
    name = StringField("Full Name", validators=[DataRequired()], render_kw={"class": "text-box"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"class": "text-box"})
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")],
                                     render_kw={"class": "text-box"})
    submit = SubmitField('Register', render_kw={"class": "btn"})


def validate_email_address(self, email_address_to_register):
    user = User.query.filter_by(email_address=email_address_to_register.data).first()
    if user is not None:
        raise ValidationError("Please Use a Different Email Address")
    # Need to validate if the user submitting data has a valid email address in db to avoid spam and security issues


class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired()], render_kw={"class": "text-box"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "text-box"})
    submit = SubmitField('Sign In', render_kw={"class": "btn"})


class ResetPasswordForm(FlaskForm):
    new_password = StringField("New Password", validators=[DataRequired()], render_kw={"class": "text-box"})
    new_password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("new_password")],
                                         render_kw={"class": "text-box"})
    submit = SubmitField('Submit', render_kw={"class": "btn"})


class UserProfileForm(FlaskForm):
    email_address = StringField("Email Address (Username)", validators=[DataRequired(), Email()],
                                render_kw={"class": "text-box"})
    name = StringField("Full Name", validators=[DataRequired()], render_kw={"class": "text-box"})
    submit = SubmitField("Update Profile", render_kw={"class": "btn"})


class PhotoUploadForm(FlaskForm):
    title = StringField("Image Title", validators=[DataRequired()], render_kw={"class": "text-box"})
    image = FileField('Photo File Upload', validators=[FileRequired()])
    submit = SubmitField("Upload Photo", render_kw={"class": "btn"})
