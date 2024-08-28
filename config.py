import os
from app import app

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a4394a144ef7d32f1cfcd6884bb034ba')