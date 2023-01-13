# Import the Flask Class from the flask module - will be main object
from flask import Flask
# Import SQLAlchemy and Migrate from their modules
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# Import the Config class from the config module - will have all of the app's configurations
from config import Config

# Create an instance of the Flask Class called app
app = Flask(__name__)

# Configure the app using the Config class
app.config.from_object(Config)

# Create an instance of SQLAlchemy to represent our database
db = SQLAlchemy(app)

# Create an instance of Migrate to represent our migration engine
migrate = Migrate(app, db)

# Create an Instance of Login Manager to set up login fucntionality
login = LoginManager(app)

#set login view to redirect unauth users
login.login_view = 'login'
login.login_message = 'Must be logged in to access this page'
login.login_message_category = 'danger'

# import all of the routes and models from the routes/models file into the current folder
from . import routes, models