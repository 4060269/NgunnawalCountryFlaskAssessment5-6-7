from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from flask_login import current_user, login_user, LoginManager, logout_user, login_required # from prototypes or framework, create an instance
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import random, os
import uuid

app = Flask(__name__)
app.config.from_object(Config) # loads the configuration for the database
db = SQLAlchemy(app)           # creates the db object using the configuration
login = LoginManager(app)
login.login_view = 'login'

UPLOAD_FOLDER = './static/Images/UserImages/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from models import Contact, todo, User, Photos
from forms import ContactForm, RegistrationForm, LoginForm, ResetPasswordForm, UserProfileForm, PhotoUploadForm

@app.route('/')                                                                # when this url is accessed
def homepage():                                                               # define function
    return render_template("index.html", title="Ngunnawal Country | Home", user=current_user) # send back much of index html and change the title via jinja

@app.route("/contact", methods=["POST", "GET"])                                                      # user requests contact html, allows data back to the serve
def contact():
    form = ContactForm()                                                                             # load contact from models and store it locally
    if form.validate_on_submit():                                                                    # checking if the user has pressed submit
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data) # create new object which has these fields and the data that was submitted
        db.session.add(new_contact)                                                                  # temporarily writes to db
        db.session.commit()                                                                          # commits write to db
        flash("Your have successfully sent a message to us!")
    return render_template("contact.html", title="Ngunnawal Country | Contact Us!", form=form, user=current_user) # send back an empty form

@app.route('/todo', methods=["POST", "GET"])
@login_required                                     # creates a new route, called to do and adds functionality of POST and GET methods
def view_todo():                      # def for define followed by function name
    if current_user.is_admin():
        all_todo = db.session.query(todo).all()  # queries and retrieves the whole to do table, the results are stored into the all_todo variable
        if request.method == "POST":  # Checks to do form cellContent1 is attempting to submit data back to the server (POST).
            new_todo = todo(text=request.form['text'])  # Creates a new variable - new_todo - with all data submitted
            new_todo.done = False  # Sets done field to False in table
            db.session.add(new_todo)  # temporarily writes entry into database, then commits to database permanently
            db.session.commit()
            db.session.refresh(new_todo)
            flash("Your have successfully created a new task!")
            return redirect("/todo")  # after previous lines success, this will refresh page
        return render_template("todo.html", title="Ngunnawal Country | To Do List", todos=all_todo, user=current_user)  # Sends Jinja template with data from to do table
    else:
        flash("You are not allowed to access this page")
        return redirect(url_for("homepage"))

@app.route("/todoedit/<todo_id>", methods=["POST", "GET"])          # Creates route, unique cos it accepts a variable in the route
def edit_note(todo_id):                                             # function definition
    if request.method == "POST":                                    # checks for a post
        db.session.query(todo).filter_by(id=todo_id).update({       # queries to find same id
            "text": request.form['text'],                           # if true, it updates text to whatever user wrote
            "done": True if request.form['done'] == "on" else False
        })
        db.session.commit()
        flash("Your have successfully updated a task!")             # commits changes to db
    elif request.method == "GET":                                   # if user getting page
        db.session.query(todo).filter_by(id=todo_id).delete()       # queries to find ids with to do and deletes
        db.session.commit()
        flash("Your have successfully deleted a task!")             # commits changes to db
    return redirect("/todo", code=302)                              # sends a error to the user that the url has been moved

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email_address=form.email_address.data, name=form.name.data, user_level=1)  # defaults to regular user
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Your have successfully registered your account")
        return redirect(url_for("homepage"))
    return render_template("registration.html", title="Ngunnawal Country | User Registration", form=form, user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid credentials")
            return redirect(url_for('login'))
        login_user(user)
        flash("Your have logged in")
        return redirect(url_for("homepage"))
    return render_template("login.html", title="Ngunnawal Country | Login", form=form, user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    flash("Your have logged out")
    return redirect(url_for('homepage'))

@app.route('/history', methods=['GET', 'POST'])
def history():
    return render_template("history.html", title="Ngunnawal Country | History", user=current_user)

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    all_images = Photos.query.all()
    return render_template("gallery.html", title="Ngunnawal Country | Gallery", user=current_user, images=all_images)

@app.route('/passwordreset', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=current_user.email_address).first()
        user.set_password(form.new_password.data)
        db.session.commit()
        flash("Your Password has been reset")
        return redirect(url_for('homepage'))
    return render_template('passwordreset.html', title="Ngunnawal Country | Password Reset", form=form, user=current_user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Ngunnawal Country | 404 Error", user=current_user), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Ngunnawal Country | 500 Error", user=current_user), 500

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm()
    user = User.query.filter_by(email_address=current_user.email_address).first()
    if request.method == 'GET':
        form.name.data = user.name
        form.email_address.data = user.email_address
    if form.validate_on_submit():
        user.update_details(email_address=form.email_address.data, name=form.name.data)
        db.session.commit()
        flash("Your details have been changed")
        return redirect(url_for("homepage"))
    return render_template("userprofile.html", title="Ngunnawal Country | Profile", user=current_user, form=form)

@app.route('/contactmessages', methods=['GET'])
@login_required
def view_contact_messages():
    if current_user.is_admin():
        contact_messages = Contact.query.all()
        return render_template("contactmessages.html", title="Ngunnawal Country | Contact Messages", user=current_user, messages=contact_messages)
    else:
        flash("You are not allowed to access this page")
        return redirect(url_for("homepage"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadphotos', methods=['GET', 'POST'])
@login_required
def photos():
    form = PhotoUploadForm()
    user_images = Photos.query.filter_by(userid=current_user.id).all()
    if form.validate_on_submit():
        new_image = form.image.data
        filename = secure_filename(new_image.filename)

        if new_image and allowed_file(filename):
            # Get the file extension of the file.
            file_ext = filename.split(".")[1]
            random_filename = str(uuid.uuid4())
            filename = random_filename + "." + file_ext

            new_image.save(os.path.join(UPLOAD_FOLDER, filename))
            photo = Photos(title=form.title.data, filename=filename, userid=current_user.id)
            db.session.add(photo)
            db.session.commit()
            flash("Image Uploaded")
            return redirect(url_for("photos"))
        else:
            flash("The File Upload failed.")
    return render_template("uploadphotos.html", title="Upload Photos", user=current_user, form=form, images=user_images)
