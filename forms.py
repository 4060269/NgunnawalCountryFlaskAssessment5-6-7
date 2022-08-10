from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email                      # from prototypes or framework, create an instance
from wtforms import StringField, SubmitField, IntegerField

class ContactForm (FlaskForm):                                          # create a py class, it will be used as flask form
    name = StringField("Name", validators=[DataRequired()])             # defined as stringfield, to indicate string data
    email = StringField("Email", validators=[DataRequired(), Email()])  # text in double quotes are displayed on form by using jinja block
    message = StringField("Message", validators=[DataRequired()])       # validators make it a requirement to put infomation in all boxes, email() makes it to be a vaild one
    submit = SubmitField('Submit')                                      # Submit text would be inside button