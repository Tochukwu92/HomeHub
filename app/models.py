from datetime import datetime, timezone
import enum
from sqlalchemy import Enum
from flask_login import UserMixin
from app import db, bcrypt, login


@login.user_loader
def load_user(id):
    """
    This is function used by LoginManager to manage users in session
    """
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    phone_number_2 = db.Column(db.String(15))
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    posts = db.relationship(
        'Post', backref='agent', lazy=True)
    
    def __repr__(self):
        return "User<{}: {}: {}: {}>".format(
            self.id, self.first_name, self.username, self.last_seen)
    
    def set_password(self, password):
        """
        this function hashed password and convert to a string
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        this function compare if password match
        """
        return bcrypt.check_password_hash(self.password_hash, password)


class StatusEnum(enum.Enum):
    """
    this class make sure that status filed in the Post class has
    only 'Rented' or 'Vacant' options
    """
    RENTED = 'Rented'
    VACANT = 'Vacant'

class Post(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    discription = db.Column(db.Text, nullable=False)
    status = db.Column(
        Enum(StatusEnum), nullable=False, unique=True)
    country = db.Column(db.String(20))
    state = db.Column(db.String(20))
    city = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    posted_time = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    images = db.relationship(
        'Image', backref='post', lazy=True)

class Image(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    post_id = db.Column(
        db.Integer, db.ForeignKey('post.id'), nullable=False)