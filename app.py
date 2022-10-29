from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from flask_login import current_user, login_user, LoginManager, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import uuid
import os

# import random
# These imports provide the functionality of the app

app = Flask(__name__)
# Faster and cleaner way of calling the app.py flask instance
app.config.from_object(Config)
# Easier time when developing app between different devices
db = SQLAlchemy(app)
# Easier name when trying to refer to the database

login = LoginManager(app)
# More convenient way of referring to this specific class in app's flask instance
login.login_view = 'login'
# Set class to string for convenience

UPLOAD_FOLDER = './static/Images/UserImages/'
# Shortening long folder path to a simple variable
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Much quicker way of defining what extensions are allowed to be uploaded
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Simplification for interacting with the upload folder

from models import Contact, todo, User, Photos
from forms import ContactForm, RegistrationForm, LoginForm, ResetPasswordForm, UserProfileForm, PhotoUploadForm


# Linking all code here to be requested and put onto users displays based on routes


@app.route("/")
# Use traditional convention by making "/" the root route
def homepage():
    return render_template("index.html", title="Ngunnawal Country | Home", user=current_user)
    # Send them the landing/home page on first visit to introduce them to the website


@app.route("/contact", methods=["POST", "GET"])
# Add the name of the page as the new route for simplicity
def contact():
    form = ContactForm()
    # Load contact from models and store it locally
    if form.validate_on_submit():
        # Checking if the user has pressed submit
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        # Create new object which has these fields and the data that was submitted
        db.session.add(new_contact)
        # Temporarily writes to db
        db.session.commit()
        # Commits write to db
        flash("Your have successfully sent a message to us!")
        # Inform the user that the message has sent, as it isn't clear otherwise
    return render_template("contact.html", title="Ngunnawal Country | Contact Us!", form=form, user=current_user)
    # Sends back the same form with a flash message


@app.route("/todo", methods=["POST", "GET"])
# Creates a new route, called to-do and adds functionality of POST and GET methods
@login_required
# We need to authenticate that the user is an admin, if they are not, they are automatically redirected
def view_todo():
    if current_user.is_admin():
        all_todo = db.session.query(todo).all()
        # queries and retrieves the whole to do table, the results are stored into the all_todo variable
        if request.method == "POST":
            # Checks to do form cellContent1 is attempting to submit data back to the server (POST).
            new_todo = todo(text=request.form["text"])
            # Creates a new variable - new_todo - with all data submitted
            new_todo.done = False
            # Sets done field to False in table
            db.session.add(new_todo)
            db.session.commit()
            db.session.refresh(new_todo)
            flash("Your have successfully created a new task!")
            return redirect("/todo")
            # After the previous line's success, this will refresh page
        return render_template("todo.html", title="Ngunnawal Country | To Do List", todos=all_todo, user=current_user)
        # Sends Jinja template with data from to do table
    else:
        flash("You are not allowed to access this page")
        return redirect(url_for("homepage"))


@app.route("/todoedit/<todo_id>", methods=["POST", "GET"])
# Placing a variable in the route to differentiate different items
def edit_note(todo_id):
    if request.method == "POST":
        db.session.query(todo).filter_by(id=todo_id).update({
            # Queries to find same ID to allow editing
            "text": request.form['text'], "done": True if request.form['done'] == "on" else False
            # If found, it updates text to whatever user wrote
        })
        db.session.commit()
        flash("Your have successfully updated a task!")
    elif request.method == "GET":
        db.session.query(todo).filter_by(id=todo_id).delete()
        # Instead find ID to delete when they select a task
        db.session.commit()
        flash("Your have successfully deleted a task!")
    return redirect("/todo", code=302)
    # Sends an error to the user that the url has been moved


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email_address=form.email_address.data, name=form.name.data, user_level=1, active=1)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Your have successfully registered your account")
        return redirect(url_for("homepage"))
    return render_template("registration.html", title="Ngunnawal Country | User Registration", form=form,
                           user=current_user)
    # Once details are entered and submitted, we need to take data, make it local, set properties then commit to db


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data) or not user.active:
            flash("Your password is incorrect or your account has been disabled, contact us to check this")
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
    if current_user.is_anonymous:
        return render_template("galleryanonymous.html", title="Ngunnawal Country | Gallery", user=current_user)
    else:
        user_images = Photos.query.filter_by(userid=current_user.id).all()
    return render_template("gallery.html", title="Ngunnawal Country | Gallery", user=current_user, images=user_images)


@app.route('/passwordreset', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=current_user.email_address).first()
        user.set_password(form.new_password.data)
        db.session.commit()
        flash("Your password has been reset")
        return redirect(url_for("homepage"))
    return render_template('passwordreset.html', title="Ngunnawal Country | Password Reset", form=form,
                           user=current_user)


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
        flash("Your details have been changed successfully")
        return redirect(url_for("homepage"))
    return render_template("userprofile.html", title="Ngunnawal Country | Profile", user=current_user, form=form)


@app.route('/contactmessages', methods=['GET'])
@login_required
def view_contact_messages():
    if current_user.is_admin():
        contact_messages = Contact.query.all()
        return render_template("contactmessages.html", title="Ngunnawal Country | Contact Messages",
                               user=current_user, messages=contact_messages)
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
            flash("Image has been successfully uploaded!")
            return redirect(url_for("photos"))
        else:
            flash("The image upload has failed")
    return render_template("uploadphotos.html", title="Ngunnawal Country | Upload Photos", user=current_user, form=form)


@app.route('/listallusers', methods=['GET', 'POST'])
@login_required
def list_all_users():
    if current_user.is_admin():
        all_users = User.query.all()
        return render_template("listAllUsers.html", title="Ngunnawal Country | All Active Users", user=current_user,
                               users=all_users)
    else:
        flash("You are not allowed to access this page")
        return redirect(url_for("homepage"))


@app.route('/passwordreset/<userid>', methods=['GET', 'POST'])
@login_required
def reset_user_password(userid):
    form = ResetPasswordForm()
    user = User.query.filter_by(id=userid).first()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password has been reset for user {}'.format(user.name))
        return redirect(url_for('homepage'))
    return render_template("passwordreset.html", title='Ngunnawal Country | Administrator Reset Password', form=form,
                           user=user)


@app.route('/userenable/<userid>')
@login_required
def user_enable(userid):
    if current_user.is_admin():
        user = User.query.filter_by(id=userid).first()
        user.active = not user.active
        db.session.commit()
        return redirect(url_for("list_all_users"))
    else:
        flash("You are not allowed to access this page")
        return redirect(url_for("homepage"))
