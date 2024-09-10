import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    """
    #  form securiy configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a4394a144ef7d32f1cfcd6884bb034ba'

    # sqlite database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'homehub_storage.db')

    
    # image configuration
    UPLOAD_FOLDER = 'static/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','gif'}