from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_user, LoginManager, logout_user, login_required # from prototypes or framework, create an instance
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)             # loads the configuration for the database
db = SQLAlchemy(app)                       # creates the db object using the configuration
login = LoginManager(app)
login.login_view = 'login'


from models import Contact
from forms import ContactForm, RegistrationForm, LoginForm
from models import todo, User #insults


@app.route('/')                                                                # when this url is accessed
def aboutpage():                                                               # define function
    return render_template("index.html", title="Ngunnawal Country | About", user=current_user)    # send back much of index html and change the title via jinja

@app.route("/contact.html", methods=["POST", "GET"])                                                 # user requests contact html, allows data back to the serve
def contact():
    form = ContactForm()                                                                             # load contact from models and store it locally
    if form.validate_on_submit():                                                                    # checking if the user has pressed submit
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data) # create new object which has these fields and the data that was submitted
        db.session.add(new_contact)                                                                  # temporarily writes to db
        db.session.commit()                                                                          # commits write to db
    return render_template("contact.html", title ="Contact Us", form=form, user=current_user)                           # send back an empty form

@app.route('/todo', methods=["POST", "GET"])                        # creates a new route, called to do and adds functionality of POST and GET methods
def view_todo():                                                    # def for define followed by function name
    all_todo = db.session.query(todo).all()                         # queries and retrieves the whole to do table, the results are stored into the all_todo variable
    if request.method == "POST":                                    # Checks to do form cellContent1 is attempting to submit data back to the server (POST).
        new_todo = todo(text=request.form['text'])                  # Creates a new variable - new_todo - with all data submitted
        new_todo.done = False                                       # Sets done field to False in table
        db.session.add(new_todo)                                    # temporarily writes entry into database, then commits to database permanently
        db.session.commit()
        db.session.refresh(new_todo)
        return redirect("/todo")                                    # after previous lines success, this will refresh page
    return render_template("todo.html", todos=all_todo, user=current_user)             # Sends Jinja template with data from to do table

@app.route("/todoedit/<todo_id>", methods=["POST", "GET"])          # Creates route, unique cos it accepts a variable in the route
def edit_note(todo_id):                                             # function definition
    if request.method == "POST":                                    # checks for a post
        db.session.query(todo).filter_by(id=todo_id).update({       # queries to find same id
            "text": request.form['text'],                           # if true, it updates text to whatever user wrote
            "done": True if request.form['done'] == "on" else False
        })
        db.session.commit()                                         # commits changes to db
    elif request.method == "GET":                                   # if user getting page
        db.session.query(todo).filter_by(id=todo_id).delete()       # queries to find ids with to do and deletes
        db.session.commit()                                         # commits changes to db
    return redirect("/todo", code=302)                              # sends a error to the user that the url has been moved

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email_address=form.email_address.data, name=form.name.data, user_level=1)  # defaults to regular user
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("aboutpage"))
    return render_template("registration.html", title="User Registration", form=form, user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for("homepage"))
    return render_template("login.html", title="Sign In", form=form, user=current_user)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))
@app.route('/history.html', methods=['GET', 'POST'])
def history():
    return render_template("history.html")

@app.route('/gallery.html', methods=['GET, 'POST'])
def gallery():
    render_template("gallery.html")
