from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# application instance
app = Flask(__name__)

# initializes all configuration from Config class to flask app 
app.config.from_object('config.Config')

# database instance
db = SQLAlchemy(app)

# bcrypt instance for password hashing
bcrypt = Bcrypt(app)

# login manager instance for user validation and authentication
login = LoginManager(app)

# redirect any user not logged in but tries to access login_required route
login.login_view = 'login'

login.login_message_category = 'info'




from app import routes, models
