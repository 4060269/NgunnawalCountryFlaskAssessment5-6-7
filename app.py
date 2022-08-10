from flask import Flask
from flask import Flask, render_template, request, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)  # loads the configuration for the database
db = SQLAlchemy(app)            # creates the db object using the configuration

from models import Contact
from forms import ContactForm
from models import todo #insults

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

@app.route('/todo', methods=["POST", "GET"])
def view_todo():
    all_todo = db.session.query(todo).all()
    if request.method == "POST":
        new_todo = todo(text=request.form['text'])
        new_todo.done = False
        db.session.add(new_todo)
        db.session.commit()
        db.session.refresh(new_todo)
        return redirect("/todo")
    return render_template("todo.html", todos=all_todo)

@app.route("/todoedit/<todo_id>", methods=["POST", "GET"])
def edit_note(todo_id): # Creates the route and python function. This is different from other routes as it accepts a variable in the route.
    if request.method == "POST":
        db.session.query(todo).filter_by(id=todo_id).update({
            "text": request.form['text'],
            "done": True if request.form['done'] == "on" else False
        })
        db.session.commit()
    elif request.method == "GET":
        db.session.query(todo).filter_by(id=todo_id).delete()
        db.session.commit()
    return redirect("/todo", code=302)
