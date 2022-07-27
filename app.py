from flask import Flask
from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)  # loads the configuration for the database
db = SQLAlchemy(app)            # creates the db object using the configuration


@app.route('/')
def aboutpage():  # put application's code here
    return render_template("index.html", title="Ngunnawal Country | About")


if __name__ == '__main__':
    app.run()
