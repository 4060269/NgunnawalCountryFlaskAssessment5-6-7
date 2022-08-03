from flask import Flask
from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from models import Contact
from forms import ContactForm

app = Flask(__name__)
app.config.from_object(Config)  # loads the configuration for the database
db = SQLAlchemy(app)            # creates the db object using the configuration


@app.route('/')
def aboutpage():  # put application's code here
    return render_template("index.html", title="Ngunnawal Country | About")

@app.route("/contact.html", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
    return render_template("contact.html", title ="Contact Us", form=form)

if __name__ == '__main__':
    app.run()
