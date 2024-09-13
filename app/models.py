from datetime import datetime, timezone
from flask_login import UserMixin
from app import db, bcrypt, login



class User(db.Model, UserMixin):
    """
    Database column field for all the classes
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    phone_number_2 = db.Column(db.String(15))
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    posts = db.relationship(
        'Post', backref='agent', lazy=True)
    
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



class Post(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(20))
    state = db.Column(db.String(20))
    city = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    posted_time = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    images = db.relationship(
        'PostImage', backref='post', lazy=True)


class PostImage(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    post_id = db.Column(
        db.Integer, db.ForeignKey('post.id'), nullable=False)
    

@login.user_loader
def load_user(id):
    """
    This is function used by LoginManager to manage users in session
    """
    return User.query.get(int(id))